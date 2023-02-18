from __future__ import print_function

import os.path
import csv
import pandas as pd
import numpy as np
from PIL import ImageTk,Image
import random as r
import matplotlib.pyplot as plt
import seaborn as sb
import statsmodels.api as sm
from scipy import stats
import scipy.stats as s
import tkinter as tk
import io


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID.
print("x")
SAMPLE_SPREADSHEET_ID = '1hmr8vA7tnvEV3vcjuoWabojLw7rkh8-CuXu47lod8Qo'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Forms2!A2:AD500").execute()
values = result.get('values', [])
print("y")
#csv gen
df = pd.DataFrame(values)
df.to_csv('sample.csv')
teams = []
for i in range(len(df.index)):
    if str(df.iloc[i][1]).split(" ") not in teams:
        team = str(df.iloc[i][1]).split(" ")
        if len(team)>=2:
            teams.append(team)
print(teams)
def search(team):
    for num,name in teams:
        complete = num+" "+name
        if team == num or team==name or team==complete:
            print(complete)
            return complete
    return " "
def error(match):
    Azul = 0
    Rojo = 0
    PA = 0
    PR = 0
    PUR = 0
    PDR = 0
    AUR = 0
    ADR = 0
    ER = 0
    LR = 0
    PUA = 0
    PDA = 0
    AUA = 0
    ADA = 0
    EA = 0
    LA = 0
    FA = 0
    FR = 0
    for i in range(len(df.index)):
        if str(df.iloc[i][2])==match:
            if str(df.iloc[i][3])=="Azul":
                PA = int(df.iloc[i][28])
                PUA += int(df.iloc[i][14])*2
                PDA += int(df.iloc[i][12])
                AUA += int(df.iloc[i][7])*4
                ADA +=int(df.iloc[i][9])*2
                print(PA)
                if int(df.iloc[i][16]) == 0:
                    EA = 0
                elif int(df.iloc[i][16]) == 1:
                    EA += 4
                elif int(df.iloc[i][9]) == 2:
                    EA += 6
                elif int(df.iloc[i][9]) == 3:
                    EA += 10
                elif int(df.iloc[i][9]) == 4:
                    EA += 16
                if df.iloc[i][5] == "Si":
                    LA += 2
                FA += int(df.iloc[i][21])
            if str(df.iloc[i][3])=="Rojo":
                PR = int(df.iloc[i][28])
                print(PR)
                PR = int(df.iloc[i][28])
                PUR += int(df.iloc[i][14])*2
                PDR += int(df.iloc[i][12])
                AUR += int(df.iloc[i][7])*4
                ADR +=int(df.iloc[i][9])*2
                if int(df.iloc[i][16]) == 0:
                    ER += 0
                elif int(df.iloc[i][16]) == 1:
                    ER += 4
                elif int(df.iloc[i][9]) == 2:
                    ER += 6
                elif int(df.iloc[i][9]) == 3:
                    ER += 10
                elif int(df.iloc[i][9]) == 4:
                    ER += 16
                if df.iloc[i][5] == "Si":
                    LR += 2
                FR += int(df.iloc[i][21])
    Azul = PUA +PDA +AUA +ADA+FR+FA+EA
    Rojo = PUR +PDR +AUR +ADR+FA+FR+ER
    if PA != Azul or Rojo != PR:
        return (0,["Azul: R:"+str(PA) + " | P:"+str(Azul)],["Rojo: R:"+str(PR) +" | P:"+str(Rojo)])
    return(1,PA,PR)
def analyze(list, count):
    Match = []
    Amount = []
    Value = []
    for i in list:
        if i not in Match:
            Match.append(i)
    Match = sorted(Match)

    for i in Match:
        c = 0
        for j in list:
            if i==j:
                c+=1
        Amount.append(c)

    for j in range(len(Match)):
        if j>=1:
            Value.append([Match[j],Amount[j]/count+Value[j-1][1]])
        else:
            Value.append([Match[j], Amount[j] / count])
        print(Value)
    return Value


