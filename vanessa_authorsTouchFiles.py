# this file gets authors who touched commit files

import numpy as np
import matplotlib.pyplot as plt 
import json
import requests
import csv
from datetime import datetime
import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(testdict, dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)
            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            #print(jsonCommits) 
            
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # get event/payload ['name'], author = comit['author'], date = shaObject['date'         
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                # n = shaObject['commit']
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if (".java" not in filename): continue; 
                    dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    print(filename)
                    author = shaObject['commit']['author']['name'];
                    date_of = shaObject['commit']['author']['date'];
                    testdict[author] = date_of; # try to make 2D dict 
                    print(author) # where testdict[filename][date] = author 
                    print(date_of)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# E N D

''' this function creates the scatter plot using CSV file. '''        
def create_plot(document):
    tmp_data = [] # used for graphing
    #file = csv.DictReader(open(document))
    tmp_data = np.genfromtxt(document,delimiter=',', names=['Filename','Touches'])
    # Plot...
    y = np.random.random(290)
    plt.scatter(tmp_data['Filename'], tmp_data['Touches'], c=y, s=50) # s is a size of marker 
    plt.gray()
    plt.show()
    
#E N D 
        
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["ghp_IdzlGhHoh7Fg53apvKx"]

dictfiles = dict()
testdict = dict()  

countfiles(testdict, dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches", "Author", "Date"];
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)


bigcount = None
bigfilename = None

# print (dictfiles)

# should call appendCSV here? will add filename, count, "author, date"
for filename, count in dictfiles.items():
    
    for author, date_of in testdict.items():
        rows = [filename, count, author, date_of] #tmp sol.. does "author/date" for every filename!
        writer.writerow(rows)    
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close();

print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')

#call scatter plot 
create_plot(fileOutput) 