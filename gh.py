#!/usr/bin/python3
from github import Github
from github import GithubException

import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)


import numpy as np


g = Github("71e38534cacd976d08656eb2840fb98a505ca8cf")
list=[]
listTuple=[]
names=[]
values=[]
for repo in g.get_user().get_repos():
    try:
        print(repo.name)
        paginatedList=repo.get_commits()
        print(paginatedList.totalCount)
        for commit in paginatedList:
            if (commit==None or commit.author==None or commit.author.login==None):
                list.append('None')
            else:
                list.append(commit.author.login)
    
        my_dict = {i:list.count(i) for i in list}
    
        newlistkeys=[]
        for i in my_dict.keys():
            newlistkeys.append(i)
        newlistvalues=[]
        for i in my_dict.values():
            newlistvalues.append(i)

        #fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
        #axs[0].bar(newlistkeys, newlistvalues)
        #plt.show()
        #print(my_dict)     
        tips = sns.load_dataset("tips")
        sns.catplot(x=newlistkeys, y=newlistvalues, kind="box", data=tips)
        plt.show()
    except GithubException as e:
        print('Repo empty')   

    list=[]     