def percentages(team):
    team = search(team)
    Primary_up= []
    Primary_down = []
    Autonomous_up = []
    Autonomous_down = []
    count = 0
    for i in range(len(df.index)):
        Auto_up = 0
        Auto_down = 0
        Teleop_up = 0
        Teleop_down = 0
        if df.iloc[i][1] == team:
            Auto_up += int(df.iloc[i][8])
            Auto_down+= int(df.iloc[i][10])
            Teleop_down += int(df.iloc[i][13])
            Teleop_up += int(df.iloc[i][15])
            Primary_up.append(Teleop_up)
            Primary_down.append(Teleop_down)
            Autonomous_up.append(Auto_up)
            Autonomous_down.append(Auto_down)
            count+=1
    All = [Primary_up,Primary_down,Autonomous_down,Autonomous_up]

    Distribution = []
    for a in All:
        Distribution.append(analyze(a,count))
    print(Distribution)
    return Distribution

def coordinates(Distribution):
    All = []
    for i in range(len(Distribution)):
        x = [0]
        y = [0]
        count = 0
        for j in Distribution[i]:
            if j[0] == 0:
                x.append(1)
                y.append(j[1])
            else:
                x.append(j[0])
                y.append(j[1])
            count+=1
        All.append([x,y])
    return All

def regression(All):
    graph = []
    for i in All:
        x = []
        y = []
        for j in range(len(i[0])):
            if i[0][j] != 0 and i[1][j] != 1:
                a = np.log(i[0][j])
                if a not in x:
                     x.append(a)
                     y.append(np.log(-np.log(1-i[1][j])))
        if len(x) >= 2:
            m, b = np.polyfit(x,y, 1)
            h = [m, np.exp(-b / m)]
            graph.append(h)
        elif len(x)== 1:
            for j in range(len(i[0])):
                if i[0][j] != 0 and i[1][j] != 1:
                    sum = -np.log(1-i[1][j])/i[0][j]
                    graph.append([sum])
        elif len(x) == 0:
            graph.append([0,0])
    return graph

def weibull(values):
    scenarios = []
    printable = []
    count = 1
    for value in values:
        if len(value)==2:
            if value[0] != 0 and value[1] != 0:
                wi = value[0]*((-np.log(1-np.random.rand(1)))**(1/value[1]))
                printable.append([wi,count])
                wi2 = value[0] * ((-np.log(1 - np.random.rand(1000))) ** (1 / value[1]))
                print("AAAAAAAAAAAAAAAAAAAAA")
                print(wi2)
            else:
                wi = 0
                printable.append([wi, count])
            scenarios.append(wi)
        else:
            wi = -np.log(1-np.random.rand(1))/value[0]
            scenarios.append(wi)
            printable.append([wi, count])
        count+=1

    suma = 0
    A = 0
    PU = 0
    PD = 0
    for i in range(len(scenarios)):
        point = int(scenarios[i])
        print(printable)
        if i == 0:
           suma+= point*2
           PU += point*2
        elif i == 1:
            suma += point
            PD +=point
        elif i == 2:
            suma += point*2
            A+=point*2
        elif i == 3:
            suma += point*4
            A+= point*4
    p = [int(A),int(PU),int(PD)]
    return [int(suma),p]

def weibullplot(values):
    scenarios = []
    for value in values:
        if len(value) == 2:
            if value[0] != 0 and value[1] != 0:
                wi = value[0] * ((-np.log(1 - np.random.rand(1000))) ** (1 / value[1]))
                scenarios.append(wi)
        else:
            wi = -np.log(1 - np.random.rand(1000)) / value[0]
            scenarios.append(wi)
    for scene in scenarios:
        plt.plot(scene)
        plt.show()
