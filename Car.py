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
        self.car_type = self.__determinate_car_type(model)
        self.plate_num = plate_num

    @staticmethod
    def __determinate_car_type(model):
        economy = [Model.lada_2121, Model.renault_logan]
        comfort = [Model.hyundai_solaris, Model.volkswagen_polo]
        business = [Model.mercedes_benz_s, Model.audi_a8]
        if model in economy:
            return CarType.economy
        if model in comfort:
            return CarType.comfort
        if model in business:
            return CarType.business
