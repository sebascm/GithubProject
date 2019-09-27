#!/usr/bin/python3
from github import Github
from github import GithubException
from collections import Counter

import sys
import json
import jsonschema


class Connection():
    def __init__(self):
        self.token = sys.argv[1]
        self.repo = sys.argv[2]
        self.auth = Github(self.token)


def createRepresentation(repo, totalCommits, totalContributors, tipoGrafico,
                         ordenacion, dictPercentage):
    dictData = {"Nombre repositorio": repo,
                "Commits totales": totalCommits,
                "Contribuidores totales": totalContributors,
                "Grafico": tipoGrafico,
                "Ordenacion": ordenacion,
                "Datos": [{"Autor": key,
                           "Porcentaje": value}
                          for key, value in
                          dictPercentage.items()]}
    return dictData


def setPercentage(listKeys, listPercentage):
    dictPercentages = {}
    countPercentage = 0
    for listKeys, listPercentage in zip(listKeys, listPercentage):
        # Condición de que tengan más de un 0.5% de commits
        if (listPercentage > 0.5):
            dictPercentages[listKeys] = listPercentage
        else:
            # Porcentaje "Otros"
            countPercentage = countPercentage + listPercentage
    # Se añade ese porcentaje a "Otros"
    dictPercentages['Otros'] = countPercentage

    return dictPercentages


def calculatePercentage(listCommits, totalCommits):
    dictCommits = Counter(listCommits)
    listKeys = list(dictCommits.keys())
    # Añadimos un usuario "Otros" para aquellos
    # que realicen < 0.5% de commits
    listKeys.append('Otros')
    listPercentage = []
    for item in dictCommits.values():
        percentage = 100 * float(item) / float(totalCommits)
        listPercentage.append(percentage)

    return listPercentage, listKeys


def getLoginCommiter(commitList):
    listCommits = []
    for commit in commitList:
        if (commit.author is None or commit.author.login is None):
            # Si el usuario está inactivo, el login del autor es None
            listCommits.append('None')
        else:
            listCommits.append(commit.author.login)

    return listCommits


def createJson(data):
    with open('dataTotal.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def validateJson():
    # Obtención del JSON y esquema
    with open('commitsSchema.jschema') as json_file:
        commitsSchema = json.load(json_file)
    with open('dataTotal.json') as json_file:
        jsonFile = json.load(json_file)
    # Validación
    jsonschema.validate(jsonFile, commitsSchema)


class Commits(Connection):
    connection = Connection()
    g = connection.auth
    repo = connection.repo
    tipoGrafico = "PieChart"
    ordenacion = "Porcentaje"
    try:
        totalCommits = g.get_repo(repo).get_commits().totalCount
        commits = g.get_repo(repo).get_commits()
        totalContributors = g.get_repo(repo).get_contributors().totalCount
        listCommits = getLoginCommiter(commits)
        listPercentage, listKeys = calculatePercentage(listCommits,
                                                       totalCommits)
        dictPercentage = setPercentage(listKeys, listPercentage)
        data = createRepresentation(repo, totalCommits, totalContributors,
                                    tipoGrafico, ordenacion, dictPercentage)
        createJson(data)
    except GithubException:
        print("No se puede acceder al repositorio")


def main():
    Commits()


if __name__ == '__main__':
    main()