def Endgame(team):
    team = search(team)
    EndGame = 0
    count = 0
    for i in range(len(df.index)):
        if df.iloc[i][1] == team:
            EndGame += int(df.iloc[i][20])
            print(int(df.iloc[i][20]))
            count += 1
    print(EndGame/count)
    if int(EndGame/count) > 0:
        if int(EndGame / count) < 1:
            EndGame = 0
        elif int(EndGame / count) >= 1 and int(EndGame / count) < 2:
            EndGame = 4
        elif int(EndGame / count) >= 2 and int(EndGame / count) < 3:
            EndGame = 6
        elif int(EndGame / count) >= 3 and int(EndGame / count) < 4:
            EndGame = 10
        else:
            EndGame = 15
    return EndGame
def fouls(team):
    team = search(team)
    Fouls = 0
    count = 0
    for i in range(len(df.index)):
        if df.iloc[i][1] == team:
            Fouls += int(df.iloc[i][23])
            count += 1
    if count==0:
        return Fouls
    return(Fouls/count)

def line(team):
    team = search(team)
    Auto = 0
    count = 0
    for i in range(len(df.index)):
        if df.iloc[i][1] == team:
            if df.iloc[i][6] == "Si":
                Auto += 2
            Auto += int(df.iloc[i][13])
            count+=1
    if Auto == 0:
        return 0
    return int(Auto/count)

def point(team):
    team = search(team)
    sum = Endgame(team)+line(team) + weibull(regression(coordinates(percentages(team))))[0]
    return sum
def info(team):
    team = search(team)
    w = weibull(regression(coordinates(percentages(team))))[1]
    a = [w[0]+line(team),w[1]+w[2],Endgame(team)]
    return a
def maximum(team):
    team = search(team)
    p = []
    for i in range(200):
        p.append(point(team))
    return max(p)

def avg(team):
    team = search(team)
    sum = 0
    for i in range(300):
        sum+=point(team)
    return sum/300

def alliance(Alliance1):
    a1 = point(Alliance1[0]) +point(Alliance1[1])+point(Alliance1[2])
    return a1
def avgAlliance(Alliance1):
    sum = 0
    for i in range(100):
        sum+=alliance(Alliance1)
    return sum/100
def maxAlliance(Alliance1):
    sum = []
    for i in range(100):
        sum.append(alliance(Alliance1))
    return max(sum)
def simulator(Alliance1,Alliance2):
    count = 50
    v1 = 0
    v2 = 0
    sa = 0
    sb = 0
    for i in range(count):
        a1 = point(Alliance1[0]) + point(Alliance1[1]) +point(Alliance1[2])+fouls(Alliance2[0])+fouls(Alliance2[1])+fouls(Alliance2[2])
        print(f"Alianza 1 {a1}")
        sa+=a1
        a2 = point(Alliance2[0]) + point(Alliance2[1]) +point(Alliance2[2])+ fouls(Alliance1[0])+fouls(Alliance1[1])+fouls(Alliance1[2])
        print(f"Alianza 2 {a2}")
        sb+=a2
        if a1 > a2:
            v1+=1
        else:
            v2+=1
    return [v1/count*100,sb/count,sa/count]

def priority2(team,priority):
    team = search(team)
    a = weibull(regression(coordinates(percentages(team))))
    points = a[1]
    expected = a[0]+Endgame(team)+line(team)
    #print(weibull(regression(coordinates(percentages(team))))[0])
    points.append(Endgame(team))
    sum = 0
    if priority[0] == 0:
        sum += points[0]*0.9+line(team)*0.9
    else:
        sum += points[0]
    if priority[1] == 0:
        sum += points[1]*0.5
    else:
        sum+= points[1]*2
    if priority[2] == 0:
        sum+=points[2]*0.5
    else:
        sum+=points[2]*2
    if priority[3] == 0:
        if points[3]>=2:
            sum+=(points[3]-2)
        else:
            sum+=0
    else:
        sum+=points[3]+4

    print([sum,expected])
    return [sum,expected]
