#!/usr/bin/python3
from github import Github

import sys
import json

class Connection():
    def __init__(self):
        self.token = sys.argv[1]
        self.repo = sys.argv[2]
        self.auth = Github(self.token)

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
    
    return auxDict

def updateUserPullRequestsStats(user, pull, contributorStats):
    if pull.state == "open":
        contributorStats['open_pull_requests'] += 1
    else:
        contributorStats['closed_pull_requests'] += 1
    if pull.is_merged():
        contributorStats['merged_pull_requests'] += 1
    return contributorStats

def addContributorsStats(pullsList):
    contributorsDict = {}
    for pull in pullsList:
        if pull.user.login not in contributorsDict:
            if (pull.user is None or pull.user.login is None):
                # Si el usuario está inactivo, el login del autor es None
                contributorsDict['None'] = 'None'
            else:
                contributorsDict[pull.user.login] = addUserPullRequestsStats(pull.user, pull) 
        else:
            contributorsDict[pull.user.login] = updateUserPullRequestsStats(pull.user, pull, contributorsDict[pull.user.login])
    return contributorsDict

def getMergedPulls(contributorsDict):
    auxCount = 0
    for contributor in contributorsDict:
        auxCount += contributorsDict[contributor]['merged_pull_requests']

    return auxCount

class Pulls(Connection):
    connection = Connection()
    g = connection.auth
    repo = g.get_repo(connection.repo)

    openPulls = repo.get_pulls(state="open")
    closedPulls = repo.get_pulls(state="close")
    allPulls = repo.get_pulls(state="all")
    
    openPullsCount = openPulls.totalCount
    closedPullsCount = closedPulls.totalCount
    totalPullsCount = allPulls.totalCount

    contributors = repo.get_contributors()

    contributorsDict = addContributorsStats(allPulls)
    
    mergedPullsCount = getMergedPulls(contributorsDict)

    statsDict = {}
    statsDict['totalPulls'] = totalPullsCount
    statsDict['openPulls'] = openPullsCount
    statsDict['closedPulls'] = closedPullsCount
    statsDict['mergedPulls'] = mergedPullsCount
    statsDict['closedAndMergedPercent'] = 100 * float(mergedPullsCount) / float(closedPullsCount)

    statsDict['contributorsStats'] = contributorsDict

    with open('pullRequestsStats.json', 'w') as json_file:
        json.dump(statsDict, json_file, indent=4)