from decimal import Decimal

import car
import map
import driver
import offer
import passenger

_car = car.Car(car.Model.HYUNDAI_SOLARIS, 'E-123')
_driver = driver.Driver('Makar', 'cool_driver_007', _car)
_driver.location = map.Location(1, 1)
_driver.get_ready()

_passenger = passenger.Passenger('Mikhail', 'smellofnapalm')
_passenger.google_pay_balance = Decimal(1000.0)
_passenger.location = map.Location(0, 0)
destination = map.Location(3, 3)

_offer = offer.OfferDirector().make_offer_without_car_with_applepay(_passenger, destination)
if offer is not None:
    offer.OfferManager().add_offer(_offer)
    offer.OfferManager().notify_observers()
trip = _driver.handle_offer(offer_index=0)

if trip is not None:
    trip.next_state()
    trip.next_state()
    trip.next_state()
    print(trip.__dict__)




