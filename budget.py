from utils import right_pad, left_pad


class Category:
    _name_length = 30
    _description_length = 23
    _amount_length = 7

    def __init__(self, name: str):
        self.name = name
        self.ledger = []
        self.current_balance = 0

    def deposit(self, amount: float, description: str = ''):
        self.ledger.append({'amount': amount, 'description': description})
        self.current_balance += amount

    def withdraw(self, amount: float, description: str = '') -> bool:
        if not self.check_funds(amount):
            return False
        self.ledger.append({'amount': -amount, 'description': description})
        self.current_balance -= amount
        return True

    def transfer(self, amount: float, destination_category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, 'Transfer to ' + destination_category.name)
        destination_category.deposit(amount, 'Transfer from ' + self.name)

        return True

    def get_balance(self) -> float:
        return self.current_balance

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


def create_spend_chart(categories):
    pass
