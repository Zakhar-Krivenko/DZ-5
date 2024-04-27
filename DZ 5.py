import aiohttp
import asyncio

class PrivatBankAPI:
    def __init__(self):
        self.base_url = 'https://api.privatbank.ua/p24api'

    async def get_exchange_rate(self, currency, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/pubinfo?json&exchange&coursid=5&date={date}') as response:
                data = await response.json()
                for rate in data:
                    if rate['ccy'] == currency:
                        return {'sale': float(rate['sale']), 'purchase': float(rate['buy'])}
                return None

async def fetch_exchange_rates(days):
    api = PrivatBankAPI()
    tasks = []
    for i in range(1, days + 1):
        date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
        tasks.append(api.get_exchange_rate('EUR', date))
        tasks.append(api.get_exchange_rate('USD', date))
    exchange_rates = await asyncio.gather(*tasks)
    return exchange_rates

async def main(days):
    exchange_rates = await fetch_exchange_rates(days)
    results = []
    for i in range(0, len(exchange_rates), 2):
        date = (datetime.now() - timedelta(days=i // 2 + 1)).strftime('%d.%m.%Y')
        result = {
            date: {
                'EUR': exchange_rates[i],
                'USD': exchange_rates[i + 1]
            }
        }
        results.append(result)
    return results

if __name__ == '__main__':
    import sys
    from datetime import datetime, timedelta

    if len(sys.argv) != 2:
        print("Usage: python main.py <number of days>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        if days > 10:
            print("Error: Number of days cannot exceed 10")
            sys.exit(1)
    except ValueError:
        print("Error: Invalid number of days")
        sys.exit(1)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(days))
    print(results)
