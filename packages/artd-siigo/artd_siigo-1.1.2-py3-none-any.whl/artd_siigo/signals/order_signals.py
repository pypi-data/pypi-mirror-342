from django.db.models.signals import post_save
from django.dispatch import receiver
from artd_siigo.models import SiigoOrderInvoice, SiigoInvoice

from artd_order.models import Order
from artd_siigo.utils.create_invoice import create_invoice_from_order
from datetime import datetime


@receiver(post_save, sender=SiigoOrderInvoice)
def create_invoice_in_siigo(sender, instance, created, **kwargs):
    if created:
        siigo_order_invoice: SiigoOrderInvoice = instance
        order: Order = siigo_order_invoice.order
        messages, response = create_invoice_from_order(order=order)
        siigo_order_invoice.messages = messages
        siigo_order_invoice.json_data = response
        siigo_order_invoice.save()
        if response:
            if "status_code" in response:
                status_code = int(response["status_code"])
                if status_code >= 200 and status_code <= 300:
                    if "response" in response:
                        try:
                            invoice_data: dict = response["response"]
                            print(invoice_data)
                            date = datetime.strptime(
                                invoice_data["date"], "%Y-%m-%d"
                            ).date()
                            defaults = {
                                "siigo_id": invoice_data.get("id", ""),
                                "number": invoice_data.get("number", ""),
                                "name": invoice_data.get("name", ""),
                                "date": date,
                                "customer": invoice_data.get("customer", {}),
                                "cost_center": invoice_data.get("cost_center", ""),
                                "currency": invoice_data.get("currency", {}),
                                "total": invoice_data.get("total", 0),
                                "balance": invoice_data.get("balance", 0),
                                "seller": invoice_data.get("seller", None),
                                "stamp": invoice_data.get("stamp", {}),
                                "mail": invoice_data.get("mail", {}),
                                "observations": invoice_data.get("observations", ""),
                                "items": invoice_data.get("items", {}),
                                "payments": invoice_data.get("payments", {}),
                                "public_url": invoice_data.get("public_url", ""),
                                "global_discounts": invoice_data.get(
                                    "global_discounts", {}
                                ),
                                "additional_fields": invoice_data.get(
                                    "additional_fields", {}
                                ),
                                "metadata": invoice_data.get("metadata", {}),
                                "json_data": invoice_data,
                            }
                            print(f">>>defaults: {defaults}")
                            siigo_invoice, created = (
                                SiigoInvoice.objects.update_or_create(
                                    partner=order.partner,
                                    order=order,
                                    defaults=defaults,
                                )
                            )
                            print(f">>>siigo_invoice: {siigo_invoice}")
                            siigo_order_invoice.invoice = siigo_invoice
                            siigo_order_invoice.proccessed = True
                            siigo_order_invoice.save()
                        except Exception as e:
                            print(f"Error: {e}")
                            # print(response)
