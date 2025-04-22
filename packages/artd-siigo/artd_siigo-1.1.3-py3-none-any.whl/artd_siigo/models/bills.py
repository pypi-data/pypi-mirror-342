from artd_partner.models import Partner
from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_siigo.models.catalogs import SiigoDocumentType
from artd_siigo.models.base_models import BaseModel
from artd_order.models import Order

ARTD_DOCUMENT_TYPE = (
    ("order", _("Order")),
    ("credit_note", _("Credit Note")),
    ("debit_note", _("Debit Note")),
)


class BillType(BaseModel):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        verbose_name=_("Partner"),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
    )
    code = models.CharField(
        max_length=100,
        verbose_name=_("Code"),
    )

    class Meta:
        verbose_name = _("Bill Type")
        verbose_name_plural = _("Bill Types")
        unique_together = ("partner", "code")

    def __str__(self):
        return f"{self.name} {self.partner.name}"


class BillConfig(BaseModel):
    partner = models.OneToOneField(
        Partner,
        on_delete=models.CASCADE,
        verbose_name=_("Partner"),
    )
    siigo_document_type = models.ForeignKey(
        SiigoDocumentType,
        on_delete=models.PROTECT,
        verbose_name=_("Siigo Document Type"),
    )
    bill_type = models.ForeignKey(
        BillType,
        on_delete=models.PROTECT,
        verbose_name=_("Bill Type"),
    )
    generate_electronic_document = models.BooleanField(
        default=False,
        verbose_name=_("Generate Electronic Document"),
    )
    artd_document_type = models.CharField(
        max_length=100,
        choices=ARTD_DOCUMENT_TYPE,
        verbose_name=_("Document Type"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Bill Config")
        verbose_name_plural = _("Bill Configs")
        unique_together = ("partner", "artd_document_type")

    def __str__(self):
        return f"{self.partner.name} {self.siigo_document_type.name}"


class SiigoInvoice(BaseModel):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        verbose_name=_("Partner"),
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
        null=True,
        blank=True,
    )
    siigo_id = models.CharField(
        max_length=100,
        verbose_name=_("Siigo ID"),
        blank=True,
        null=True,
    )
    number = models.PositiveIntegerField(
        verbose_name=_("Number"),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        blank=True,
        null=True,
    )
    date = models.DateField(
        verbose_name=_("Date"),
        blank=True,
        null=True,
    )
    customer = models.JSONField(
        verbose_name=_("Customer"),
        blank=True,
        null=True,
        default=dict,
    )
    cost_center = models.PositiveIntegerField(
        verbose_name=_("Cost Center"),
        blank=True,
        null=True,
    )
    currency = models.JSONField(
        verbose_name=_("Currency"),
        default=dict,
        blank=True,
        null=True,
    )
    total = models.FloatField(
        verbose_name=_("Total"),
        blank=True,
        null=True,
    )
    balance = models.FloatField(
        verbose_name=_("Balance"),
        blank=True,
        null=True,
    )
    seller = models.PositiveIntegerField(
        verbose_name=_("Seller"),
        blank=True,
        null=True,
    )
    stamp = models.JSONField(
        verbose_name=_("Stamp"),
        default=dict,
        blank=True,
        null=True,
    )
    mail = models.JSONField(
        verbose_name=_("Mail"),
        default=dict,
        blank=True,
        null=True,
    )
    observations = models.TextField(
        verbose_name=_("Observations"),
        blank=True,
        null=True,
    )
    items = models.JSONField(
        verbose_name=_("Items"),
        default=dict,
        blank=True,
        null=True,
    )
    payments = models.JSONField(
        verbose_name=_("Payments"),
        default=dict,
        blank=True,
        null=True,
    )
    public_url = models.TextField(
        verbose_name=_("Public URL"),
        blank=True,
        null=True,
    )
    global_discounts = models.JSONField(
        verbose_name=_("Global Discounts"),
        default=dict,
        blank=True,
        null=True,
    )
    additional_fields = models.JSONField(
        verbose_name=_("Additional Fields"),
        default=dict,
        blank=True,
        null=True,
    )
    metadata = models.JSONField(
        verbose_name=_("Metadata"),
        default=dict,
        blank=True,
        null=True,
    )
    json_data = models.JSONField(
        verbose_name=_("JSON Data"),
        default=dict,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Siigo Invoice")
        verbose_name_plural = _("Siigo Invoices")

    def __str__(self):
        return f"{self.partner.name} {self.siigo_id}"


class SiigoOrderInvoice(BaseModel):
    """Model definition for Siigo Order Proxy."""

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
    )
    invoice = models.OneToOneField(
        SiigoInvoice,
        on_delete=models.CASCADE,
        verbose_name=_("Invoice"),
        null=True,
        blank=True,
    )
    proccessed = models.BooleanField(
        default=False,
        verbose_name=_("Proccessed"),
    )
    messages = models.JSONField(
        verbose_name=_("Messages"),
        default=dict,
        blank=True,
        null=True,
    )
    json_data = models.JSONField(
        verbose_name=_("JSON Data"),
        default=dict,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Siigo Order Proxy."""

        verbose_name = _("Siigo Order Invoice")
        verbose_name_plural = _("Siigo Order Invoice")

    def __str__(self):
        """Unicode representation of Siigo Order Proxy."""
        if not self.invoice:
            return f"{self.order.increment_id} No Invoice"
        return f"{self.order.increment_id} {self.invoice.siigo_id}"
