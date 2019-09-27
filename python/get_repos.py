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
        self.repoName = sys.argv[2]
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


def createJson(fileName, data):
    with open(fileName + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def validateJson():
    # Obtención del JSON y esquema
    with open('commitsSchema.jschema') as json_file:
        commitsSchema = json.load(json_file)
    with open('dataTotal.json') as json_file:
        jsonFile = json.load(json_file)
    # Validación
    jsonschema.validate(jsonFile, commitsSchema)


class Commits():

    def __init__(self, repo, repoName):
        self.repo = repo
        self.repoName = repoName
        self.grafico = "PieChart"
        self.orden = "Porcentaje"

    def getData(self):
        try:
            totalCommits = self.repo.get_commits().totalCount
            commits = self.repo.get_commits()
            contributors = self.repo.get_contributors().totalCount
            listCommits = getLoginCommiter(commits)
            listPercentage, listKeys = calculatePercentage(listCommits,
                                                           totalCommits)
            percentage = setPercentage(listKeys, listPercentage)
            data = createRepresentation(self.repoName, totalCommits,
                                        contributors, self.grafico,
                                        self.orden, percentage)
            return data
        except GithubException:
            print("No se puede acceder al repositorio")


def addUserPullRequestsStats(user, pull):
    auxDict = {}
    if pull.state == "open":
        auxDict['open_pull_requests'] = 1
        auxDict['closed_pull_requests'] = 0
    else:
        auxDict['open_pull_requests'] = 0
        auxDict['closed_pull_requests'] = 1
    if pull.is_merged():
        auxDict['merged_pull_requests'] = 1
    else:
        auxDict['merged_pull_requests'] = 0
    auxDict['changed_files'] = pull.changed_files

    return auxDict


def updateUserPullRequestsStats(pull, contributorStats):
    if pull.state == "open":
        contributorStats['open_pull_requests'] += 1
    else:
        contributorStats['closed_pull_requests'] += 1
    if pull.is_merged():
        contributorStats['merged_pull_requests'] += 1
    contributorStats['changed_files'] += pull.changed_files
    return contributorStats


def addContributorsStats(pullsList):
    contributors = {}

    for pull in pullsList:
        login = pull.user.login
        if login not in contributors:
            if (pull.user is None or login is None):
                # Si el usuario está inactivo, el login del autor es None
                contributors['None'] = 'None'
            else:
                contributors[login] = addUserPullRequestsStats(login, pull)
        else:
            stats = contributors[login]
            contributors[login] = updateUserPullRequestsStats(pull, stats)

    for user in contributors:
        openPR = contributors[user]['open_pull_requests']
        closedPR = contributors[user]['closed_pull_requests']
        mergedPR = contributors[user]['merged_pull_requests']
        changedFiles = contributors[user]['changed_files']
        totalPR = openPR + closedPR

        if closedPR != 0:
            contributors[user]['merged_percent'] = 100 * mergedPR / closedPR

        contributors[user]['average_changed_files'] = changedFiles / totalPR

    return contributors


def getMergedPulls(contributorsDict):
    auxCount = 0
    for contributor in contributorsDict:
        auxCount += contributorsDict[contributor]['merged_pull_requests']

    return auxCount


def getTotalFilesChanged(pullRequests):
    auxCount = 0
    for pullRequests in pullRequests:
        auxCount += pullRequests.changed_files

    return auxCount


class PullRequests():

    def __init__(self, repo):
        self.openPulls = repo.get_pulls(state="open").totalCount
        self.closedPulls = repo.get_pulls(state="close").totalCount
        self.allPulls = repo.get_pulls(state="all")
        self.totalPulls = self.allPulls.totalCount
        self.contributors = repo.get_contributors()

    def getData(self):
        contributorsDict = addContributorsStats(self.allPulls)
        mergedPulls = getMergedPulls(contributorsDict)
        changedFiles = getTotalFilesChanged(self.allPulls)

        statsDict = {}
        statsDict['total_pulls'] = self.totalPulls
        statsDict['open_pulls'] = self.openPulls
        statsDict['closed_pulls'] = self.closedPulls
        statsDict['merged_pulls'] = mergedPulls
        statsDict['merged_percent'] = 100 * mergedPulls / self.closedPulls
        statsDict['average_changed_files'] = changedFiles / self.totalPulls
        statsDict['contributors_stats'] = contributorsDict

        return statsDict


def main():
    connection = Connection()
    g = connection.auth
    repo = g.get_repo(connection.repoName)

    commitsData = Commits(repo, connection.repoName).getData()
    createJson("commitsData", commitsData)

    pullRequestsData = PullRequests(repo).getData()
    createJson("pullRequestsData", pullRequestsData)


if __name__ == '__main__':
    main()
