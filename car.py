import enum


class Model(enum.Enum):
    LADA_2121 = 0
    RENAULT_LOGAN = 1
    HYUNDAI_SOLARIS = 2
    VOLKSWAGEN_POLO = 3
    MERCEDES_BENZ_S = 4
    AUDI_A8 = 5


class CarType(enum.Enum):
    ECONOMY = 0
    COMFORT = 1
    BUSINESS = 2


class Car:
    def __init__(self, model: Model, plate_num: str):
        self.model = model
        self.car_type: CarType = self.__determine_car_type(model)
        self.plate_num = plate_num

    @staticmethod
    def __determine_car_type(model):
        if model in [Model.LADA_2121, Model.RENAULT_LOGAN]:
            return CarType.ECONOMY
        if model in [Model.HYUNDAI_SOLARIS, Model.VOLKSWAGEN_POLO]:
            return CarType.COMFORT
        if model in [Model.MERCEDES_BENZ_S, Model.AUDI_A8]:
            return CarType.BUSINESS