def points(team):
    team = search(team)
    ran = []
    EndGame = 0
    Auto = 0
    Teleop = 0
    Fouls = 0
    count = 0
    for i in range(len(df.index)):
        if df.iloc[i][1] == team:
            EndGame += int(df.iloc[i][20])
            Auto += int(df.iloc[i][8]) * 4 + int(
                df.iloc[i][10]) * 2
            if df.iloc[i][6] == "Si":
                Auto += 2
            Teleop += int(df.iloc[i][13]) + int(
                df.iloc[i][15]) * 2
            Fouls += int(df.iloc[i][23])
            count += 1
            ran.append(EndGame + Auto + Teleop)
    if int(EndGame)>0:
        if int(EndGame / count) < 1:
            EndGame = 0
        elif int(EndGame / count) >= 1 and int(EndGame / count) < 2:
            EndGame = 4
        elif int(EndGame / count) >= 2 and int(EndGame / count) < 3:
            EndGame = 6
        elif int(EndGame / count) >= 3 and int(EndGame / count) < 4:
            EndGame = 10
        else:
            EndGame = 15
    deviation = np.std(ran)
    af = 0
    Tf = 0
    F = 0
    if int(Auto)==0:
        af = 0
    else:
        af = Auto
    if Teleop == 0:
        Tf = 0
    else:
        Tf = Teleop
    if Fouls == 0:
        F = 0
    else:
        F = Fouls
    Total = int(EndGame+af/count+Tf/count+F/count)
    scores = {"Endgame": EndGame, "Auto": int(af/count), "Teleop": int(Tf/count), "Fouls": int(F/count),"Total":int(Total)}
    return scores

def priority(scores, purpose):
    points = 0
    print(scores)
    for score, value in scores.items():
        if score == "Endgame":
            if purpose[0] == 1:
                points += (value * 1.1)
            else:
                points +=(value * 0.5)
        elif score == "Auto":
            if purpose[1] == 1:
                points += (value * 1.05)
            else:
                points += (value * 0.95)
        elif score == "Teleop":
            if purpose[2] == 1:
                points += (value * 1.1)
            else:
                points += (value * 0.8)
        elif score == "Fouls":
            if purpose[3] == 1:
                points += (value * 1.3)
            else:
                points += (value * 0.7)
    return points

def alliance2(team_1, purpose_1, team_2, purpose_2, team_3, purpose_3):
    cont_1 = priority(points(team_1), purpose_1)
    cont_2 = priority(points(team_2), purpose_2)
    cont_3 = priority(points(team_3), purpose_3)
    Endgame = 0
    Auto = 0
    Teleop = 0
    Fouls = 0
    Endgame += cont_1[0] + cont_2[0] + cont_3[0]
    Auto += cont_1[1] + cont_2[1] + cont_3[1]
    Teleop += cont_1[2] + cont_2[2] + cont_3[2]
    Fouls += cont_1[3] + cont_2[3] + cont_3[3]
    Deviation = (cont_1[4] + cont_2[4] + cont_3[4])
    return ((Endgame + Auto + Teleop), Fouls, Deviation)

def alliance3(teams):
    sum = points(teams[0])["Total"]+points(teams[1])["Total"]+points(teams[2])["Total"]
    return sum
#WINDOW
window = tk.Tk()
window.geometry("600x600")
window.configure(bg='grey')
l = tk.Label(window,text="Scouting Buluk 3472 \nSimulator 2022 ඞ",fg="green",height=3,width=40)
l.place(x=0,y=0)
l.config(font=("Courier", 20))
l2 =tk.Label(window,text="Simplified Analysis",fg="green",height=2,width=20)
l2.place(x=434,y=100)
l2.config(font=("Courier", 10),bg="green",fg="black")
l3 =tk.Label(window,text="Advanced Analysis",fg="green",height=2,width=20)
l3.place(x=0,y=100)
l3.config(font=("Courier", 10),bg="green",fg="black")

