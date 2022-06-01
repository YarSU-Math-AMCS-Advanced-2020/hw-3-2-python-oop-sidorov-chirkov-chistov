from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum
from typing import Optional

from passenger import Passenger


class PaymentHandlerType(Enum):
    GooglePayHandler = 1
    ApplePayHandler = 2
    BankCardPayHandler = 3
    CashPayHandler = 4


# Create handler with selected type first
# Cash payment is default
def create_handler(passenger: Passenger,
                   payment_handler_type: PaymentHandlerType) -> PaymentHandler:
    if payment_handler_type == CashPayHandler:
        handler: PaymentHandler = CashPayHandler(passenger)
        return handler

    handler = GooglePayHandler(passenger)
    handler.set_next(ApplePayHandler(passenger))
    handler.set_next(BankCardPayHandler(passenger))

    if payment_handler_type == ApplePayHandler:
        handler = ApplePayHandler(passenger)
        handler.set_next(GooglePayHandler(passenger))
        handler.set_next(BankCardPayHandler(passenger))

    if payment_handler_type == BankCardPayHandler:
        handler = BankCardPayHandler(passenger)
        handler.set_next(GooglePayHandler(passenger))
        handler.set_next(ApplePayHandler(passenger))

    handler.set_next(CashPayHandler(passenger))
    return handler


class PaymentHandler(ABC):
    _next_handler: Optional[PaymentHandler] = None

    @abstractmethod
    def __init__(self, passenger: Passenger):
        self.passenger = passenger

    def set_next(self, handler: PaymentHandler) -> PaymentHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, price: Decimal) -> str:
        if self._next_handler:
            return self._next_handler.handle(price)

        return 'Something went wrong'


class GooglePayHandler(PaymentHandler):
    def __init__(self, passenger: Passenger):
        super().__init__(passenger)

    def handle(self, price: Decimal) -> str:
        if self.passenger.google_pay_balance >= price:
            self.passenger.google_pay_balance -= price
            return 'Payment by GooglePay went through'
        else:
            return super().handle(price)


class ApplePayHandler(PaymentHandler):
    def __init__(self, passenger: Passenger):
        super().__init__(passenger)

    def handle(self, price: Decimal) -> str:
        if self.passenger.apple_pay_balance >= price:
            self.passenger.apple_pay_balance -= price
            return 'Payment by ApplePay went through'
        else:
            return super().handle(price)


class BankCardPayHandler(PaymentHandler):
    def __init__(self, passenger: Passenger):
        super().__init__(passenger)

    def handle(self, price: Decimal) -> str:
        if self.passenger.google_pay_balance >= price:
            self.passenger.bank_card_balance -= price
            return 'Payment by card went through'
        else:
            return super().handle(price)


class CashPayHandler(PaymentHandler):
    def __init__(self, passenger: Passenger):
        super().__init__(passenger)

    def handle(self, price: Decimal) -> str:
        return 'Passenger have to pay by cash'
