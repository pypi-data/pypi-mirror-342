import os
from typing import Any

from pydantic import BaseModel, ConfigDict


class AwsCredentials(BaseModel):
    access_key_id: str
    secret_access_key: str
    session_token: str | None


class AwsRole(BaseModel):
    external_id: str
    role: str


class LayerData(BaseModel):
    mimetype: str
    digest: str
    size: int
    annotations: dict[str, str] | None
    model_config = ConfigDict(frozen=True)


class ImageMetadata(BaseModel):
    name: str
    digest: str
    repotags: list[str]
    created: str
    dockerversion: str
    labels: dict[str, str] | None
    architecture: str
    os: str
    layers: list[str]
    layersdata: list[LayerData]
    env: list[str]
    image_ref: str = ""
    model_config = ConfigDict(frozen=True)


class LayerInfo(BaseModel):
    id_: str
    tar_full_path: str
    metadata: dict[str, Any]


class ImageContext(BaseModel):
    id: str
    name: str
    publisher: str | None
    arch: str
    size: str
    full_extraction_dir: str
    layers_dir: str
    manifest: dict[str, Any]
    image_ref: str

    def get_layer_info(self, layer_id: str) -> LayerInfo | None:
        if layer_metadata := next(x for x in self.manifest["layers"] if x["id"] == layer_id):
            return LayerInfo(
                id_=layer_id,
                tar_full_path=os.path.join(self.layers_dir, layer_metadata),
                metadata=layer_metadata,
            )
        return None