def s(Alliance,w):
    l = tk.Label(w, text=str(int(alliance(Alliance))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def werror(match,w):
    l = tk.Label(w, text=str(error(match)),height=4,width=45)
    l.place(x=0,y=300)
    l.config(font=("Courier", 10))
def wavgAlliance(Alliance,w):
    l = tk.Label(w, text="Avg: "+str(int(avgAlliance(Alliance))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def wmaximumAlliance(Alliance,w):
    l = tk.Label(w, text="Max: "+str(int(maxAlliance(Alliance))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def wpoints(team,w):
    l = tk.Label(w, text="Exp: "+str(int(point(team))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def wmaximum(team,w):
    l = tk.Label(w, text="Max: "+str(int(maximum(team))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def wavg(team,w):
    l = tk.Label(w, text="Avg: "+str(int(avg(team))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def wsimplified(team,w):
    l = tk.Label(w, text=str((points(team))),height=2,width=15)
    l.place(x=0,y=300)
    l.config(font=("Courier", 6), width=100,height=20)
def winfo(team,w):
    a = info(team)
    l = tk.Label(w, text="Auto: "+str(a[0]) +"\nTeleop: "+str(a[1]) + "\nEndgame: "+str(a[2]),height=2,width=15)
    l.place(x=0,y=160)
    l.config(font=("Courier", 15), width=40,height=5)
def wsimplifiedpriority(team,p,w):
    l = tk.Label(w, text=str(int(priority(points(team),p.split(",")))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def wsimplifiedAlliance(teams,w):
    l = tk.Label(w, text=str(int(alliance3(teams))),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
def wpriority(team,priorities,w):
    l = tk.Label(w, text="P:"+str(int(priority2(team,priorities.split(","))[0])),height=2,width=10)
    l.place(x=180,y=300)
    l.config(font=("Courier", 20))
    l2 = tk.Label(w, text="E:"+str(int(priority2(team,priorities.split(","))[1])),height=2,width=10)
    l2.place(x=180,y=200)
    l2.config(font=("Courier", 20))
def wsimulator(Alliance1,Alliance2,w):
    a = simulator(Alliance1,Alliance2)
    if a[0] > 50:
       l = tk.Label(w, text="A1: "+str(int(a[0]))+"%",height=2,width=10)
    else:
        l = tk.Label(w, text="A2: "+str(100-int(a[0]))+"%", height=2, width=10)
    l.config(font=("Courier", 14))
    l.place(x=220,y=300)
    l.config(font=("Courier", 28))
    l2 = tk.Label(w, text="A1: "+str(int(a[2])),height=2,width=10)
    l2.place(x=200,y=200)
    l2.config(font=("Courier", 20))
    l3 = tk.Label(w, text="A2: "+str(int(a[1])),height=2,width=10)
    l3.place(x=500,y=200)
    l3.config(font=("Courier", 20))
def w1():
    window1 = tk.Tk()
    window1.geometry("400x400")
    window1.configure(bg='grey')
    T = tk.Text(window1, height=2, width=20)
    T.place(x=200,y=60)
    l = tk.Label(window1, text="My Team: ",height=2,width=10)
    l.place(x=120,y=60)
    T2 = tk.Text(window1, height=2, width=20)
    T2.place(x=200, y=100)
    l2 = tk.Label(window1, text="Team 1", height=2, width=10)
    l2.place(x=120,y=100)
    T3 = tk.Text(window1, height=2, width=20)
    T3.place(x=200, y=140)
    l3 = tk.Label(window1, text="Team 2", height=2, width=10)
    l3.place(x=120,y=140)
    l4 = tk.Label(window1, text="Equipos",height=2,width=10)
    l4.config(font=("Courier", 14))
    l4.place(x=300,y=0)
    b1 = tk.Button(window1,text="Expected Score",width=13,height=5, command= lambda m="F" : s([T.get("1.0","end-1c"),T2.get("1.0","end-1c"),T3.get("1.0","end-1c")],window1))
    b1.place(x=0, y=10)
    b2 = tk.Button(window1,text="Average Score",width=13,height=5, command= lambda m="F" : wavgAlliance([T.get("1.0","end-1c"),T2.get("1.0","end-1c"),T3.get("1.0","end-1c")],window1))
    b2.place(x=0, y=100)
    b3 = tk.Button(window1,text="Max Score",width=13,height=5, command= lambda m="F" : wmaximumAlliance([T.get("1.0","end-1c"),T2.get("1.0","end-1c"),T3.get("1.0","end-1c")],window1))
    b3.place(x=0, y=190)

def w2():
    window2 = tk.Tk()
    window2.geometry("400x400")
    window2.configure(bg='grey')
    T = tk.Text(window2, height=2, width=20)
    T.place(x=200, y=60)
    l = tk.Label(window2, text="My Team: ",height=2,width=10)
    l.place(x=120,y=60)
    T2 = tk.Text(window2, height=2, width=20)
    T2.place(x=200, y=100)
    l2 = tk.Label(window2, text="Priorities [1,0,0,1]\n[A,PU,PD,E]: ",height=2,width=10)
    l2.place(x=120,y=100)
    button = tk.Button(window2, text="Expected Points", width=13, height=5, command=lambda m="F": wpoints(T.get("1.0","end-1c"),window2))
    button.place(x=2, y=10)
    button1 = tk.Button(window2, text="Priority Points", width=13, height=5, command=lambda m="F": wpriority(T.get("1.0", "end-1c"),T2.get("1.0", "end-1c"),window2))
    button1.place(x=2, y=100)
    button2 = tk.Button(window2,text="Maximum expected \nscore", width=13, height=5, command=lambda m="F":wmaximum(T.get("1.0", "end-1c"),window2))
    button2.place(x=2, y=190)
    button3 = tk.Button(window2,text="Average expected \nscore", width=13, height=5, command=lambda m="F":wavg(T.get("1.0", "end-1c"),window2))
    button3.place(x=2, y=280)
def w3():
    window3 = tk.Tk()
    window3.geometry("800x400")
    window3.configure(bg='grey')
    T = tk.Text(window3, height=2, width=20)
    T.place(x=200,y=60)
    l = tk.Label(window3, text="My Team: ",height=2,width=10)
    l.place(x=120,y=60)
    T2 = tk.Text(window3, height=2, width=20)
    T2.place(x=200, y=100)
    l2 = tk.Label(window3, text="Team 1", height=2, width=10)
    l2.place(x=120,y=100)
    T3 = tk.Text(window3, height=2, width=20)
    T3.place(x=200, y=140)
    l3 = tk.Label(window3, text="Team 2", height=2, width=10)
    l3.place(x=120,y=140)
    l4 = tk.Label(window3, text="Alliance 1",height=2,width=10)
    l4.config(font=("Courier", 14))
    l4.place(x=250, y=0)
    l5 = tk.Label(window3, text="Alliance 2", height=2, width=10)
    l5.config(font=("Courier", 14))
    l5.place(x=550, y=0)
    T4 = tk.Text(window3, height=2, width=20)
    T4.place(x=500,y=60)
    T5 = tk.Text(window3, height=2, width=20)
    T5.place(x=500, y=100)
    T6 = tk.Text(window3, height=2, width=20)
    T6.place(x=500, y=140)
    button1 = tk.Button(window3, text="Simulator", width=13, height=5, command=lambda m="F": wsimulator([T.get("1.0","end-1c"),T2.get("1.0","end-1c"),T3.get("1.0","end-1c")],[T4.get("1.0","end-1c"),T5.get("1.0","end-1c"),T6.get("1.0","end-1c")], window3))
    button1.place(x=0, y=20)
def w4():
    window4 = tk.Tk()
    window4.geometry("400x400")
    window4.configure(bg='grey')
    T = tk.Text(window4, height=2, width=20)
    T.place(x=200, y=60)
    l = tk.Label(window4, text="My Team: ", height=2, width=10)
    l.place(x=120, y=60)
    T2 = tk.Text(window4, height=2, width=20)
    T2.place(x=200, y=100)
    l2 = tk.Label(window4, text="Priorities [1,0,0,1]: ",height=2,width=10)
    l2.place(x=120,y=100)
    button1= tk.Button(window4, text="Expected points", width=13, height=5, command=lambda m="F": wsimplified(T.get("1.0", "end-1c"), window4))
    button1.place(x=0, y=20)
    button2 = tk.Button(window4, text="Priority Points", width=13,height=5,command=lambda m="F": wsimplifiedpriority(T.get("1.0", "end-1c"),T2.get("1.0", "end-1c"), window4))
    button2.place(x=0, y=120)
def w5():
    window5 = tk.Tk()
    window5.geometry("400x400")
    window5.configure(bg="grey")
    T = tk.Text(window5, height=2, width=20)
    T.place(x=200,y=60)
    l = tk.Label(window5, text="My Team: ",height=2,width=10)
    l.place(x=120,y=60)
    T2 = tk.Text(window5, height=2, width=20)
    T2.place(x=200, y=100)
    l2 = tk.Label(window5, text="Team 1", height=2, width=10)
    l2.place(x=120,y=100)
    T3 = tk.Text(window5, height=2, width=20)
    T3.place(x=200, y=140)
    l3 = tk.Label(window5, text="Team 2", height=2, width=10)
    l3.place(x=120,y=140)
    l4 = tk.Label(window5, text="Equipos",height=2,width=10)
    l4.config(font=("Courier", 14))
    l4.place(x=300,y=0)
    button = tk.Button(window5,text="Expected Score",width=10,height=5,command=lambda m="F": wsimplifiedAlliance([T.get("1.0","end-1c"),T2.get("1.0","end-1c"),T3.get("1.0","end-1c")],window5))
    button.place(x=0, y=10)
def w6():
    window6 = tk.Tk()
    window6.geometry("400x400")
    window6.configure(bg="grey")
    T = tk.Text(window6, height=2, width=20)
    T.place(x=200,y=60)
    l = tk.Label(window6, text="My Team: ",height=2,width=10)
    l.place(x=120,y=60)
    button = tk.Button(window6,text="info",width=10,height=5,command=lambda m="F": winfo(T.get("1.0","end-1c"),window6))
    button.place(x=0, y=10)
def w7():
    window7 = tk.Tk()
    window7.geometry("400x400")
    window7.configure(bg="grey")
    T = tk.Text(window7, height=2, width=20)
    T.place(x=200,y=60)
    l = tk.Label(window7, text="Match: ",height=2,width=10)
    l.place(x=120,y=60)
    button = tk.Button(window7,text="Review",width=10,height=5,command=lambda m="F": werror(T.get("1.0","end-1c"),window7))
    button.place(x=0, y=10)
button = tk.Button(window,text="MyAlliance", bg="red",width=10,height=5, command= lambda m="F":w1())
button.place(x=35,y=240)
button1 = tk.Button(window,text="MyTeam",bg="green",width=10,height=5, command= lambda m="F":w2())
button1.place(x=35,y=140)
button2 = tk.Button(window,text="Simulator",bg="blue",width=10,height=5, command= lambda m="F":w3())
button2.place(x=35,y=340)
button6 = tk.Button(window,text="Info",bg="blue",width=10,height=5, command= lambda m="F":w6())
button6.place(x=35,y=440)
button3 = tk.Button(window,text="MyTeam",bg="green",width=10,height=5, command= lambda m="F":w4())
button3.place(x=470,y=140)
button4 = tk.Button(window,text="MyAlliance",bg="red",width=10,height=5, command= lambda m="F":w5())
button4.place(x=470,y=240)
button5 = tk.Button(window,text="MyMatch",bg="red",width=10,height=5, command= lambda m="F":w7())
button5.place(x=470,y=340)
window.mainloop()



