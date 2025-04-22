import logging
from typing import TYPE_CHECKING

from labels.utils.strings import format_exception

if TYPE_CHECKING:
    from collections.abc import ItemsView
from typing import cast

from packageurl import PackageURL
from pydantic import ValidationError

from labels.internal.collection.types import IndexedDict
from labels.internal.collection.yaml import parse_yaml_with_tree_sitter
from labels.model.file import DependencyType, Location, LocationReadCloser
from labels.model.package import Language, Package, PackageType
from labels.model.relationship import Relationship
from labels.model.resolver import Resolver
from labels.pkg.cataloger.generic.parser import Environment

LOGGER = logging.getLogger(__name__)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        location.dependency_type = DependencyType.DIRECT
        return location.model_copy(update=l_upd)
    return location


def _get_packages(
    reader: LocationReadCloser,
    dependencies: IndexedDict[str, str] | None,
) -> list[Package]:
    if dependencies is None:
        return []

    packages = []

    general_location = _get_location(reader.location, dependencies.position.start.line)
    items: ItemsView[str, IndexedDict[str, str] | str] = dependencies.items()
    for name, version in items:
        if not name or not isinstance(version, str) or not version:
            continue

        try:
            packages.append(
                Package(
                    name=name,
                    version=version,
                    locations=[general_location],
                    language=Language.DART,
                    licenses=[],
                    type=PackageType.DartPubPkg,
                    p_url=PackageURL(  # type: ignore
                        type="pub",
                        name=name,
                        version=version,
                    ).to_string(),
                ),
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types are incorrect.",
                extra={
                    "extra": {
                        "exception": format_exception(str(ex)),
                        "location": general_location.path(),
                    },
                },
            )
            continue
    return packages


def parse_pubspec_yaml(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    content = cast(
        IndexedDict[str, IndexedDict[str, str]],
        parse_yaml_with_tree_sitter(reader.read_closer.read()),
    )
    deps: IndexedDict[str, str] | None = content.get("dependencies")
    dev_deps: IndexedDict[str, str] | None = content.get("dev_dependencies")
    packages = [
        *_get_packages(reader, deps),
        *_get_packages(reader, dev_deps),
    ]
    return packages, []
