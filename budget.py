from math import floor

from utils import right_pad, left_pad


class Category:
    _name_length = 30
    _description_length = 23
    _amount_length = 7

    def __init__(self, name: str):
        self.name = name
        self.ledger = []
        self.current_balance = 0
        self.withdraw_amount = 0

    def deposit(self, amount: float, description: str = ''):
        self.ledger.append({'amount': amount, 'description': description})
        self.current_balance += amount

    def withdraw(self, amount: float, description: str = '') -> bool:
        if not self.check_funds(amount):
            return False
        self.ledger.append({'amount': -amount, 'description': description})
        self.current_balance -= amount
        self.withdraw_amount += amount
        return True

    def transfer(self, amount: float, destination_category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, 'Transfer to ' + destination_category.name)
        destination_category.deposit(amount, 'Transfer from ' + self.name)

        return True

    def get_balance(self) -> float:
        return self.current_balance

    def get_withdraw_amount(self) -> float:
        return self.withdraw_amount

    def check_funds(self, amount: float) -> bool:
        return amount <= self.get_balance()

    def __str__(self) -> str:
        return "{0}{1}{2}".format(
            self._format_name(),
            self._format_ledger(),
            self._format_total()
        )

    def _format_name(self) -> str:
        amount_of_stars = self._name_length - len(self.name)
        if amount_of_stars % 2 == 0:
            left = right = amount_of_stars // 2
        else:
            left = amount_of_stars // 2
            right = left + 1
        return '*' * left + self.name + '*' * right

    def _format_ledger(self) -> str:
        result = '\n'
        for item in self.ledger:
            result += '{0}{1}\n'.format(
                right_pad(item['description'], length=self._description_length),
                left_pad('{:.2f}'.format(item['amount'])[:self._amount_length])
            )
        return result

    def _format_total(self) -> str:
        return 'Total: ' + str(self.current_balance)


def create_spend_chart(categories) -> str:
    total_spending = 0
    categories_spending = {}
    max_name_length = 0
    for category in categories:
        total_spending += category.get_withdraw_amount()
        max_name_length = max(max_name_length, len(category.name))
    for category in categories:
        categories_spending[category.name] = floor(category.get_withdraw_amount() / total_spending * 100)

    result = 'Percentage spent by category\n'
    for i in range(0, 11):
        current_percentage = 100 - (10 * i)
        result += left_pad(str(current_percentage), length=3) + '|'
        for category in categories_spending:
            if categories_spending[category] >= current_percentage:
                result += ' o '
            else:
                result += '   '
        result += ' \n'
    result += '    ' + ('-' * len(categories) * 3) + '-\n'

    for i in range(1, max_name_length + 1):
        result += '    '
        for category in categories_spending:
            if len(category) >= i:
                result += ' ' + category[i - 1] + ' '
            else:
                result += '   '
        if i == max_name_length:
            result += ' '
        else:
            result += ' \n'
    return result
