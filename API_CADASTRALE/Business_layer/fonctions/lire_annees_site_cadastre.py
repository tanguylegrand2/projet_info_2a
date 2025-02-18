import requests
from bs4 import BeautifulSoup


class LireAnneesSiteCadastre:
    def applique(self):
        requete = requests.get("https://cadastre.data.gouv.fr/data/etalab-cadastre/")
        page = requete.content
        soup = BeautifulSoup(page)
        soup.find({"class": "outerText"})
        page = list(str(page))
        liste_ind = []
        L = []
        for i in range(len(page)):
            if page[i] != " ":
                L.append(page[i])
        nb = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        annees = []
        for i in range(9, len(L)):
            if L[i] in nb:
                if L[i - 1] in nb:
                    if L[i - 2] == "-":
                        if L[i - 3] in nb:
                            if L[i - 4] in nb:
                                if L[i - 5] == "-":
                                    if L[i - 6] in nb:
                                        if L[i - 7] in nb:
                                            if L[i - 8] in nb:
                                                if L[i - 9] in nb:
                                                    annees.append(L[i - 9 : i + 1])

        years = []
        for elem in annees:
            x = ""
            for i in range(len(elem)):
                x += elem[i]
            years.append(x)

        years.append("latest")
        return [{"annees disponibles sur le site": years}]
