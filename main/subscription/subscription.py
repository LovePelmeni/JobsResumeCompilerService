import pydantic

class SubscriptionModel(pydantic.BaseModel):
    pass



class JobResumeSubscription(object):

    """
    / * Class Represents Subscription for Private Premuim Resume Themes.
    """
    def apply(self, subscription_info: SubscriptionModel):
        pass

    def unapply(self, subscription_id: int):
        pass