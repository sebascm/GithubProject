#!/usr/bin/python3
from github import Github
from collections import Counter

import sys
import json


class Connection():
    def __init__(self):
        self.token = sys.argv[1]
        self.repo = sys.argv[2]
        self.auth = Github(self.token)


class Commits(Connection):
    connection = Connection()
    g = connection.auth
    repo = connection.repo
    totalCommits = g.get_repo(repo).get_commits().totalCount
    commits = g.get_repo(repo).get_commits()
    totalContributors = g.get_repo(repo).get_contributors().totalCount
    contributors = g.get_repo(repo).get_contributors()
    listCommits = []
    for commit in commits:
            if (commit.author is None or commit.author.login is None):
                # Si el usuario está inactivo, el login del autor es None
                listCommits.append('None')
            else:
                listCommits.append(commit.author.login)
    dictCommits = Counter(listCommits)
    listKeys = list(dictCommits.keys())
    # Añadimos un usuario "Otros" para aquellos que realicen < 0.5% de commits
    listKeys.append('Otros')
    listPercentage = []
    for item in dictCommits.values():
        percentage = 100 * float(item) / float(totalCommits)
        listPercentage.append(percentage)

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

    with open('dataTotal.json', 'w', encoding='utf-8') as f:
        jsonFile = json.dump({"Nombre repositorio": repo,
                              "Commits totales": totalCommits,
                              "Contribuidores totales": totalContributors},
                             f, indent=4)

    with open('dataCommits.json', 'w', encoding='utf-8') as f:
        jsonFile = json.dump({"Commits": [{"Autor": key, "Porcentaje": value}
                             for key, value in dictPercentages.items()]}, f,
                             indent=4)
