import requests
import sys


class Wallet:
    def __init__(self, investment, convert):
        if investment < 0 or not (investment + 1 > investment):
            raise Exception
        if convert <= 0 or not (convert + 1 > convert):
            raise Exception
        self._investment = investment
        self._convert = convert
        self._balance = 0
        self._wallet = 0

    def deposit(self, num):
        if num <= 0:
            raise ValueError("Deposit must be positive")
        if num > self._investment:
            raise ValueError
        self._wallet += num
        self._balance += self._convert * num
        self._investment -= num

    def withdraw(self, num):
        if num <= 0:
            raise ValueError("Withdrawal must be positive")
        if num > self._wallet:
            raise ValueError
        if num * self._convert > self._balance:
            raise ValueError
        self._wallet -= num
        self._balance -= self._convert * num

    @property
    def investment(self):
        return self._investment

    @property
    def balance(self):
        return self._balance

    @property
    def wallet(self):
        return self._wallet


def main():
    portfolio = get_investment()
    while True:
        print(f"Current balance of crypto wallet: ${portfolio.balance:,.2f}")
        action = input("Would you like to deposit, withdraw, or quit? d/w/q: ").lower()
        if action == "d":
            coins = float(input("Enter the amount to deposit: "))
            try:
                portfolio.deposit(coins)
            except ValueError:
                sys.exit("Insufficient funds")
        elif action == "w":
            coins = float(input("Enter the amount to withdraw: "))
            try:
                portfolio.withdraw(coins)
            except ValueError:
                sys.exit("Insufficient funds")
        elif action == "q":
            sys.exit(f"Final portfolio balance: ${portfolio.balance:,.2f}")
        else:
            print("Invalid option: Please choose 'd', 'w', or 'q'.")


def get_investment():
    investment = float(input("How many coins do you own? "))
    if investment >= 0:
        try:
            convert = convert_coins(1)
            return Wallet(investment, convert)
        except requests.RequestException:
            sys.exit("Unable to retrieve data")
    else:
        raise ValueError


def convert_coins(coins):
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        result = response.json()
        total = result["bpi"]["USD"]["rate_float"]
        return total
    except requests.RequestException:
        sys.exit("Unable to retrieve data")


if __name__ == "__main__":
    main()