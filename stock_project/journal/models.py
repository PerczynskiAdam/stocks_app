# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class VMarketInfo(models.Model):
#     id = models.IntegerField(primary_key=True)
#     date = models.DateField(blank=True, null=True)
#     symbol = models.CharField(max_length=16)
#     open = models.DecimalField(max_digits=14, decimal_places=2)
#     high = models.DecimalField(max_digits=14, decimal_places=2)
#     low = models.DecimalField(max_digits=14, decimal_places=2)
#     close = models.DecimalField(max_digits=14, decimal_places=2)
#     volume = models.DecimalField(max_digits=14, decimal_places=2)

#     class Meta:
#         managed = False  # Created from a view. Don't remove.
#         db_table = 'v_market_info'
    
#     def __str__(self) -> str:
#         return "Date: " + self.date.strftime("%m/%d/%Y") + " of a: " + self.symbol


class Transactions(models.Model):
    id = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=20)
    # position = models.IntegerField()
    # type = models.CharField(max_length=20)
    # quantity = models.IntegerField()
    open_time = models.DateTimeField()
    # open_price = models.DecimalField(max_digits=14, decimal_places=2)
    # close_time = models.DateTimeField()
    # close_price = models.DecimalField(max_digits=14, decimal_places=2)
    # profit = models.DecimalField(max_digits=14, decimal_places=2)
    # net_profit = models.DecimalField(max_digits=14, decimal_places=2)
    pct_net_profit = models.DecimalField(max_digits=14, decimal_places=2)
    # rollover = models.DecimalField(max_digits=14, decimal_places=2)
    # comment = models.CharField(max_length=100)

    class Meta:
        db_table = 'journal_transactions'

    def __str__(self) -> str:
        return "Date: " + self.open_time.strftime("%m/%d/%Y") + " of a: " + self.symbol + f". Result :" + str(self.pct_net_profit)


class Balance(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    balance = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = 'journal_balance'

    def __str__(self) -> str:
        # return "Balance: " + "{:.2f}".format(self.balance) + " on: " + self.date.strftime("%m/%d/%Y")
        return "Balance: " + str(self.balance) + " on: " + self.date.strftime("%m/%d/%Y")


class Positions(models.Model):
    id = models.IntegerField(primary_key=True)
    balance = models.ForeignKey(Balance, on_delete=models.DO_NOTHING, null=True, blank=True)
    symbol = models.CharField(max_length=20)
    open_date = models.DateField()
    open_time = models.TimeField()
    open_price = models.DecimalField(max_digits=14, decimal_places=2)
    close_price = models.DecimalField(max_digits=14, decimal_places=2)
    net_profit = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = 'journal_positions'
    
    def __str__(self) -> str:
        return "Date: " + self.open_date.strftime("%m/%d/%Y") + " of a: " + self.symbol + f". Result :" + "{:.2f}".format(self.net_profit)

    @property
    def pctNetProfitPos(self):
        pct_net_profit = self.net_profit / self.close_price * 100
        return pct_net_profit
    
    @property
    def pctPosSize(self):
        pct_pos_size = self.open_price / self.balance.balance * 100
        return pct_pos_size
    
    @property
    def pctNetProfitBalance(self):
        pct_net_profit = self.net_profit / self.balance.balance * 100
        return pct_net_profit

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
class StockTrade(models.Model):
    id = models.IntegerField(primary_key=True)
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    ticker = models.CharField(max_length=5)
    exchange = models.CharField(max_length=10)
    date = models.DateField()
    buy_point = models.DecimalField(max_digits=14, decimal_places=2)
    stop_loss = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    # image = models.ImageField()

    class Meta:
        db_table = 'journal_stocktrade'
        ordering = ['date', 'ticker']

    def stockTags(self):
        return self.tag_set.all()

    def __str__(self) -> str:
        return "Date: " + self.date.strftime("%m/%d/%Y") + " of a: " + self.ticker + ":" + self.exchange + str(self.tags.name)