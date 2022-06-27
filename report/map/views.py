

from dis import dis
from lib2to3.pytree import type_repr
from multiprocessing import context

from time import time
from django.http import HttpResponse
from django.shortcuts import render
import json

from .models import Ranges, Color_Info, Point_Info,Static_Info
from .forms import PointForm
import datetime
import pandas as pd
import os
import configparser

color_list = []
def Map(request):
    
    points = Point_Info.objects.all()
    points_list = []
    Messages = []
    dict_from_csv = pd.read_csv('map//data.csv', header=None, index_col=0, squeeze=True).to_dict()

    Time = list(dict_from_csv[1].keys())
    Node = list(dict_from_csv[1].values())
    latitude = list(dict_from_csv[2].values())
    longitude = list(dict_from_csv[3].values())
    technology = list(dict_from_csv[4].values())
    ARFCN = list(dict_from_csv[5].values())
    code = list(dict_from_csv[6].values())
    PLMNID = list(dict_from_csv[7].values())
    LAC = list(dict_from_csv[8].values())
    Color = list(dict_from_csv[13].values())
    CellID = list(dict_from_csv[9].values())
    Scan = list(dict_from_csv[10].values())
    Power = list(dict_from_csv[11].values())
    Quality = list(dict_from_csv[12].values())


    # create location list
    for i in range(1,len(latitude)) :
        l = []
        
        color = Color[i].split(' ')
        
        color = color[0].replace('*','')
        
        if  color == '' :
            color_list.append("#aaaaaa")
           
        else:
            c = str(Set_Color(int(color)))
            color_list.append(c)
        
        message = "Time : "+str(Time[i])+"//"+"Loc : ("+str(latitude[i])+"/"+str(longitude[i])+")"+"//"+"Node id : "+str(Node[i])+"//"+"-------------------------------"+"//"+"Technology : "+str(technology[i])+"//"+"ARFCN : "+ARFCN[i]+"//"+"Code : "+code[i]+"//"+"PLMNID : "+PLMNID[i]+"//"+"LAC : "+LAC[i]+"//"+"Cell id : "+str(CellID[i])+"//"+"Scan Tech : "+str(Scan[i])+"//"+"Power : "+str(Power[i])+"//"+"Quality : "+str(Quality[i])+"//"+"-------------------------------"+"//"+"Color : "+str(Color[i])
        # l.append(format(float(point.latitude),".6f"))
        # l.append(format(float(point.longitude),".6f"))
        l.append(float(latitude[i]))
        l.append(float(longitude[i]))
        points_list.append(l)
        Messages.append(message)

        
        # color_list.append(Set_Color(int(color)))
    
        # print(type(Color[i]))
        
    # print(len(color_list))
    Set_Color_info(color_list)
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

    Time = list(dict_from_csv[1].keys())
    Node = list(dict_from_csv[1].values())
    latitude = list(dict_from_csv[2].values())
    longitude = list(dict_from_csv[3].values())
    technology = list(dict_from_csv[4].values())
    ARFCN = list(dict_from_csv[5].values())
    code = list(dict_from_csv[6].values())
    PLMNID = list(dict_from_csv[7].values())
    LAC = list(dict_from_csv[8].values())
    Color = list(dict_from_csv[13].values())
    CellID = list(dict_from_csv[9].values())
    Scan = list(dict_from_csv[10].values())
    Power = list(dict_from_csv[11].values())
    Quality = list(dict_from_csv[12].values())

    for i in range(1,len(latitude)) :
        l = []
        
        color = Color[i].split(' ')
        
        color = color[0].replace('*','')
        
        if  color == '' :
            color_list.append("#aaaaaa")
           
        else:
            c = str(Set_Color(int(color)))
            color_list.append(c)

        Point_Info.objects.create(time = Time[i],node = Node[i],latitude = latitude[i],longitude = longitude[i],technology = technology[i],arfcn = ARFCN[i],code = code[i],plmnId = PLMNID[i],
        lac = LAC[i],color = Color[i],cellId = CellID[i],scan = Scan[i],power = Power[i],quality = Quality[i])
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
    
    conditions = Ranges.objects.all()
    for con in conditions:
        if color_val in range(con.min,con.max):

            return con.color
    return None

