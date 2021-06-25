# importing the required libraries
# plot and patches
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import json
import numpy as np
import xlsxwriter

text_color = 'w'

# method to create the pitch
def createpitch(xa,ya,xh,yh,pa,ph):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # pitch outline and center line
    plt.plot([0, 0], [0, 90], color="black")
    plt.plot([0, 120], [90, 90], color="black")
    plt.plot([120, 120], [90, 0], color="black")
    plt.plot([0, 120], [0, 0], color="black")
    plt.plot([60, 60], [0, 90], color="black")
    # left penalty box
    plt.plot([0, 16.5], [25, 25], color="black")
    plt.plot([16.5, 16.5], [25, 65], color="black")
    plt.plot([0, 16.5], [65, 65], color="black")
    # right penalty box
    plt.plot([120, 103.5], [25, 25], color="black")
    plt.plot([103.5, 103.5], [25, 65], color="black")
    plt.plot([120, 103.5], [65, 65], color="black")

    # left 6-yard box
    plt.plot([0, 5.5], [36, 36], color="black")
    plt.plot([5.5, 5.5], [36, 54], color="black")
    plt.plot([0, 5.5], [54, 54], color="black")

    # right 6-yard box
    plt.plot([120, 114.5], [36, 36], color="black")
    plt.plot([114.5, 114.5], [36, 54], color="black")
    plt.plot([120, 114.5], [54, 54], color="black")

    # center circle
    centrecircle = plt.Circle((60, 45), 9.15, color='black', fill=False)
    # kickoff circle
    kocircle = plt.Circle((60, 45), 0.8, color='black', fill=True)

    # leftpenaltyspot
    lpencircle = plt.Circle((11, 45), 0.8, color='black', fill=True)
    # rightpenaltyspot
    rpencircle = plt.Circle((109, 45), 0.8, color='black', fill=True)
    ax.add_patch(centrecircle)
    ax.add_patch(kocircle)
    ax.add_patch(rpencircle)
    ax.add_patch(lpencircle)

    # arcs
    leftarc = Arc((11, 45), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color='black')
    righttarc = Arc((109, 45), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color='black')

    ax.add_patch(leftarc)
    ax.add_patch(righttarc)

    #plt.axis('off')

    plt.scatter(xa,ya)
    plt.scatter(xh, yh)
    for m in range(len(pa)):
        plt.annotate(pa[m],(xa[m],ya[m]),fontsize=9)

    for q in range(len(ph)):
        plt.annotate(ph[q],(xh[q],yh[q]),fontsize=9)
    plt.show()



# url
base_url = 'https://understat.com/match/'
match_id = str(input('Please Enter The Match ID: '))
url = base_url + match_id
print(url)
res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')
scripts = soup.find_all('script')
shotsdata = scripts[1].string
ind_start = shotsdata.index("('") + 2
ind_end = shotsdata.index("')")
json_data = shotsdata[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

data = json.loads(json_data)

data_a = data['a']
data_h = data['h']
x = []
y = []
xa = []
ya = []
xh = []
yh = []
xG = []
team = []
result = []
situation = []
player = []
playera = []
playerh = []
player_assisted = []
minute = []
shotType = []

for index in range(len(data_a)):
    for key in data_a[index]:
        if key == 'X':
            x.append(data_a[index][key])
            xa.append(float(data_a[index][key]))
        if key == 'Y':
            y.append(data_a[index][key])
            ya.append(float(data_a[index][key]))
        if key == 'xG':
            xG.append(data_a[index][key])
        if key == 'h_a':
            if data_a[index][key] == 'a':
                team.append(data_a[index]['a_team'])
            else:
                team.append(data_a[index]['h_team'])
        if key == 'result':
            result.append(data_a[index][key])
        if key == 'situation':
            situation.append(data_a[index][key])
        if key == 'player':
            player.append(data_a[index][key])
            playera.append(data_a[index][key])
        if key == 'player_assisted':
            player_assisted.append(data_a[index][key])
        if key == 'minute':
            minute.append(data_a[index][key])
        if key == 'shotType':
            shotType.append(data_a[index][key])

for index in range(len(data_h)):
    for key in data_h[index]:
        if key == 'X':
            x.append(data_h[index][key])
            xh.append(float(data_h[index][key]))
        if key == 'Y':
            y.append(data_h[index][key])
            yh.append(float(data_h[index][key]))
        if key == 'xG':
            xG.append(data_h[index][key])
        if key == 'h_a':
            if data_h[index][key] == 'a':
                team.append(data_h[index]['a_team'])
            else:
                team.append(data_h[index]['h_team'])
        if key == 'result':
            result.append(data_h[index][key])
        if key == 'situation':
            situation.append(data_h[index][key])
        if key == 'player':
            player.append(data_h[index][key])
            playerh.append(data_h[index][key])
        if key == 'player_assisted':
            player_assisted.append(data_h[index][key])
        if key == 'minute':
            minute.append(data_h[index][key])
        if key == 'shotType':
            shotType.append(data_h[index][key])


for i in range(len(xh)):
    xh[i] = (xh[i]*100)*1.2
    yh[i] = (yh[i]*100)*0.9

for i in range(len(xa)):
    xa[i] = 120 - ((xa[i]*100)*1.2)
    ya[i] = 90 - ((ya[i]*100)*0.9)




col_names = ['x', 'y', 'xG', 'team', 'result', 'situation', 'player', 'player_assisted', 'minute', 'shotType']
df = pd.DataFrame([x, y, xG, team, result, situation, player, player_assisted, minute, shotType], index=col_names)
df = df.T
path =  str(data_a[1]['h_team'] + " vs " + data_a[1]['a_team']) +".xlsx"
writer = pd.ExcelWriter(path, engine='xlsxwriter')
shetname = str(data_a[1]['h_team'] + " vs " + data_a[1]['a_team'])
if len(shetname) >= 31:
    shetname = shetname[0:30]
#df.to_excel(writer, sheet_name=shetname)
#writer.save()
#print(x)


createpitch(xa,ya,xh,yh,playera, playerh)


