import discord
import wolframalpha
import requests
from bs4 import BeautifulSoup
import os

# Rename 'help' variable to 'help_message' to avoid conflicts with built-in keyword
help_message = 'To ask a question: q "question"\n To check the price of a stock: price "stock symbol"'

# Use 'startswith()' method instead of converting message to a list and accessing first character
def get_response(message: str) -> str:
    p_message = message.lower()

    if '1071561802808303666' in message:
        for greeting in ['hi', 'hey', 'sup', 'yo', 'hello', 'wsup', 'wassup']:
            if greeting in p_message:
                return greeting
        return help_message

    if message.startswith('q '):
        question = message[2:]
        client = wolframalpha.Client(str(os.getenv('WOLFRAM_TOKEN')))
        res = client.query(question)
        answer = next(res.results).text
        return answer

    if message.startswith('price '):
        message_price = message.split()
        page = requests.get(f"https://www.marketwatch.com/investing/index/{message_price[1].lower()}")
        soup = BeautifulSoup(page.text, "html.parser")

        price = soup.findAll("span", attrs={"class": "value"})
        price2 = soup.findAll("bg-quote", attrs={"class": "value"})
        company = soup.findAll("h1", attrs={"class": "company__name"})
        country = soup.find("span", attrs={"class": "company__market"})
        change = soup.find("bg-quote", attrs={"field": "change"})

        if country.text.startswith('Canada'):
            return f'The current stock price of {message_price[1].upper()} ({company[0].text}) is {price[0].text} CAD.'

        try:
            return f'The current stock price of {message_price[1].upper()} ({company[0].text}) is {price[0].text} USD.'
        except:
            return f'The current stock price of {message_price[1].upper()} ({company[0].text}) is {price2[0].text} USD.'

        # Add error handling for invalid or not found stock symbols
        # return 'Invalid stock symbol' or 'Stock symbol not found' as appropriate
