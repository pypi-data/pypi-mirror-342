from dataclasses import asdict
import json

from zeta.db.auth_token import ZetaAuthTokenData
from zeta.db.subscription import SubscriptionTier
from zeta.db.user import ZetaUserData


class ZetaJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ZetaUserData):
            return asdict(obj)
        elif isinstance(obj, ZetaAuthTokenData):
            return asdict(obj)
        elif isinstance(obj, SubscriptionTier):
            return obj.value
        return super().default(obj)