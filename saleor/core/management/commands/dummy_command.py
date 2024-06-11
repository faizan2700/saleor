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
    help = "Checks if command works."

    def handle(self, **options):
        self.stdout.write("Checking command.") 