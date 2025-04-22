import atexit
import logging
import os
import sqlite3
from pathlib import Path
from typing import (
    Literal,
)

import boto3
import zstd
from botocore import (
    UNSIGNED,
)
from botocore.config import (
    Config,
)
from platformdirs import (
    user_data_dir,
)

from labels.advisories.match_versions import match_vulnerable_versions
from labels.advisories.utils import generate_cpe
from labels.model.advisories import Advisory

LOGGER = logging.getLogger(__name__)

BUCKET_NAME = "skims.sca"
DB_NAME = "skims_sca_advisories_for_images.db"
BUCKET_FILE_KEY = f"{DB_NAME}.zst"
CONFIG_DIRECTORY = user_data_dir(
    appname="fluid-labels",
    appauthor="fluidattacks",
    ensure_exists=True,
)
DB_LOCAL_PATH = os.path.join(CONFIG_DIRECTORY, DB_NAME)
DB_LOCAL_COMPRESSED_PATH = f"{DB_LOCAL_PATH}.zst"
S3_SERVICE_NAME: Literal["s3"] = "s3"
S3_CLIENT = boto3.client(
    service_name=S3_SERVICE_NAME,
    config=Config(
        region_name="us-east-1",
        signature_version=UNSIGNED,
    ),
)


def get_package_advisories(
    package_manager: str,
    package_name: str,
    version: str,
    platform_version: str,
) -> list[Advisory]:
    connection = DATABASE.get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            adv_id,
            source,
            vulnerable_version,
            severity_level,
            severity,
            severity_v4,
            epss,
            details,
            percentile
        FROM advisories
        WHERE package_manager = ? AND platform_version = ? AND package_name = ?;
        """,
        (package_manager, platform_version, package_name),
    )
    return [
        Advisory(
            id=result[0],
            urls=[result[1]],
            version_constraint=result[2] or None,
            severity=result[3] or "Low",  # F011 cvss4 severity
            cvss3=result[4],
            cvss4=result[5],
            epss=result[6] or 0.0,
            description=result[7] or None,
            percentile=result[8] or 0.0,
            cpes=[generate_cpe(package_manager, package_name, version)],
            namespace=package_manager,
        )
        for result in cursor.fetchall()
    ]


def get_vulnerabilities(
    platform: str,
    product: str,
    version: str,
    platform_version: str | None,
) -> list[Advisory]:
    vulnerabilities = []
    if (
        product
        and version
        and platform_version
        and (
            advisories := get_package_advisories(
                platform,
                product.lower(),
                version,
                platform_version,
            )
        )
    ):
        vulnerabilities = [
            advisor
            for advisor in advisories
            if match_vulnerable_versions(version.lower(), advisor.version_constraint)
        ]

    return vulnerabilities


def _get_database_file() -> None:
    LOGGER.info("⬇️ Downloading advisories database")
    S3_CLIENT.download_file(
        Bucket=BUCKET_NAME,
        Key=BUCKET_FILE_KEY,
        Filename=DB_LOCAL_COMPRESSED_PATH,
    )
    LOGGER.info("🗜️ Decompressing advisories database")

    try:
        with Path(DB_LOCAL_COMPRESSED_PATH).open("rb") as compressed_file:
            compressed_data = compressed_file.read()
        uncompressed_data = zstd.decompress(compressed_data)
        with Path(DB_LOCAL_PATH).open("wb") as output_file:
            output_file.write(uncompressed_data)
    except Exception:
        LOGGER.exception("❌ Unable to decompress database %s")


def initialize_db() -> bool:
    local_database_exists = Path(DB_LOCAL_PATH).is_file()

    try:
        db_metadata = S3_CLIENT.head_object(Bucket=BUCKET_NAME, Key=BUCKET_FILE_KEY)
        up_to_date = (
            local_database_exists
            and Path(DB_LOCAL_PATH).stat().st_mtime >= db_metadata["LastModified"].timestamp()
        )

        if up_to_date:
            LOGGER.info("✅ Advisories database is up to date")
            return True
        _get_database_file()
        Path(DB_LOCAL_COMPRESSED_PATH).unlink()
    except Exception:
        if local_database_exists:
            LOGGER.warning(
                "⚠️ Advisories may be outdated, unable to update database",
            )
            return True

        LOGGER.exception(
            "❌ Advisories won't be included, unable to download database",
        )
        return False
    else:
        return True


class Database:
    def __init__(self) -> None:
        self.connection: sqlite3.Connection | None = None

    def initialize(self) -> None:
        if self.connection is None and initialize_db():
            self.connection = sqlite3.connect(
                DB_LOCAL_PATH,
                check_same_thread=False,
            )
            atexit.register(self.connection.close)

    def get_connection(self) -> sqlite3.Connection:
        if self.connection is not None:
            return self.connection
        self.connection = sqlite3.connect(
            DB_LOCAL_PATH,
            check_same_thread=False,
        )
        atexit.register(self.connection.close)
        return self.connection


DATABASE = Database()
