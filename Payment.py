from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from Client import Client


# TODO: we can construct different chains of payment
def payment_process(client: Client, price: Decimal) -> str:
    gp = GooglePayHandler(client)
    ap = ApplePayHandler(client)
    bc = BankCardPayHandler(client)
    cp = CashPayHandler(client)
    gp.set_next(ap).set_next(bc).set_next(cp)
    return gp.handle(price)


class PaymentHandler(ABC):
    _next_handler: PaymentHandler = None

    @abstractmethod
    def __init__(self, client: Client):
        self.client = client

    def set_next(self, handler: PaymentHandler) -> PaymentHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, price: Decimal) -> str:
        if self._next_handler:
            return self._next_handler.handle(price)

        return 'Something went wrong'


class GooglePayHandler(PaymentHandler):
    def __init__(self, client: Client):
        super().__init__(client)

    def handle(self, price: Decimal) -> str:
        if self.client.google_pay_balance >= price:
            self.client.google_pay_balance -= price
            return "Payment by GooglePay went through"
        else:
            return super().handle(price)


class ApplePayHandler(PaymentHandler):
    def __init__(self, client: Client):
        super().__init__(client)

    def handle(self, price: Decimal) -> str:
        if self.client.apple_pay_balance >= price:
            self.client.apple_pay_balance -= price
            return "Payment by ApplePay went through"
        else:
            return super().handle(price)


class BankCardPayHandler(PaymentHandler):
    def __init__(self, client: Client):
        super().__init__(client)

    def handle(self, price: Decimal) -> str:
        if self.client.google_pay_balance >= price:
            self.client.bank_card_balance -= price
            return "Payment by card went through"
        else:
            return super().handle(price)


class CashPayHandler(PaymentHandler):
    def __init__(self, client: Client):
        super().__init__(client)

    def handle(self, price: Decimal) -> str:
        return "Client have to pay by cash"
