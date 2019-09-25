#!/usr/bin/python3
from github import Github

import sys


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
    list = []
    for commit in commits:
            if (commit.author is None or commit.author.login is None):
                # Si el usuario está inactivo, el login del autor es None
                list.append('None')
            else:
                list.append(commit.author.login)
    print(list)
#    my_dict = dict((i, list.count(i)) for i in list)
#    print(my_dict)
