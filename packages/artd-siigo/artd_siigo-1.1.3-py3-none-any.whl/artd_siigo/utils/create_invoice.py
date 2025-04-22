from artd_partner.models import Partner
from artd_product.models import Product
from artd_order.models import Order, OrderProduct
from artd_siigo.models import (
    PartnerSiigoConfiguration,
    BillConfig,
    SiigoCustomer,
    UserMapping,
    PaymentMethodMapping,
    SiigoProduct,
)
from datetime import datetime
from artd_siigo.utils.create_bill_from_order import get_or_create_customer
from artd_siigo.utils.siigo_api_util import SiigoApiUtil


def create_invoice_from_order(order: Order):
    result_messages = []
    partner: Partner = order.partner
    partner_siigo_configuration = PartnerSiigoConfiguration.objects.filter(
        partner=partner
    ).last()
    if not partner_siigo_configuration:
        result_messages.append(
            f"No SIIGO configuration was found for the partner {partner.name}"
        )
        return result_messages, {}

    if not partner_siigo_configuration.export_invoices_to_siigo:
        result_messages.append(
            f"Export to SIIGO is disabled for the partner {partner.name}"
        )
        return result_messages, {}
    if not partner_siigo_configuration.export_customers_to_siigo:
        result_messages.append(
            f"Export to SIIGO is disabled for the partner {partner.name}"
        )
        return result_messages, {}
    if not partner_siigo_configuration.export_products_to_siigo:
        result_messages.append(
            f"Export to SIIGO is disabled for the partner {partner.name}"
        )
    if not partner_siigo_configuration.import_customers_from_siigo:
        result_messages.append(
            f"Import from SIIGO is disabled for the partner {partner.name}"
        )
        return result_messages, {}
    if not partner_siigo_configuration.import_products_from_siigo:
        result_messages.append(
            f"Import from SIIGO is disabled for the partner {partner.name}"
        )

    bill_config = BillConfig.objects.filter(
        partner=partner,
        artd_document_type="order",
    ).last()

    if not bill_config:
        result_messages.append(
            f"No bill configuration was found for the partner {partner.name}"
        )
        return result_messages, {}
    else:
        document = {"id": bill_config.siigo_document_type.siigo_id}

    date = datetime.now().strftime("%Y-%m-%d")

    get_or_create_customer(customer=order.customer)
    customer = order.customer
    if not customer:
        result_messages.append(f"No customer was found for the order {order.id}")
        return result_messages, {}
    else:
        siigo_customer = SiigoCustomer.objects.filter(
            customer=customer,
        ).last()
        if not siigo_customer:
            result_messages.append(
                f"No SIIGO customer was found for the customer {customer.name} ID:{customer.id}"
            )
            return result_messages, {}
        else:
            if not siigo_customer.identification:
                result_messages.append(
                    f"No identification was found for the SIIGO customer {siigo_customer.name} ID:{siigo_customer.id}"
                )
                return result_messages, {}
            else:
                if not customer.document:
                    result_messages.append(
                        f"No document was found for the customer {customer.name} ID: {customer.id}"
                    )
                    return result_messages, {}
                customer = {
                    "identification": siigo_customer.identification,
                }

    seller = order.created_by
    if not seller:
        result_messages.append(f"No seller was found for the order {order.id}")
        return result_messages, {}
    else:
        siigo_mapped_user = UserMapping.objects.filter(
            user=seller,
        ).last()
        if not siigo_mapped_user:
            result_messages.append(
                f"No SIIGO customer was found for the seller {seller.name}"
            )
            return result_messages, {}
        else:
            siigo_user = siigo_mapped_user.siigo_user
            if not siigo_user:
                result_messages.append(
                    f"No SIIGO user was found for the seller {seller.name}"
                )
                return result_messages, {}
            else:
                seller_id = siigo_user.siigo_id

    order_payment_method = order.order_payment_method
    if not order_payment_method:
        result_messages.append(
            f"No payment method was found for the order with ID {order.id}"
        )
        return result_messages, {}
    else:
        payment_method_mapping = PaymentMethodMapping.objects.filter(
            order_payment_method=order_payment_method,
        ).last()
        if not payment_method_mapping:
            result_messages.append(
                f"No SIIGO payment method was found for the order payment method {order_payment_method.name}"
            )
            return result_messages, {}
        else:
            payment_type = payment_method_mapping.siigo_payment_type

    products = order.orderproduct_set.all()
    if products.count() == 0:
        result_messages.append(f"No products were found for the order {order.number}")
        return result_messages, {}
    else:
        items = []
        for product in products:
            order_product: OrderProduct = product
            product: Product = order_product.product
            if not SiigoProduct.objects.filter(product=product).exists():
                product.save()
            siigo_product = SiigoProduct.objects.filter(product=product).last()
            siigo_product_json_data = siigo_product.json_data
            taxes = []
            if "taxes" in siigo_product_json_data:
                for tax in siigo_product_json_data["taxes"]:
                    taxes.append(
                        {
                            "id": tax["id"],
                        }
                    )

            items.append(
                {
                    "code": siigo_product.code,
                    "description": siigo_product.name,
                    "quantity": order_product.quantity,
                    "taxes": taxes,
                    "taxed_price": float(order_product.base_total),
                }
            )

    invoice_data = {
        "document": document,
        "customer": customer,
        "date": date,
        "seller": seller_id,
        "items": items,
        "payments": [
            {
                "id": payment_type.siigo_id,
                "value": float(order.total_paid),
                "due_date": order.created_at.strftime("%Y-%m-%d"),
            }
        ],
    }
    siigo_api_util = SiigoApiUtil(order.partner)
    response = siigo_api_util.create_invoice(invoice_data)
    return result_messages, response
