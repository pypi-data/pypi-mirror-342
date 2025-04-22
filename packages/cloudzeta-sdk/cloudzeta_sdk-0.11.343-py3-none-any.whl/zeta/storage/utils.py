from dataclasses import dataclass
from enum import Enum
import os

from zeta.utils.logging import zetaLogger


class StorageVendor(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


@dataclass
class StorageConfig(object):
    vendor: StorageVendor
    url: str

    def to_dict(self):
        return {
            "vendor": self.vendor.value,
            "bucketUrl": self.bucketUrl,
        }

    @classmethod
    def create_default(cls):
        vendor_name = os.getenv("ZETA_DEFAULT_STORAGE_VENDOR")
        if vendor_name == StorageVendor.AZURE.value:
            account = os.getenv("AZURE_STORAGE_ACCOUNT")
            container = os.getenv("AZURE_STORAGE_CONTAINER")
            if not account or not container:
                raise ValueError(
                    "Environment variables AZURE_STORAGE_ACCOUNT and AZURE_STORAGE_CONTAINER must "
                    "be set for Azure storage."
                )
            vendor_url = f"https://{account}.blob.core.windows.net/{container}"
        elif vendor_name == StorageVendor.GCP.value:
            vendor_url = os.getenv("GOOGLE_STORAGE_BUCKET")
            if not vendor_url:
                raise ValueError(
                    "Environment variable GOOGLE_STORAGE_BUCKET must be set for GCP storage."
                )
        else:
            raise ValueError(f"Invalid storage vendor: {vendor_name}")

        return cls(vendor=StorageVendor(vendor_name), url=vendor_url)

    @classmethod
    def create_genai_models_config(cls):
        vendor_name = os.getenv("ZETA_DEFAULT_STORAGE_VENDOR")
        if vendor_name == StorageVendor.AZURE.value:
            account = os.getenv("AZURE_STORAGE_ACCOUNT")
            container = os.getenv("AZURE_GENAI_MODELS_CONTAINER")
            if not account or not container:
                raise ValueError(
                    "Environment variables AZURE_STORAGE_ACCOUNT and AZURE_GENAI_MODELS_CONTAINER "
                    "must be set for Azure storage."
                )
            vendor_url = f"https://{account}.blob.core.windows.net/{container}"
        elif vendor_name == StorageVendor.GCP.value:
            raise NotImplementedError("GCP is not supported for genai models.")
        else:
            raise ValueError(f"Invalid storage vendor: {vendor_name}")

        return cls(vendor=StorageVendor(vendor_name), url=vendor_url)