def test(request):
    return render(request,'index.html')


def RSRP(request):
   
    # Set_Color_info(color_list)
    # data = pd.read_csv('map//RSRP.csv', header=None, index_col=0, squeeze=True).to_dict()
    statics = Static_Info.objects.filter(parameter = "RSRP")
    context = {
        'info' :Color_Info.objects.all().distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
    }
    # context.update('rsrp_static','dscvfcd')
    temp = send_data()
    context.update(temp)
    return render(request, 'RSRP.html',context=context)


def Set_Color_info(color_list):
    # color_count = Color.objects.all()
    
    # my_dict = {i.color:color_info.count(i.color) for i in color_info}
    l = []
    for i in color_list:
        # count = color_info.count(i[0])
        l.append(i)


    my_dict = {i:l.count(i) for i in l}
    colors = Color_Info.objects.filter(parameter = "RSRP")
    temp = []
    values = my_dict.values()
    total = sum(values)
    for i in colors:
        count = 0
        if i.color_range.color not in my_dict :
            count = 0
           
        else:
            
            count = my_dict[i.color_range.color]

        distribution = (count/(total))*100
        # print([i.color_range.color])
        temp.append([distribution,i.color_range.color])

        Color_Info.objects.filter(id = i.id).update(distribution = distribution,count = count)
   

   

   

def send_data():
    points_list = []
    Messages = []
    dict_from_csv = pd.read_csv('map//data.csv', header=None, index_col=0, squeeze=True).to_dict()
    Time = list(dict_from_csv[1].keys())
    Node = list(dict_from_csv[1].values())
    latitude = list(dict_from_csv[2].values())
    longitude = list(dict_from_csv[3].values())
    technology = list(dict_from_csv[4].values())
    ARFCN = list(dict_from_csv[5].values())
    code = list(dict_from_csv[6].values())
    PLMNID = list(dict_from_csv[7].values())
    LAC = list(dict_from_csv[8].values())
    Color = list(dict_from_csv[13].values())
    CellID = list(dict_from_csv[9].values())
    Scan = list(dict_from_csv[10].values())
    Power = list(dict_from_csv[11].values())
    Quality = list(dict_from_csv[12].values())

    # create location list
    for i in range(1,len(latitude)) :
        l = []
        
        color = Color[i].split(' ')
        
        color = color[0].replace('*','')
        
        if  color == '' :
            color_list.append("#aaaaaa")
           
        else:
            c = str(Set_Color(int(color)))
            color_list.append(c)
        
        message = "Time : "+str(Time[i])+"//"+"Loc : ("+str(latitude[i])+"/"+str(longitude[i])+")"+"//"+"Node id : "+str(Node[i])+"//"+"-------------------------------"+"//"+"Technology : "+str(technology[i])+"//"+"ARFCN : "+ARFCN[i]+"//"+"Code : "+code[i]+"//"+"PLMNID : "+PLMNID[i]+"//"+"LAC : "+LAC[i]+"//"+"Cell id : "+str(CellID[i])+"//"+"Scan Tech : "+str(Scan[i])+"//"+"Power : "+str(Power[i])+"//"+"Quality : "+str(Quality[i])+"//"+"-------------------------------"+"//"+"Color : "+str(Color[i])
        l.append(float(latitude[i]))
        l.append(float(longitude[i]))
        points_list.append(l)
        Messages.append(message)
    Set_Color_info(color_list)
    contex = {
        "popup_message" :'hello world',
        "circule_poses":[points_list],
        "circule_color":color_list,
        "circule_messages" : Messages, 
        "marker_poses":[35.7600,51.5200]
    }
    return contex



def setting(request):
    return render(request,'setting.html')

def test_line_chart(request):
    return render(request,'test_line_chart.html')

def test_circle_chart(request):

    context = {
        'info' :Color_Info.objects.all().distinct(),
        'len': len(list(Color_Info.objects.all()))
    }
    return render(request,'test_circle_chart.html',context)