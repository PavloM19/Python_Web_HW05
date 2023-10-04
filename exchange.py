import aiohttp
import asyncio
from datetime import datetime, timedelta
import platform


def main(days = 1, *add_currency):
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates?date='
    
    def limit_days(num: int):
        if num < 1:
            print("Days must be greater than zero")
            num = 1
        elif num > 10:
            print('Error: Number of days should not exceed 10.')
            num = 10

        return num        


    def dates(num_days: int) -> list[str]:
        list_dates = list()
        today = datetime.now()
        for i in range(num_days):
            day = today - timedelta(days=i)
            list_dates.append(day.strftime("%d.%m.%Y"))
        
        return list_dates


    def format_data(raw_data: dict) -> dict:
        formatted = dict()
        formatted[raw_data['date']] = dict()

        for rate in raw_data['exchangeRate']:
            if rate['currency'] in currency_list:
                temp_dict = dict()
                temp_dict[rate['currency']] = {
                    'sale': rate['saleRate'], 
                    'purchase': rate['purchaseRate']
                }
                formatted[raw_data['date']].update(temp_dict)

        return formatted


    async def exchange_rates(days):
        list_dates = dates(limit_days(days))
        out_list = list()
        for date in list_dates:
            url = f'{BASE_URL}{date}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        out_list.append(format_data(data))
                    else:
                        print(f"Error for date: {date}")

        return out_list
        

    currency_list = {'USD', 'EUR'}
    all_currency = ['AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'GEL', 'HUF', 'ILS', 'JPY', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 'TMT', 'TRY', 'UAH', 'USD', 'UZS', 'XAU']

    if isinstance(days, str):
        if days.isdigit():
            days = int(days)
        else:
            print("Days must be a number")
            days = 1

    if add_currency:
        for cur in add_currency:
            cur = cur.upper()
            if cur in all_currency:
                currency_list.update(set([cur])) #additional currency
            else:
                print(f"{cur} is not a valid currency code")
        
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    return exchange_rates(days) # asyncio.run(exchange_rates(days))


if __name__ == "__main__":
    out_data = main('2', 'USD', 'GBP', 'pln', 'zz')
    print(out_data)