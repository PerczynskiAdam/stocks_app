from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Avg

from .models import Transactions, Balance, Positions, StockTrade

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


def detail(request, id):


    transaction = get_object_or_404(Transactions, pk=id)
    context = {
        'transactions': transaction
    }
    return render(request, 'journal/detail.html', context)