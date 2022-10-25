from django.test import TestCase
from lubricentro_myc.models import ProductPriceHistory
from lubricentro_myc.models.product import Producto
from lubricentro_myc.signals import delete_invoice_item, save_invoice_item, save_product
from lubricentro_myc.tests.factories import (
    ClientFactory,
    InvoiceFactory,
    InvoiceItemFactory,
    ProductFactory,
)


class SignalsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_1 = ClientFactory()
        cls.product_1 = ProductFactory(codigo=1, stock=5.0, precio_costo=25.0)
        cls.product_2 = ProductFactory(codigo=2, stock=11.5)
        cls.invoice = InvoiceFactory(cliente=cls.client_1)

    def test_save_invoice_item_with_new_invoice_item(self):
        new_invoice_item = InvoiceItemFactory.build(
            remito=self.invoice, producto=self.product_1, cantidad=4.0
        )
        save_invoice_item(sender=None, instance=new_invoice_item)
        product = Producto.objects.get(codigo=self.product_1.codigo)
        self.assertEqual(product.stock, 1.0)

    def test_save_invoice_item_updating_invoice_item(self):
        invoice_item_1 = InvoiceItemFactory(
            remito=self.invoice, producto=self.product_1, cantidad=0.0
        )
        new_invoice_item = InvoiceItemFactory.build(
            id=invoice_item_1.id,
            remito=self.invoice,
            producto=self.product_1,
            cantidad=3.0,
        )
        save_invoice_item(sender=None, instance=new_invoice_item)
        product = Producto.objects.get(codigo=self.product_1.codigo)
        self.assertEqual(product.stock, 2.0)

    def test_delete_invoice_item(self):
        invoice_item = InvoiceItemFactory.build(
            remito=self.invoice,
            producto=self.product_1,
            cantidad=3.0,
        )
        delete_invoice_item(sender=None, instance=invoice_item)
        product = Producto.objects.get(codigo=self.product_1.codigo)
        self.assertEqual(product.stock, 8.0)

    def test_save_product(self):
        updated_product = ProductFactory.build(
            codigo=self.product_1.codigo, precio_costo=35.0
        )
        save_product(sender=None, instance=updated_product)
        product_price_history = ProductPriceHistory.objects.filter(
            product__codigo=self.product_1.codigo
        ).first()
        self.assertEqual(product_price_history.old_price, self.product_1.precio_costo)
        self.assertEqual(product_price_history.new_price, updated_product.precio_costo)
