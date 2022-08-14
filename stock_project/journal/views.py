from django.http.response import Http404
from django.shortcuts import redirect, render
from django.db.models import Avg

from .models import Transactions, Balance, Positions, StockTrade
from .forms import StockTradeForm

# Create your views here.
def index(request):
    template = 'journal/index.html'
    context = {}
    # Stan konta i procentowa zmiana obliczona na podstawie Balance
    init_acc_balance = Balance.objects.order_by('date')[0]
    acc_balance = Balance.objects.order_by('-date')[0]
    context['acc_balance'] = acc_balance
    context['profit'] = "{:.2%}".format((acc_balance.balance - init_acc_balance.balance) / init_acc_balance.balance)

    # maksymalny zysk i strata
    max_profit = Positions.objects.order_by('-net_profit')[0]
    context['max_profit'] = max_profit

    max_loss = Positions.objects.order_by('net_profit')[0]
    context['max_loss'] = max_loss

    # Średnia strata - ocena podejmowanego ryzyka przy zawieraniu transakcji
    avg_loss = Transactions.objects.filter(pct_net_profit__lt=0).aggregate(avg_loss=Avg('pct_net_profit'))
    context['avg_loss'] = avg_loss

    # zaplanowane transkacje
    stock_trades = StockTrade.objects.all()
    context['stock_trades'] = stock_trades

    return render(request, template, context)


def create_trade(request):
    template = 'journal/create_trade.html'
    context = {}

    form = StockTradeForm()

    if request.method == 'POST':
        form = StockTradeForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('index')

    context['form']= form
    return render(request, template, context)


def update_trade(request, pk):
    trade = StockTrade.objects.get(id=pk)

    template = 'journal/create_trade.html'
    context = {}

    form = StockTradeForm(instance=trade)

    if request.method == 'POST':
        # zamiast dodawać znowu instancje to ją nadpisuje
        form = StockTradeForm(request.POST, instance=trade)

        if form.is_valid():
            form.save()

            return redirect('index')

    context['form']= form
    return render(request, template, context)


def display_trade(request, pk):
    template = 'journal/trade.html'
    context = {}

    trade = StockTrade.objects.get(id=pk)
    context['trade'] = trade
    return render(request, template, context)
