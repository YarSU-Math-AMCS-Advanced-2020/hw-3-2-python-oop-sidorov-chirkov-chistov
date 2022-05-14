from uuid import UUID


# Decorator for a singleton
def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


# TODO: очень много копипаста, надо менять способ хранения всего этого
@singleton
class Manager:
    @staticmethod
    def del_by_id(lst: list, id: UUID):
        for i in range(len(lst)):
            if lst[i].id == id:
                del lst[i]
                return True
        return False

    @staticmethod
    def find_by_id(lst: list, id: UUID):
        for element in lst:
            if element.id == id:
                return element
        return None

    @staticmethod
    def add_element(lst: list, element):
        if element not in lst:
            lst.append(element)
            return True
        return False
