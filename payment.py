from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal

from customer import Customer


# TODO: we can construct different chains of payment
def payment_process(customer: Customer, price: Decimal) -> str:
    payment_handler = GooglePayHandler(customer)
    payment_handler.set_next(ApplePayHandler(customer))
    payment_handler.set_next(BankCardPayHandler(customer))
    payment_handler.set_next(CashPayHandler(customer))
    return payment_handler.handle(price)


class PaymentHandler(ABC):
    _next_handler: PaymentHandler = None

    @abstractmethod
    def __init__(self, customer: Customer):
        self.customer = customer

    def set_next(self, handler: PaymentHandler) -> PaymentHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, price: Decimal) -> str:
        if self._next_handler:
            return self._next_handler.handle(price)

        return 'Something went wrong'


class GooglePayHandler(PaymentHandler):
    def __init__(self, customer: Customer):
        super().__init__(customer)

    def handle(self, price: Decimal) -> str:
        if self.customer.google_pay_balance >= price:
            self.customer.google_pay_balance -= price
            return 'Payment by GooglePay went through'
        else:
            return super().handle(price)


class ApplePayHandler(PaymentHandler):
    def __init__(self, customer: Customer):
        super().__init__(customer)

    def handle(self, price: Decimal) -> str:
        if self.customer.apple_pay_balance >= price:
            self.customer.apple_pay_balance -= price
            return 'Payment by ApplePay went through'
        else:
            return super().handle(price)


class BankCardPayHandler(PaymentHandler):
    def __init__(self, customer: Customer):
        super().__init__(customer)

    def handle(self, price: Decimal) -> str:
        if self.customer.google_pay_balance >= price:
            self.customer.bank_card_balance -= price
            return 'Payment by card went through'
        else:
            return super().handle(price)


class CashPayHandler(PaymentHandler):
    def __init__(self, customer: Customer):
        super().__init__(customer)

    def handle(self, price: Decimal) -> str:
        return 'Client have to pay by cash'
