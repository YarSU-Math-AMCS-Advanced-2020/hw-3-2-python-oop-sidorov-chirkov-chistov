import random
from random import randint
from typing import List, Optional
from uuid import uuid4, UUID

from driver import Driver
from manager import Manager, singleton
from map import Location, Map
from passenger import Passenger


class User:
    def __init__(self, login: str, password: str):

        # user with login admin and password 'password' is an empty user
        if login != 'admin' and password != 'password':
            if type(login) != str:
                raise TypeError("Login should be string, got " + str(type(login)))
            if not login[0].isalpha() or not login.isalnum():
                raise ValueError("Login should consist of letters and digits,"
                                 "first symbol is letter")

        self.login = login
        self.__location = Location(randint(Map().min_x, Map().max_x),
                                   randint(Map().min_y, Map().max_y))
        self.id = uuid4()

        # We don't save passwords!
        self.__password = hash(password)
        self.__rating: float = random.random() * 10  # from 0.0 to 10.0

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value: float):
        self.__rating = value
        if self.__rating > 10.0:
            self.__rating = 10.0
        if self.__rating < 0.0:
            self.__rating = 0.0

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value: Location):
        if 0 <= value.x <= Map().max_x and 0 <= value.y <= Map().max_y:
            self.__location = value

    def __str__(self):
        return f"{self.login}"


@singleton
class UserManager:
    def __init__(self):
        self.users: List[User] = []

    def del_user_by_id(self, _id: UUID) -> bool:
        return Manager.del_by_id(self.users, _id)

    def find_user_by_id(self, _id: UUID) -> Optional[User]:
        return Manager.find_by_id(self.users, _id)

    def find_driver_by_id(self, _id: UUID) -> Optional[Driver]:
        driver = Manager.find_by_id(self.users, _id)
        if driver is Driver:
            return driver
        return None

    def find_passenger_by_id(self, _id: UUID) -> Optional[Passenger]:
        passenger = Manager.find_by_id(self.users, _id)
        if passenger is Passenger:
            return passenger
        return None

    def add_user(self, user: User) -> bool:
        for user in self.users:
            if user.login == user.login:
                raise ValueError("Login is already used by another user")
        return Manager.add_element(self.users, user)
