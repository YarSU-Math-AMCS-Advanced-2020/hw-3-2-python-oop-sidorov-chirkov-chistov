from decimal import Decimal

import user


class Passenger(user.User):
    def __init__(self, login: str, password: str):
        super().__init__(login, password)
        self.google_pay_balance: Decimal = Decimal(0.0)
        self.apple_pay_balance: Decimal = Decimal(0.0)
        self.bank_card_balance: Decimal = Decimal(0.0)
