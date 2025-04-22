from django.core.management.base import BaseCommand, CommandError
from artd_siigo.utils.siigo_api_util import SiigoApiUtil
from artd_siigo.utils.siigo_db_util import SiigoDbUtil
from artd_partner.models import Partner
import time


class Command(BaseCommand):
    help = "Imports products from Siigo for a specified partner"

    def add_arguments(self, parser):
        # Define 'partner_slug' argument as required
        parser.add_argument(
            "partner_slug",
            type=str,
            help="The slug for the partner whose products lists need to be imported",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Importing producs from Siigo..."))
        partner_slug = options["partner_slug"]

        # Validate partner existence
        try:
            partner = Partner.objects.get(partner_slug=partner_slug)
        except Partner.DoesNotExist:
            raise CommandError(f"Partner with slug '{partner_slug}' does not exist")

        try:
            siigo_api = SiigoApiUtil(partner)
            siigo_db = SiigoDbUtil(partner)
            products = siigo_api.get_all_products(partner=partner)
            total_products = len(products)
            self.stdout.write(
                self.style.SUCCESS(
                    f"### Products imported successfully ### {total_products} products"
                )
            )
            processed_products = 0
            time.sleep(5)
            for product in products:
                name = product.get("name", "")
                siigo_db.insert_product_in_db(product)
                processed_products += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Product {processed_products} of {total_products} '{name}' processed successfully"
                    )
                )

        except Exception as e:
            raise CommandError(f"Error importing products: {e}")
