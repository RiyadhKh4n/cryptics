import json
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from .models import Portfolio, Asset
from .forms import PortfolioForm, AddAsset, UpdateAsset
import logging
logr = logging.getLogger(__name__)


tickerList = []
global coins
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

params = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}

headers = {
    'X-CMC_PRO_API_KEY': settings.APIKEY,
    'Accepts': 'application/json'
}

session = Session()
session.headers.update(headers)


def call_api():
    try:
        response = session.get(URL, params=params)
        data = json.loads(response.text)
        coins = data['data']
        get_ticker_list(data)

        return coins

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def get_ticker_list(data):
    for d in data['data']:
        ticker_from_api = d['symbol']
        if ticker_from_api not in tickerList:
            tickerList.append(ticker_from_api)


def get_coin_price(ticker, coins):
    """
    Will get the price of a coin
    """
    if ticker in tickerList:
        for x in coins:
            if x['symbol'] == ticker:
                price = float((x['quote']['USD']['price']))
        return price


def validate_ticker(ticker):
    """
    Will validate if the users ticker exits in tickerList
    """
    for x in tickerList:
        if ticker in tickerList:
            print("Valid ticker")
            return True

        else:
            print("Invalid ticker")
            return False


def get_portfolio_list(request):
    portfolios = Portfolio.objects.filter(user=request.user)

    portfolio_balance_list = []

    for i in portfolios:
        portfolio_id = i.id

        assets = Asset.objects.filter(portfolio_name=portfolio_id)
        curr_holdings = assets.values_list('current_holdings', flat=True)

        total_balance = 0
        for index, value in enumerate(curr_holdings):
            total_balance = total_balance + value

        portfolio_balance_list.append(float(total_balance))
            
    zipped_assets = zip(portfolios, portfolio_balance_list)
    zipped_context = tuple(zipped_assets)

    total_portfolio_balance = 0.00

    for index, value in enumerate(portfolio_balance_list):
        total_portfolio_balance = total_portfolio_balance + value

    context = {
        'portfolios': zipped_context,
        'TPB': total_portfolio_balance
    }
    return render(request, 'portfolio/portfolio.html', context)


def create_portfolio(request):
    form = PortfolioForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.slug = form['name'].value()
        obj.usd_value = 0.00
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
    returnedCoin = call_api()
    assets = Asset.objects.filter(portfolio_name=portfolio_id)
    
    portfolio_assets = assets.values_list('ticker', flat=True)

    asset_prices = []
    for i in portfolio_assets:
        current_asset_price = get_coin_price(i, returnedCoin)
        rounded_price = round(current_asset_price, 3)
        asset_prices.append(rounded_price)

    quantity = assets.values_list('quantity', flat=True)

    current_holdings = []
    for index, value in enumerate(quantity):
        new_holdings = float(quantity[index]) * asset_prices[index]
        rounded_holdings = round(new_holdings, 3)
        current_holdings.append(rounded_holdings)

    zipped_assets = zip(assets, asset_prices, current_holdings)
    zipped_context = tuple(zipped_assets)

    context = {
        'assets': zipped_context,
        'portfolio_id': portfolio_id,
    }
    return render(request, 'portfolio/assets.html', context)


def get_asset(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    returnedCoin = call_api()

    if request.method == "POST":
        coin = request.POST.get("ticker").upper()
        valid = validate_ticker(coin)

        if valid:
            price = get_coin_price(coin, returnedCoin)
            return redirect(add_asset, portfolio.id, coin, price)

        else:
            messages.success(request, f"{coin} does not exist!")

    context = {
        'tickerList': tickerList,
        'portfolio': portfolio,
    }
    return render(request, 'portfolio/get_ticker.html', context)


def add_asset(request, portfolio, coin, price):
    portfolio = Portfolio.objects.get(pk=portfolio)
    form = AddAsset()
    if request.method == "POST":
        form = AddAsset(request.POST)
        if form.is_valid():
            try:
                asset = Asset.objects.get(portfolio_name=portfolio, ticker=coin)
                pk = asset.id
                b_or_s = 'buy'
                update_asset(request, pk, b_or_s, coin, price)
                return redirect(reverse('get_asset_list', args=[portfolio.id]))

            except Asset.DoesNotExist:
                obj = form.save(commit=False)
                quantity = float(form['quantity'].value())
                AP = float(request.POST.get('average_price'))
                obj.price = price
                USDspent = float(quantity) * float(price)
                obj.average_price = AP
                obj.portfolio_name = portfolio
                obj.ticker = coin
                obj.pnl = 0.00
                obj.usd_earned = 0.00
                obj.usd_spent = USDspent
                obj.current_holdings = float(quantity) * float(price)
                obj.save()
                return redirect(reverse('get_asset_list', args=[portfolio.id]))

    context = {
        'form': form,
        'tickerList': tickerList,
        'ticker': coin,
        'price': price,
    }
    return render(request, 'portfolio/add_asset.html', context)


def update_asset(request, pk, b_or_s, coin, price):
    asset = get_object_or_404(Asset, pk=pk)
    returnedCoin = call_api()
    if request.method == 'POST':
        if coin is not None:
            coin = coin
        else:
            coin = request.POST.get("ticker")
        if price is not None:
            price = get_coin_price(coin, returnedCoin)
        else:
            price = price

        form = UpdateAsset(request.POST, instance=asset)
        asset_qty = float(asset.quantity)
        curr_spent = float(asset.usd_spent)
        curr_usd_earned = float(asset.usd_earned)
        curr_PnL = float(asset.pnl)
        if b_or_s == 'buy':
            # do the calculations for BUYING
            new_qty = float(form['quantity'].value())
            new_inv = float(price) * float(new_qty)
            asset.quantity = asset_qty + new_qty
            asset.usd_spent = curr_spent + new_inv
            asset.current_holdings = float(asset.quantity) * float(price)
            asset.ticker = coin
            asset.save()
            messages.success(request, f"{new_qty} {coin} successfully purchased!")

        elif b_or_s == 'sell':
            # do the calculations for SELLING
            if float(form['quantity'].value()) > asset_qty:
                messages.error(request, "Not enough available to sell.")
                return redirect(update_asset, pk, 'sell')
            else:
                new_qty = float(form['quantity'].value())
                usd_earned = price * new_qty
                asset.ticker = coin
                asset.quantity = asset_qty - new_qty
                asset.usd_earned = curr_usd_earned + usd_earned
                asset.current_holdings = (asset.quantity) * price
                if asset.quantity <= 0:
                    asset.delete()
                else:
                    asset.save()
                messages.success(request, f"{new_qty} {coin} successfully sold!")
        return redirect(get_asset_list, asset.portfolio_name.pk)

    if b_or_s == 'sell':
        # grab the current quantity available to sell
        form = UpdateAsset(instance=asset)
    else:
        form = UpdateAsset()
    context = {
        'asset': asset,
        'b_or_s': b_or_s,
        'form': form,
    }
    return render(request, 'portfolio/buy_sell_asset.html', context)
