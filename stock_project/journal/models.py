# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class VMarketInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    symbol = models.CharField(max_length=16)
    open = models.DecimalField(max_digits=14, decimal_places=2)
    high = models.DecimalField(max_digits=14, decimal_places=2)
    low = models.DecimalField(max_digits=14, decimal_places=2)
    close = models.DecimalField(max_digits=14, decimal_places=2)
    volume = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'v_market_info'
    
    def __str__(self) -> str:
        return "Date: " + self.date.strftime("%m/%d/%Y") + " of a: " + self.symbol


class VTransactions(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    symbol = models.CharField(max_length=20)
    buy_quantity = models.IntegerField()
    buy_price = models.DecimalField(max_digits=14, decimal_places=2)
    buy_total_price = models.DecimalField(max_digits=14, decimal_places=2)
    sell_quantity = models.IntegerField()
    sell_price = models.DecimalField(max_digits=14, decimal_places=2)
    sell_total_price = models.DecimalField(max_digits=14, decimal_places=2)
    trade_result = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'v_transactions'

    def __str__(self) -> str:
        return "Date: " + self.date.strftime("%m/%d/%Y") + " of a: " + self.symbol + f". Result : {self.trade_result:.2%}"