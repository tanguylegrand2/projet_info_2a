from logging import raiseExceptions
from Business_layer.figure_geometrique.figure_geometrique import Figure_geometrique


class Rectangle(Figure_geometrique):
    def __init__(self, point1: list, point2: list):
        if point1[0] <= point2[0] and point1[1] <= point2[1]:
            super().__init__(point1, point2)
        elif point1[0] >= point2[0] and point1[1] >= point2[1]:
            super().__init__(point2, point1)
        else:
            raiseExceptions(
                "Rectangle mal défini, il faut respecter la forme point1=[xmin,ymin], point2=[xmax,ymax]"
            )

    def se_recoupent(self, autre_rectangle):
        x1min = autre_rectangle.__get_point1__()[0]
        y1min = autre_rectangle.__get_point1__()[1]
        x1max = autre_rectangle.__get_point2__()[0]
        y1max = autre_rectangle.__get_point2__()[1]
        x2min = self.__get_point1__()[0]
        y2min = self.__get_point1__()[1]
        x2max = self.__get_point2__()[0]
        y2max = self.__get_point2__()[1]
        if (
            (x1min <= x2min <= x1max or x1min <= x2max <= x1max)
            and (y1min <= y2min <= y1max or y1min <= y2max <= y1max)
        ) or (
            (x2min <= x1min <= x2max or x2min <= x1max <= x2max)
            and (y2min <= y1min <= y2max or y2min <= y1max <= y2max)
        ):
            return True
        else:
            return False

    def point_a_l_interieur_du_rectangle(self, point):
        return (self.__get_point1__()[0] <= point[0] <= self.__get_point2__()[0]) and (
            self.__get_point1__()[1] <= point[1] <= self.__get_point2__()[1]
        )
