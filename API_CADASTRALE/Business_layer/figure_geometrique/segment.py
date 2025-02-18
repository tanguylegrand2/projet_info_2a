from Business_layer.figure_geometrique.figure_geometrique import Figure_geometrique


class Segment(Figure_geometrique):
    def __init__(self, point1: list, point2: list):
        super().__init__(point1, point2)
