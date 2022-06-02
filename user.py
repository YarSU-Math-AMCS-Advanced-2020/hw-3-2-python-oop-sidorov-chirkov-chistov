from random import randint, random
from typing import List, Optional
from uuid import uuid4, UUID

import driver
import manager
import map
import passenger


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
        self.__location = map.Location(randint(map.Map().min_x, map.Map().max_x),
                                       randint(map.Map().min_y, map.Map().max_y))
        self.id = uuid4()

        # We don't save passwords!
        self.__password = hash(password)
        self.__rating: float = random() * 10  # from 0.0 to 10.0

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
    def location(self, value: map.Location):
        if 0 <= value.x <= map.Map().max_x and 0 <= value.y <= map.Map().max_y:
            self.__location = value

    def __str__(self):
        return f"{self.login}"


@manager.singleton
class UserManager:
    def __init__(self):
        self.users: List[User] = []

    def del_user_by_id(self, _id: UUID) -> bool:
        return manager.Manager.del_by_id(self.users, _id)

    def find_user_by_id(self, _id: UUID) -> Optional[User]:
        return manager.Manager.find_by_id(self.users, _id)

    def find_driver_by_id(self, _id: UUID) -> Optional[driver.Driver]:
        __driver = manager.Manager.find_by_id(self.users, _id)
        if __driver is driver.Driver:
            return __driver
        return None

    def find_passenger_by_id(self, _id: UUID) -> Optional[passenger.Passenger]:
        __passenger = manager.Manager.find_by_id(self.users, _id)
        if __passenger is passenger.Passenger:
            return __passenger
        return None

    def add_user(self, user: User) -> bool:
        for user in self.users:
            if user.login == user.login:
                raise ValueError("Login is already used by another user")
        return manager.Manager.add_element(self.users, user)
