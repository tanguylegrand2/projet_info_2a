from logging import raiseExceptions
from Business_layer.figure_geometrique.segment import Segment
from Business_layer.figure_geometrique.rectangle import Rectangle


class Fonctions_Multipolygon:
    def segments(self, multipolygone):
        multipolygon = multipolygone.copy()
        seg = []
        while multipolygon != []:
            test = False
            if type(multipolygon[-1]) == list and multipolygon[-1] != []:
                if type(multipolygon[-1][0]) == list and multipolygon[-1] != []:
                    if type(multipolygon[-1][0][0]) in [float, int]:
                        test = True
            if test == True:
                seg.append(multipolygon.pop())
            else:
                liste = multipolygon.pop()
                for elem in liste:
                    multipolygon.append(elem)
        segments_a_retourner = []
        for groupe in seg:
            if len(groupe) >= 2:
                for i in range(len(groupe) - 1):
                    segments_a_retourner.append(Segment(groupe[i], groupe[i + 1]))
        if segments_a_retourner == []:
            segments_a_retourner = None
        return segments_a_retourner

    def points(self, multipolygone):
        multipolygon = multipolygone.copy()
        if type(multipolygon) != list:
            return None
        else:
            ok = True
            for i in multipolygon:
                if len(i) != 2 or type(i[0]) == list or type(i[1]) == list:
                    ok = False
            while not ok:
                new_liste = []
                for i in multipolygon:
                    if len(i) == 2 and type(i[0]) != list and type(i[1]) != list:
                        new_liste.append(i)
                    else:
                        for elem in i:
                            new_liste.append(elem)
                multipolygon = new_liste
                ok = True
                for i in multipolygon:
                    if len(i) != 2 or type(i[0]) == list or type(i[1]) == list:
                        ok = False
            return multipolygon

    def rectangle(self, multipolygone):
        multipolygon = multipolygone.copy()
        if type(multipolygon) != list:
            return None
        else:
            ok = True
            for i in multipolygon:
                if len(i) != 2 or type(i[0]) == list or type(i[1]) == list:
                    ok = False
            while not ok:
                new_liste = []
                for i in multipolygon:
                    if len(i) == 2 and type(i[0]) != list and type(i[1]) != list:
                        new_liste.append(i)
                    else:
                        for elem in i:
                            new_liste.append(elem)
                multipolygon = new_liste
                ok = True
                for i in multipolygon:
                    if len(i) != 2 or type(i[0]) == list or type(i[1]) == list:
                        ok = False
            n_points = len(multipolygon)
            if n_points > 0:
                x_list = [multipolygon[i][0] for i in range(n_points)]
                y_list = [multipolygon[i][1] for i in range(n_points)]
                xmin = min(x_list)
                xmax = max(x_list)
                ymin = min(y_list)
                ymax = max(y_list)
                return Rectangle([xmin, ymin], [xmax, ymax])
            else:
                return None
