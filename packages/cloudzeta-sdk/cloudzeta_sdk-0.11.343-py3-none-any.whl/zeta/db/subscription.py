from dataclasses import dataclass, field
from enum import Enum

from zeta.db import BaseData, ZetaBase
from zeta.utils.logging import zetaLogger


class SubscriptionTier(Enum):
    FREE = "free"
    ESSENTIAL = "essential"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"


CreditLookup = {
    SubscriptionTier.FREE: 1000,
    SubscriptionTier.ESSENTIAL: 20 * 1000,
    SubscriptionTier.PRO: 50 * 1000,
    SubscriptionTier.ENTERPRISE: 1000 * 1000,
    SubscriptionTier.ADMIN: 1000 * 1000,
}


AllowedTierTransitions = {
    SubscriptionTier.FREE: [SubscriptionTier.ESSENTIAL, SubscriptionTier.PRO],
    SubscriptionTier.ESSENTIAL: [SubscriptionTier.ESSENTIAL, SubscriptionTier.PRO],
    SubscriptionTier.PRO: [SubscriptionTier.PRO],
    SubscriptionTier.ENTERPRISE: [],
    SubscriptionTier.ADMIN: [],
}

AllowedPriceKeyUpgrades = {
    "zeta-essential-monthly": ["zeta-essential-yearly", "zeta-pro-monthly", "zeta-pro-yearly"],
    "zeta-essential-yearly": ["zeta-pro-yearly"],
    "zeta-pro-monthly": ["zeta-pro-yearly"],
    "zeta-pro-yearly": [],
}

AllowedPriceKeyDowngrades = {
    "zeta-essential-monthly": [],
    "zeta-essential-yearly": ["zeta-essential-monthly"],
    "zeta-pro-monthly": ["zeta-essential-monthly", "zeta-essential-yearly"],
    "zeta-pro-yearly": ["zeta-essential-monthly", "zeta-essential-yearly", "zeta-pro-monthly"],
}

@dataclass
class ZetaSubscriptionData(BaseData):
    tier: SubscriptionTier
    credits: int
    stripeCustomerId: str = None
    stripeSubscriptionIds: list[str] = field(default_factory=list)
    stripePriceKey: str = None
    creditsRefreshAt: str = None

class ZetaSubscription(ZetaBase):
    @property
    def collection_name(cls) -> str:
        return "subscriptions"

    @property
    def data_class(self):
        return ZetaSubscriptionData

    @property
    def is_paying(self) -> bool:
        return self.valid and self._data.stripePriceKey is not None

    def _data_from_dict(self, data: dict):
        super()._data_from_dict(data)

        if self._data and type(self._data.tier) == str:
            self._data.tier = SubscriptionTier(self._data.tier)

    @classmethod
    def create_default_subscription(cls, user_id: str):
        """
        Create a new default subscription for a user. The caller is responsible for
        checking if the user is valid and has not already been assigned a subscription.
        """
        return cls.create({
            "uid": user_id,
            "tier": SubscriptionTier.FREE.value,
            "credits": 1000,
            "stripeCustomerId": None,
            "stripeSubscriptionIds": [],
            "stripePriceKey": None,
            "creditsRefreshAt": None,
        })

    def append_stripe_subscription_id(self, stripe_subscription_id: str):
        assert self._db, "Supabase is not initialized"

        self._db.schema("public").rpc("append_stripe_subscription_id", {
            "subscription_uid": self.uid,
            "stripe_subscription_id": stripe_subscription_id,
        }).execute()

    def consume_credits_automatically(self, amount: int) -> bool:
        """
        Consume credits automatically from the subscription.

        Returns True if the credits were consumed successfully, False otherwise.
        """
        assert self._db, "Supabase is not initialized"

        if self.data.credits < amount:
            zetaLogger.error(f"Insufficient credits: {self.data.credits} < {amount}")
            return False

        try:
            query = self.table.update({
                "credits": self.data.credits - amount,
            }).eq("uid", self.uid)
            query = query.eq("credits", self.data.credits)
            update_res = query.execute()

            if update_res.data and len(update_res.data) > 0:
                self._data.credits = update_res.data[0]["credits"]
                return True
            else:
                zetaLogger.error(f"Failed to consume credits automatically: {self.uid}, "
                                 f"result: {update_res}")
                return False
        except Exception as e:
            zetaLogger.error(f"Failed to consume credits automatically: {e}")
            return False

    @classmethod
    def get_by_stripe_customer_id(cls, stripe_customer_id: str):
        assert cls._db, "Supabase is not initialized"

        thiz = cls()
        query_res = thiz.table.select("*").eq("stripe_customer_id", stripe_customer_id).execute().data
        if len(query_res) == 0:
            zetaLogger.error(f"document not found for stripe_customer_id: {stripe_customer_id}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for stripe_customer_id: {stripe_customer_id}")
        else:
            thiz._uid = query_res[0]["uid"]
            thiz._data_from_dict(query_res[0])

        return thiz
