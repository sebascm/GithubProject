#!/usr/bin/python3
from github import Github

import sys


class Connection():
    def __init__(self):
        self.token = sys.argv[1]
        self.repo = sys.argv[2]
        self.connection = Github(self.token)


class Commits(Connection):
    connection = Connection()
    g = connection.connection
    repo = connection.repo
    totalCommits = g.get_repo(repo).get_commits().totalCount
    commits = g.get_repo(repo).get_commits()
    totalContributors = g.get_repo(repo).get_contributors().totalCount
    contributors = g.get_repo(repo).get_contributors()
    listCommits = []
    for commit in commits:
            if (commit is None or commit.author is None or commit.author.login
                    is None):
                listCommits.append('None')
            else:
                listCommits.append(commit.author.login)
    print(listCommits)
