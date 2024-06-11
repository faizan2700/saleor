"""Clear the database preserving shop's configuration.

This command clears the database from data such as orders, products or customer
accounts. It doesn't remove shop's configuration, such as: staff accounts, service
accounts, plugin configurations, site settings or navigation menus.
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from ....account.models import User
from ....attribute.models import Attribute
from ....checkout.models import Checkout
from ....discount.models import Promotion, Voucher
from ....giftcard.models import GiftCard
from ....order.models import Order
from ....page.models import Page, PageType
from ....payment.models import Payment, Transaction, TransactionItem
from ....product.models import Category, Collection, Product, ProductType
from ....shipping.models import ShippingMethod, ShippingZone
from ....warehouse.models import Warehouse
from ....webhook.models import Webhook


class Command(BaseCommand):
    help = "Removes data from the database preserving shop configuration."

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete-staff",
            action="store_true",
            help="Delete staff user accounts (doesn't delete superuser accounts).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Allows running the cleardb command in DEBUG=False mode.",
        )

    def handle(self, **options):
        force = options.get("force", False)
        if not settings.DEBUG and not force:
            raise CommandError("Cannot clear the database in DEBUG=False mode.")

        count_checkout_objs = Checkout.objects.all().count() 
        Checkout.objects.all().delete()
        self.stdout.write(f"Removed checkouts, total: {count_checkout_objs}")

        transaction_item_objs = TransactionItem.objects.all().count() 
        TransactionItem.objects.all().delete()
        self.stdout.write(f"Removed transaction items, total: {transaction_item_objs}")

        transaction_objs = Transaction.objects.all().count() 
        Transaction.objects.all().delete()
        self.stdout.write(f"Removed transactions, total: {transaction_objs}")

        payment_objs = Payment.objects.all().count() 
        Payment.objects.all().delete()
        self.stdout.write(f"Removed payments, total: {payment_objs}")

        order_objs = Order.objects.all().count() 
        Order.objects.all().delete()
        self.stdout.write(f"Removed orders, total: {order_objs}")
        
        product_objs = Product.objects.all().count() 
        Product.objects.all().delete()
        self.stdout.write(f"Removed products, total: {product_objs}")

        product_type_objs = ProductType.objects.all().count() 
        ProductType.objects.all().delete()
        self.stdout.write(f"Removed product types, total: {product_type_objs}")

        attribute_objs = Attribute.objects.all().count() 
        Attribute.objects.all().delete()
        self.stdout.write(f"Removed attributes, total: {attribute_objs}")

        category_objs = Category.objects.all().count() 
        Category.objects.all().delete()
        self.stdout.write(f"Removed categories, total: {category_objs}")

        collection_objs = Collection.objects.all().count() 
        Collection.objects.all().delete()
        self.stdout.write(f"Removed collections, total: {collection_objs}")

        promotion_objs = Promotion.objects.all().count() 
        Promotion.objects.all().delete()
        self.stdout.write(f"Removed promotions, total: {promotion_objs}")

        shipping_method_objs = ShippingMethod.objects.all().count() 
        ShippingMethod.objects.all().delete()
        self.stdout.write(f"Removed shipping methods, total: {shipping_method_objs}")

        shipping_zone_objs = ShippingZone.objects.all().count() 
        ShippingZone.objects.all().delete()
        self.stdout.write(f"Removed shipping zones, total: {shipping_zone_objs}")

        voucher_objs = Voucher.objects.all().count() 
        Voucher.objects.all().delete()
        self.stdout.write(f"Removed vouchers, total: {voucher_objs}")

        giftcard_objs = GiftCard.objects.all().count() 
        GiftCard.objects.all().delete()
        self.stdout.write(f"Removed gift cards, total: {giftcard_objs}")

        warehouse_objs = Warehouse.objects.all().count() 
        self.stdout.write(f"Removed warehouses, total: {warehouse_objs}")
        Warehouse.objects.all().delete()

        page_objs = Page.objects.all().count() 
        Page.objects.all().delete()
        self.stdout.write(f"Removed pages, total: {page_objs}")

        page_type_objs = PageType.objects.all().count() 
        PageType.objects.all().delete()
        self.stdout.write(f"Removed page types, total: {page_type_objs}")

        webhook_objs = Webhook.objects.all().count() 
        Webhook.objects.all().delete()
        self.stdout.write(f"Removed webhooks, total: {webhook_objs}")

        
        staff = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        qs = User.objects.exclude(pk__in=staff)
        non_staff_users = qs.count() 
        qs.delete() 
        self.stdout.write(f"Removed customers, total: {non_staff_users}")

        should_delete_staff = options.get("delete_staff")
        if should_delete_staff:
            staff = staff.exclude(is_superuser=True) 
            staff_users = staff.count() 
            staff.delete()
            self.stdout.write(f"Removed staff users, total: {staff_users}")

        # Remove addresses of staff members. Used to clear saved addresses of staff
        # accounts used on demo for testing checkout.
        addresses = 0 
        for user in staff:
            addresses += user.addresses.all().count() 
            user.addresses.all().delete()
        self.stdout.write(f"Removed staff addresses, total: {addresses}")
