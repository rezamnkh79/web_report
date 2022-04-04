
from calendar import c

from multiprocessing import Condition
from operator import concat
from traceback import print_tb

from django.http import HttpResponse
from django.shortcuts import render
import json
from .models import Color, Poit_Info
from .forms import PointForm
import datetime
import pandas as pd
import os
import configparser


def Map(request):
    print(Set_Color("88"))
    points = Poit_Info.objects.all()
    points_list = []
    Messages = []
    dict_from_csv = pd.read_csv('map//data.csv', header=None, index_col=0, squeeze=True).to_dict()
    latitude = list(dict_from_csv[2].values())
    longitude = list(dict_from_csv[3].values())
    technology = list(dict_from_csv[4].values())
    ARFCN = list(dict_from_csv[5].values())
    code = list(dict_from_csv[6].values())
    PLMNID = list(dict_from_csv[7].values())
    LAC = list(dict_from_csv[8].values())
    Color = list(dict_from_csv[13].values())
    color_list = []

    # create location list
    for i in range(1,len(latitude)) :
        l = []
        
        color = Color[i].split(' ')
        print(color)
        color = color[0].replace('*','')
        
        if  color == '' :
            color_list.append("#CBC6C4")
           
        else:
          
            color_list.append(str(Set_Color(int(color))))
        # condition = SET_COLOR(color)
        message = "Technology : "+str(technology[i])+"/"+"ARFCN : "+ARFCN[i]+"/"+"Code : "+code[i]+"/"+"PLMNID : "+PLMNID[i]+"/"+"LAC : "+LAC[i]
        # l.append(format(float(point.latitude),".6f"))
        # l.append(format(float(point.longitude),".6f"))
        l.append(float(latitude[i]))
        l.append(float(longitude[i]))
        points_list.append(l)
        Messages.append(message)

        
        # color_list.append(Set_Color(int(color)))
    
        # print(type(Color[i]))
        
    # print(len(color_list))
    contex = {
        "popup_message" :'hello world',
        #  "circule_poses":[[35.6926, 51.40000],[35.6926, 51.40110],[35.6926, 51.45000],[35.6926, 51.46000]],
        "circule_poses":[points_list],
        "circule_color":color_list,
        "circule_messages" : Messages, 
        "marker_poses":[35.7600,51.5200]
    }
    return render(request,'map.html',contex)


def Insert_info(request):
    form = PointForm(request.POST or None)
    context ={}
    if form.is_valid():
        form.save()
   
   
    context['form']= form
    return render(request, "create_view.html", context)



def Data(request):

    dict_from_csv = pd.read_csv('map//data.csv', header=None, index_col=0, squeeze=True).to_dict()
    print(len(list(dict_from_csv[3].values())))
    return HttpResponse("done")
    

# def SET_RANGE():
    
#     read_config = configparser.ConfigParser()
#     read_config.read("map//config_datatest.ini")

#     name = read_config.get("Delay_Jitter", "_0_Color")


#     condition = []
#     for (each_key, each_val) in read_config.items("DNS_A%20Records"):
#         temp = []
#         color = ""
#         # print(each_key)
#         # print(each_val)
#         # print("==============================================================")
#         if 'lowerth' in each_key:
#             # print((each_val))
#             temp.append(each_val)
#         if "upperth" in each_key:
#             temp.append(each_val)
#             # print(each_key)
#         if "color" in each_key:
#             # print(each_val)
#             color = str(each_val)
#             dict_temp = {"color" : color}
#             print(str(color)+"ddddddddddddddddddddddddddddddddddd")
#         if len(temp)==0 :
#             continue
#         else :
#             # print("color")
#             # print(color)
#             # print(temp)
#             # print("=======================================================")
#             dict_temp = {"range" :temp}
#         condition.append(dict_temp)
#     print((condition))
#     return condition
    # print(name)

# def SET_COLOR(color):
#     condition = SET_RANGE()
#     c = ""
#     # print(condition)
#     color = color.split(" ")
#     for info in condition:
#     #   print(info["range"])
#       if len(info["range"]) == 0 :
#           continue
#       if int(color[0].replace('*','')) in range(info["range"][0],info["range"][1]):
#           key_list = list(condition.keys())
#           c = key_list[info["color"]]
#     return c

def Set_Color(color_val):
    color_val = int(color_val)
    
    conditions = Color.objects.all()
    for con in conditions:
        if color_val in range(con.min,con.max):

            return con.color
    return None

