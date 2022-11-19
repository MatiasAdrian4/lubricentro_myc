from django.db import models


class ProductPriceHistory(models.Model):
    product = models.ForeignKey("lubricentro_myc.Producto", on_delete=models.CASCADE)
    old_price = models.FloatField()
    new_price = models.FloatField()
    timestamp = models.DateTimeField()

    @property
    def data(self):
        return (
            self.id,
            self.product.codigo,
            self.old_price,
            self.new_price,
            self.timestamp,
        )
