from abc import ABC


class Figure_geometrique(ABC):
    def __init__(self, point1: list, point2: list):
        self.__point1 = point1
        self.__point2 = point2

    def __eq__(self, autre_figure) -> bool:
        return (
            self.__point1 == autre_figure.__point1
            and self.__point2 == autre_figure.__point2
        ) or (
            self.__point1 == autre_figure.__point2
            and self.__point2 == autre_figure.__point1
        )

    def __str__(self):
        return str(self.__get_point1__()) + " ; " + str(self.__get_point2__())

    def __get_point1__(self) -> list:
        return self.__point1

    def __get_point2__(self) -> list:
        return self.__point2

    def __set_point1__(self, point1):
        self.__point1 = point1

    def __set_point2__(self, point2):
        self.__point2 = point2
