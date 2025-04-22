from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import re

from zeta.db import BaseData, ZetaBase
from zeta.utils.logging import zetaLogger
from zeta.storage.utils import StorageConfig, StorageVendor


class ZetaUserRole(Enum):
    NONE = None
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"

class ZetaAddons(Enum):
    NONE = None
    GENERATOR = "generator"

@dataclass
class ZetaUserData(BaseData):
    displayName: str
    email: str
    photoURL: str
    addons: list[str] = field(default_factory=list)
    # TODO: remove default value once all users are backfilled.
    storage: StorageConfig = None


class ZetaUser(ZetaBase):
    @property
    def collection_name(cls) -> str:
        return "users"

    @property
    def data_class(self):
        return ZetaUserData

    @classmethod
    def get_by_email(cls, email: str) -> ZetaUser:
        thiz = cls()

        query_res = thiz.table.select("*").eq("email", email).execute().data
        if len(query_res) == 0:
            zetaLogger.error(f"document not found for email: {email}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for email: {email}")
        else:
            thiz._uid = query_res[0]["uid"]
            thiz._data_from_dict(query_res[0])

        return thiz

    @property
    def storage(self) -> StorageConfig:
        storage_data = self._data.storage
        storage = None

        if storage_data and storage_data.get("vendor") and storage_data.get("url"):
            storage = StorageConfig(**self._data.storage)
            storage.vendor = StorageVendor(storage.vendor)
        else:
            storage = StorageConfig.create_default()
        return storage

    def get_gcp_bucket_name(self) -> str:
        # TODO: Support other storage vendors
        assert self.storage is not None
        assert self.storage.vendor == StorageVendor.GCP, "Only GCP is supported"

        bucket_name_match = re.match(r"gs://([^/]+)$", self.storage.url)
        assert bucket_name_match is not None, "Invalid bucket URL"

        return bucket_name_match.group(1)

    # Disable creating a new user
    #   Unlike ZetaBase, uid must be provided for ZetaUser (i.e. we cannot create a new user).
    #   In reality, the ZetaUser class must be created after user sign up and the UID comes
    #   from the authentication service.
    def _create(self, data) -> bool:
        raise NotImplementedError