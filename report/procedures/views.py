import pandas as pd
from django.http import HttpResponse
import os
import re

from django.shortcuts import render


def MessageCounter(request):
    directory = os.path.join(os.getcwd(), "data/datas/table")
    f = open(os.path.join(directory, 'Messages-Counter----.tex'), 'r')
    info = []
    for data in f:
        data = data.split('&')
        try:
            if data[0] == "Count":
                continue
            Count = (re.search('}(.*)', data[0]).group(1))
            Last_Timestamp = (data[1])
            Color = (re.search('{(.*)}', data[0]).group(1).split('!')[0])
            N = (data[2])
            T = (data[3])
            D = (data[4])
            C = (data[5])
            Type = (data[6])
            Name = (data[7])
            Name_ExtraId = (data[8])
            info.append(
                {
                    "Count": Count,
                    "Color":Color,
                    "Last_Timestamp": Last_Timestamp,
                    "N": N,
                    "T": T,
                    "D": D,
                    "C": C,
                    "Type": Type,
                    "Name": Name,
                    "Name_ExtraId": Name_ExtraId,

                }
            )
        except:
            continue
    print(info)
    context = {
        "info": info
    }
    return render(request, 'message_counter.html', context=context)
