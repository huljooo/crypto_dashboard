import requests
import time
import os
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

console = Console()

COINS = ['bitcoin', 'ethereum', 'solana', 'dogecoin']
API_URL = 'https://api.coingecko.com/api/v3/simple/price'


def fetch_prices(vs_currency):
    try:
        response = requests.get(API_URL, params={
            'ids': ','.join(COINS),
            'vs_currencies': vs_currency,
            'include_24hr_change': 'true'
        })
        return response.json()
    except Exception as e:
        return {coin: {vs_currency: 'Error'} for coin in COINS}


def make_table(prices, vs_currency):
    currency_upper = vs_currency.upper()
    table = Table(title=f"🚀 Crypto Dashboard ({currency_upper})", box=box.SIMPLE_HEAVY)
    table.add_column("Coin", justify="left", style="cyan", no_wrap=True)
    table.add_column(f"Price ({currency_upper})", justify="right", style="green")
    table.add_column("24h Change (%)", justify="right", style="magenta")

    for coin in COINS:
        price = prices.get(coin, {}).get(vs_currency, 'N/A')
        change = prices.get(coin, {}).get(f'{vs_currency}_24h_change', 0.0)
        change_str = f"{change:.2f}" if isinstance(change, (float, int)) else 'N/A'
        table.add_row(coin.title(), f"{price:,.2f}" if isinstance(price, (float, int)) else str(price), change_str)
    return table


def main():
    vs_currency = Prompt.ask("Wybierz walutę (np. usd, eur, pln)", default="usd").lower()

    with Live(console=console, refresh_per_second=2) as live:
        while True:
            prices = fetch_prices(vs_currency)
            table = make_table(prices, vs_currency)
            panel = Panel(table, title="Live Market Tracker", border_style="bright_blue")
            live.update(panel)
            time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Zamknięto dashboard. Do zobaczenia![/]")
