from labels.format.common import (
    process_packages,
)
from labels.format.cyclone_dx.file_builder import (
    format_cyclonedx_sbom,
)
from labels.format.fluid import (
    format_fluid_sbom,
)
from labels.format.spdx.file_builder import (
    format_spdx_sbom,
)
from labels.model.core import SbomConfig
from labels.model.package import Package
from labels.model.relationship import (
    Relationship,
)
from labels.model.resolver import Resolver


def format_sbom(
    *,
    packages: list[Package],
    relationships: list[Relationship],
    config: SbomConfig,
    resolver: Resolver,
) -> None:
    packages = process_packages(packages)
    match config.output_format:
        case "fluid-json":
            format_fluid_sbom(
                packages=packages,
                relationships=relationships,
                config=config,
                resolver=resolver,
            )
        case "cyclonedx-json":
            format_cyclonedx_sbom(
                packages=packages,
                relationships=relationships,
                config=config,
                resolver=resolver,
            )
        case "cyclonedx-xml":
            format_cyclonedx_sbom(
                packages=packages,
                relationships=relationships,
                config=config,
                resolver=resolver,
            )
        case "spdx-json":
            format_spdx_sbom(
                packages=packages,
                _relationships=relationships,
                file_format="json",
                config=config,
                resolver=resolver,
            )
        case "spdx-xml":
            format_spdx_sbom(
                packages=packages,
                _relationships=relationships,
                file_format="xml",
                config=config,
                resolver=resolver,
            )
