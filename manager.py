from typing import List, Optional, Any
from uuid import UUID


# Decorator for a singleton
def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


@singleton
class Manager:
    @staticmethod
    def del_by_id(lst: List[Any], _id: UUID) -> bool:
        for index in range(len(lst)):
            if lst[index].id == _id:
                del lst[index]
                return True
        return False

    @staticmethod
    def find_by_id(lst: List[Any], _id: UUID) -> Optional[Any]:
        for element in lst:
            if element.id == _id:
                return element
        return None

    @staticmethod
    def add_element(lst: List[Any], element: Any) -> bool:
        if element not in lst:
            lst.append(element)
            return True
        return False
