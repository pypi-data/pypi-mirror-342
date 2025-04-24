from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _  # NoQA
from pretix.base.signals import logentry_display, register_payment_providers


@receiver(register_payment_providers, dispatch_uid="payment_worldlinedirect")
def register_payment_provider(sender, **kwargs):
    from .paymentmethods import payment_method_classes

    return payment_method_classes


@receiver(
    signal=logentry_display, dispatch_uid="payment_worldlinedirect_logentry_display"
)
def logentry_display(sender, logentry, **kwargs):
    if logentry.action_type != "pretix_worldlinedirect.worldlinedirect.event":
        return

    return _("Worldline Direct reported an event")
