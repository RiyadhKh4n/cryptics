from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Portfolio, Asset
from django.contrib.auth.models import User
from .forms import PortfolioForm, AddAsset, BuyAsset
from coin.views import *


def get_portfolio_list(request):
    portfolios = Portfolio.objects.filter(user=request.user)
    context = {
        'portfolios': portfolios
    }
    return render(request, 'portfolio/portfolio.html', context)


def create_portfolio(request):
    form = PortfolioForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.slug = form['name'].value()
        obj.USDvalue = 0.00
        obj.save()
        return redirect('get_portfolio_list')

    context = {'form': form}
    return render(request, 'portfolio/create_portfolio.html', context)


def edit_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('get_portfolio_list')
    form = PortfolioForm(instance=portfolio)
    context = {
        'form': form
    }
    return render(request, 'portfolio/edit_portfolio.html', context)


def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    portfolio.delete()
    return redirect('get_portfolio_list')


def get_asset_list(request, portfolio_id):
    assets = Asset.objects.filter(portfolio_name=portfolio_id)
    context = {
        'assets': assets,
        'portfolio_id': portfolio_id,
    }
    return render(request, 'portfolio/assets.html', context)


def add_asset(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    form = AddAsset()
    if request.method == "POST":
        form = AddAsset(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.PnL = 0.00
            obj.USDEarned = 0.00
            obj.portfolio_name = portfolio
            quantity = form['quantity'].value()
            AP = form['AveragePrice'].value()
            obj.AveragePrice = AP
            # coinID = form['coinID'].value()
            # price = get_coin_price(coinID)
            USDspent = (int(quantity) * float(AP))
            obj.USDSpent = USDspent
            obj.CurrentInvestment = USDspent
            obj.save()
            return redirect(reverse('get_asset_list', args=[portfolio_id]))

    context = {'form': form}
    return render(request, 'portfolio/add_asset.html', context)


def get_single_asset(request, asset_id, portfolio_id):
    asset = Asset.objects.filter(pk=asset_id)
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    # coin = Asset.objects.get(coinID=coin_id)

    form = BuyAsset()
    if request.method == "POST":
        form = BuyAsset(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.PnL = 0.00
            obj.USDEarned = 0.00
            obj.portfolio_name = portfolio
            quantity = form['quantity'].value()
            AP = form['AveragePrice'].value()
            USDspent = (int(quantity) * float(AP))
            obj.USDSpent = USDspent
            # obj.coinID = coin
            # investment = form.cleaned_data.get("CurrentInvestment")
            obj.CurrentInvestment = USDspent
            obj.save()
            return redirect(reverse('get_asset_list', args=[portfolio_id]))

    context = {
        'assets': asset,
        'asset_id': asset_id,
        'form': form
    }

    return render(request, 'portfolio/buy_sell_asset.html', context)
