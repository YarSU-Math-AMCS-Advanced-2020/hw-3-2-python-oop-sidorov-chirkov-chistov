from decimal import Decimal

from car import Car, Model
from driver import Driver
from map import Location, Map
from offer import OfferDirector, OfferManager, OfferBuilder, Offer
from passenger import Passenger
from trip import TripManager

car = Car(Model.HYUNDAI_SOLARIS, 'E-123')
driver = Driver('Makar', 'cool_driver_007', car)
driver.location = Location(1, 1)
driver.get_ready()

passenger = Passenger('Mikhail', 'smellofnapalm')
passenger.google_pay_balance = Decimal(1000.0)
passenger.location = Location(0, 0)
destination = Location(3, 3)

offer = OfferDirector().make_offer_without_car_with_applepay(passenger, destination)
if offer is not None:
    OfferManager().add_offer(offer)
    OfferManager().notify_observers()
trip = driver.handle_offer(offer_index=0)

if trip is not None:
    trip.next_state()
    trip.next_state()
    trip.next_state()
    print(trip.__dict__)




