import enum


class Model(enum.Enum):
    lada_2121 = 0
    renault_logan = 1
    hyundai_solaris = 2
    volkswagen_polo = 3
    mercedes_benz_s = 4
    audi_a8 = 5


class CarType(enum.Enum):
    economy = 0
    comfort = 1
    business = 2


class Car:
    def __init__(self, model: Model, plate_num: str):
        self.model = model
        self.car_type: CarType = self.__determinate_car_type(model)
        self.plate_num = plate_num

    @staticmethod
    def __determinate_car_type(model):
        if model in [Model.lada_2121, Model.renault_logan]:
            return CarType.economy
        if model in [Model.hyundai_solaris, Model.volkswagen_polo]:
            return CarType.comfort
        if model in [Model.mercedes_benz_s, Model.audi_a8]:
            return CarType.business
