#!/usr/bin/env python3
import csv
import argparse
import json
import re
import plotly.graph_objects as go
import numpy as np
import datetime
import plotly

halfperiod = 150

parser = argparse.ArgumentParser(description='Analyze trends in discord channels')
parser.add_argument('file',help='File to analyze.',type=argparse.FileType('r'))
args = parser.parse_args()

messages = json.loads(args.file.read())

frames = []

for i in range(halfperiod,len(messages)-halfperiod):
    count = {}
    for m in messages[i-halfperiod:i+halfperiod]:
        try:
            count[m["user"]] += 1
        except KeyError:
            count[m["user"]] = 1
    frames.append(count)

users = {}

for f in frames:
    for user in f:
        if user not in users:
            users[user] = []

for f in frames:
    for user in users:
        if user in f:
            users[user].append(f[user])
        else:
            users[user].append(0)

fig = go.Figure()
for user in users:
    fig.add_trace(go.Scatter(y=users[user],x=np.arange(len(users[user])),name=user))

fig.write_image(str(datetime.datetime.now()) + ".svg")

plotly.offline.plot(fig, filename=str(datetime.datetime.now())+".html",auto_open=False)

