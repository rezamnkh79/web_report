

from curses.ascii import HT
from dis import dis
from inspect import Parameter
from itertools import count
from lib2to3.pytree import type_repr
from multiprocessing import context

import redis
from time import time


from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
import json


from .models import Ranges, Color_Info, Point_Info, Region,Static_Info,Table
import datetime
import pandas as pd
import os

color_list = []

def InsertColorInfoTechnology():
    dict_from_csv = pd.read_csv('map//serving.csv', header=None, index_col=0, squeeze=True)
    # Time = list(dict_from_csv[1].keys())
    # Node = list(dict_from_csv[1].values())
    
    # print(Time)
    # print(Node)
    count3G = 0
    count2G = 0
    count4G = 0
    count5G = 0
    for i in list(dict_from_csv[5]):
        if i == 4 :
            count4G +=1
        elif i == 2 :
            count2G +=1
        elif i == 3 :
            count3G +=1
        else :
            count5G += 1
    
    count2G = int(count2G/len(list(dict_from_csv[5]))*100)
    count3G = int(count3G/len(list(dict_from_csv[5]))*100)
    count4G = int(count4G/len(list(dict_from_csv[5]))*100)
    count5G = int(count5G/len(list(dict_from_csv[5]))*100)
    return ([count2G,count3G,count4G,count5G])
def InsertARFNTable(request):
    dict_from_csv = pd.read_csv('map//Map-Serving Cell-ARFCN_Code---.csv', header=None, index_col=0, squeeze=True)
    for i in range(1,len(list(dict_from_csv[1]))):
    #   table = Table.objects.create(color =list(dict_from_csv[1].keys())[i],name = list(dict_from_csv[1])[i],count = list(dict_from_csv[2])[i],distance = list(dict_from_csv[3])[i],distribution = list(dict_from_csv[4])[i],tech = list(dict_from_csv[5])[i],band = list(dict_from_csv[6])[i],freq =list(dict_from_csv[7])[i])
      table = Table.objects.create(parameter = "Arfcn-Code",color =list(dict_from_csv[1].keys())[i],name = list(dict_from_csv[1])[i],count = list(dict_from_csv[2])[i],distance = list(dict_from_csv[3])[i],distribution = list(dict_from_csv[4])[i],tech = list(dict_from_csv[5])[i])

    return HttpResponse(list(dict_from_csv[1])[2])

def Map(request):
    
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
        
        # color = Color[i].split(' ')
        
        color = Color[i].replace('*','')
        
        if  color == '' :
            color_list.append("#aaaaaa")
            loop_color="#aaaaaa"
           
        else:
            color = (color.split('('))[-1].replace(')','')
 
            loop_color = str(Set_Color((color)))
            color_list.append(loop_color)
        
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
    # Set_Color_info(color_list)
    regions = Region.objects.all()
    contex = {
        "popup_message" :'hello world',
        #  "circule_poses":[[35.6926, 51.40000],[35.6926, 51.40110],[35.6926, 51.45000],[35.6926, 51.46000]],
        "circule_poses":[points_list],
        "circule_color":color_list,
        "circule_messages" : Messages, 
        "marker_poses":[35.7600,51.5200],
        "regions":regions,
        "range" :range(len(regions)),
    }
    print(len([points_list]))
    return render(request,'map.html',contex)


# def Insert_info(request):
#     form = PointForm(request.POST or None)
#     context ={}
#     if form.is_valid():
#         form.save()
   
   
#     context['form']= form
#     return render(request, "create_view.html", context)


# here store data form csv file in database
def Data(request):
    # get info of points like distribution and finally store in database as model color info
    info_path = os.path.join("map","CSV","SigPow.csv")
    dict_from_csv_info = pd.read_csv('map//CSV//SigPow.csv', header=None, index_col=0, squeeze=True)
    # color_code_in = list(dict_from_csv_info[1].keys())
    # color_in = list(dict_from_csv_info[1].keys())
    # color_in = list(dict_from_csv_info[1].keys())
  
    # idx = ['Color', 'Name', 'Count', 'Distance', 'Distribution']
    # result = sr.str.decode(encoding = 'UTF-8')
    # sr.index = idx
    # result = sr.str.decode(encoding = 'ASCII')

    # get position and some parameter of points in database as model points info
    dict_from_csv_points = pd.read_csv('data//RSSI.csv', header=None, index_col=0, squeeze=True).to_dict()
    # print(dict_from_csv_points)
    Time = list(dict_from_csv_points[1].keys())
    Node = list(dict_from_csv_points[1].values())
    latitude = list(dict_from_csv_points[2].values())
    longitude = list(dict_from_csv_points[3].values())
    technology = list(dict_from_csv_points[4].values())
    ARFCN = list(dict_from_csv_points[5].values())
    code = list(dict_from_csv_points[6].values())
    PLMNID = list(dict_from_csv_points[7].values())
    LAC = list(dict_from_csv_points[8].values())
    Color = list(dict_from_csv_points[13].values())
    CellID = list(dict_from_csv_points[9].values())
    Scan = list(dict_from_csv_points[10].values())
    Power = list(dict_from_csv_points[11].values())
    Quality = list(dict_from_csv_points[12].values())
    region = Region.objects.get(region_name = "tehranpars")

    for i in range(1,len(latitude)) :
        loop_color = ''
        if '*' in Power[i]:
            continue
        # color = Color[i].split(' ')
        
        color = Color[i].replace('*','')
        
        if  color == '' :
            color_list.append("#aaaaaa")
            loop_color="#aaaaaa"
           
        else:
            color = (color.split('('))[-1].replace(')','')
            loop_color = str(Set_Color((color)))
            color_list.append(loop_color)

        Point_Info.objects.create(parameter="RSSI",time = Time[i],node = Node[i],latitude = latitude[i],longitude = longitude[i],technology = technology[i],arfcn = ARFCN[i],code = code[i],plmnId = PLMNID[i],
        lac = LAC[i],color = loop_color,cellId = CellID[i],scan = Scan[i],power = Power[i],quality = Quality[i],region =region)
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
import re
def Set_Color(color_val):
    colors_dict = {"#00703c":"Excellent","#00a032":"Very Good","#00d228":"Good","#ffff00":"Fair",
    "#ffaa00":"Poor","#fa6400":"Very Poor","#ff0000":"Bad",
    "#dc143c":"Very Bad","#820000":"Awful","#aaaaaa":"No Coverage","#000000":"Null","#ffffff":"Total"}
    keys = [k for k, v in colors_dict.items() if v == color_val]
    print(keys)
    print(color_val)
    return keys[0]

def test(request):
    return render(request,'index.html')


def RSRP(request):
    
    colors = []
    points = Point_Popup("RSRP")
    # print(len(points["circule_poses"][0]))
    # Set_Color_info(color_list)
    # data = pd.read_csv('map//RSRP.csv', header=None, index_col=0, squeeze=True).to_dict()
   
     # fix len should be filter\
    #
    #
    statics = Static_Info.objects.filter(parameter = "RSRP")
    context = {
        'info' : Color_Info.objects.filter(parameter = "RSRP").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "RSRP"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    # context.update('rsrp_static','dscvfcd')
    # temp = send_data()
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
    # print(context["circule_poses"])
    return render(request, 'RSRP.html',context=context)
def RSSI(request):
    
    colors = []
    points = Point_Popup("RSSI")
    # print(len(points["circule_poses"][0]))
    # Set_Color_info(color_list)
    # data = pd.read_csv('map//RSRP.csv', header=None, index_col=0, squeeze=True).to_dict()
   
     # fix len s    hould be filter\
    #
    #
    statics = Static_Info.objects.filter(parameter = "RSSI")
    context = {
        'info' : Color_Info.objects.filter(parameter = "RSSI").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "RSSI"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    # context.update('rsrp_static','dscvfcd')
    # temp = send_data()
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
    # print(context["circule_poses"])
    return render(request, 'RSSI.html',context=context)

def PingTest(request):
    
    
    points = Point_Popup("test-ping")
    # Set_Color_info(color_list)
    # data = pd.read_csv('map//RSRP.csv', header=None, index_col=0, squeeze=True).to_dict()
    l = [1]
    # fix len should be filter\
    #
    #
    #
    statics = Static_Info.objects.filter(parameter = "test-ping")
    context = {
        'info' :Color_Info.objects.filter(parameter = "test-ping").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'l':l
       
        
    }
    # context.update('rsrp_static','dscvfcd')
    # temp = send_data()
    context.update(points)
    return render(request, 'test//ping.html',context=context)


def QoE(request):
    
    
    points = Point_Popup("test-QoE")
    # Set_Color_info(color_list)
    # data = pd.read_csv('map//RSRP.csv', header=None, index_col=0, squeeze=True).to_dict()
    l = [1]
    statics = Static_Info.objects.filter(parameter = "test-QoE")
    context = {
        'info' :Color_Info.objects.filter(parameter = "test-QoE").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,      
        
    }
    # context.update('rsrp_static','dscvfcd')
    # temp = send_data()
    context.update(points)
    return render(request, 'test//ping.html',context=context)
def Technology(request):
    color_list_technology = []
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []
    print((points_info))
    # create location list
    for i in range(len(points_info)) :
        l = []
        if points_info[i].technology == "4G":

            list_color.append("#0008ff")
        elif points_info[i].technology == "3G":

            list_color.append("#ff00e6")
        elif points_info[i].technology == "2G":

            list_color.append("#00ffff")
        else:
            list_color.append("#32cd32")
            

        message = "Time : "+str(points_info[i].time)+"//"+"Loc : ("+str(points_info[i].latitude)+"/"+str(points_info[i].longitude)+")"+"//"+"Node id : "+str(points_info[i].node)+"//"+"-------------------------------"+"//"+"Technology : "+str(points_info[i].technology)+"//"+"ARFCN : "+str(points_info[i].arfcn)+"//"+"Code : "+str(points_info[i].code)+"//"+"PLMNID : "+str(points_info[i].plmnId)+"//"+"LAC : "+str(points_info[i].lac)+"//"+"Cell id : "+str(points_info[i].cellId)+"//"+"Scan Tech : "+str(points_info[i].scan)+"//"+"Power : "+str(points_info[i].power)+"//"+"Quality : "+str(points_info[i].quality)+"//"+"-------------------------------"+"//"+"Color : "+str(points_info[i].color)
        l.append(float(points_info[i].latitude))
        l.append(float(points_info[i].longitude))
        points_list.append(l)
        Messages.append(message)
    l = [1]

    context = {
        'info' :Color_Info.objects.filter(parameter = "technology").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l':l,
        "circule_poses":[points_list],
        "circule_color":list_color,
        "circule_messages" : Messages, 
       "marker_poses":[35.7600,51.5200],
        
    }
    
    return render(request, 'TechnologyInfo.html',context=context)

def ARFCN(request):
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []

    for i in range(len(points_info)) :
        l = []
        if points_info[i].technology == "4G":

            list_color.append("#0008ff")
        elif points_info[i].technology == "3G":

            list_color.append("#ff00e6")
        elif points_info[i].technology == "2G":

            list_color.append("#00ffff")
        else:
            list_color.append("#32cd32")
            

        message = "Time : "+str(points_info[i].time)+"//"+"Loc : ("+str(points_info[i].latitude)+"/"+str(points_info[i].longitude)+")"+"//"+"Node id : "+str(points_info[i].node)+"//"+"-------------------------------"+"//"+"Technology : "+str(points_info[i].technology)+"//"+"ARFCN : "+str(points_info[i].arfcn)+"//"+"Code : "+str(points_info[i].code)+"//"+"PLMNID : "+str(points_info[i].plmnId)+"//"+"LAC : "+str(points_info[i].lac)+"//"+"Cell id : "+str(points_info[i].cellId)+"//"+"Scan Tech : "+str(points_info[i].scan)+"//"+"Power : "+str(points_info[i].power)+"//"+"Quality : "+str(points_info[i].quality)+"//"+"-------------------------------"+"//"+"Color : "+str(points_info[i].color)
        l.append(float(points_info[i].latitude))
        l.append(float(points_info[i].longitude))
        points_list.append(l)
        Messages.append(message)
    l = [1]

    context = {
        'info' :Table.objects.filter(parameter = "ARFCN").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l':l,
        "circule_poses":[points_list],
        "circule_color":list_color,
        "circule_messages" : Messages, 
       "marker_poses":[35.7600,51.5200],
        
    }
    # context.update('rsrp_static','dscvfcd')
    # temp = send_data()
    
    return render(request, 'ARFCN.html',context=context)

def Code(request):
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []

    for i in range(len(points_info)) :
        l = []
        if points_info[i].technology == "4G":

            list_color.append("#0008ff")
        elif points_info[i].technology == "3G":

            list_color.append("#ff00e6")
        elif points_info[i].technology == "2G":

            list_color.append("#00ffff")
        else:
            list_color.append("#32cd32")
            

        message = "Time : "+str(points_info[i].time)+"//"+"Loc : ("+str(points_info[i].latitude)+"/"+str(points_info[i].longitude)+")"+"//"+"Node id : "+str(points_info[i].node)+"//"+"-------------------------------"+"//"+"Technology : "+str(points_info[i].technology)+"//"+"ARFCN : "+str(points_info[i].arfcn)+"//"+"Code : "+str(points_info[i].code)+"//"+"PLMNID : "+str(points_info[i].plmnId)+"//"+"LAC : "+str(points_info[i].lac)+"//"+"Cell id : "+str(points_info[i].cellId)+"//"+"Scan Tech : "+str(points_info[i].scan)+"//"+"Power : "+str(points_info[i].power)+"//"+"Quality : "+str(points_info[i].quality)+"//"+"-------------------------------"+"//"+"Color : "+str(points_info[i].color)
        l.append(float(points_info[i].latitude))
        l.append(float(points_info[i].longitude))
        points_list.append(l)
        Messages.append(message)
    l = [1]

    context = {
        'info' :Table.objects.filter(parameter = "Code").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l':l,
        "circule_poses":[points_list],
        "circule_color":list_color,
        "circule_messages" : Messages, 
       "marker_poses":[35.7600,51.5200],
        
    }
    # context.update('rsrp_static','dscvfcd')
    # temp = send_data()
    
    return render(request, 'Code.html',context=context)

def DNS(request):
    points = Point_Popup("RSRP")
    # Set_Color_info(color_list)
    # data = pd.read_csv('map//RSRP.csv', header=None, index_col=0, squeeze=True).to_dict()
    l = [1]
    statics = Static_Info.objects.filter(parameter = "RSRP")
    context = {
        'info' :Color_Info.objects.filter(parameter = "RSRP").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'object':Region.objects.all(),
        'l':l
       
        
    }
    # context.update('rsrp_static','dscvfcd')
    # temp = send_data()
    context.update(points)
    return render(request, 'DNS.html',context=context)

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
   
def set_color_info(request):
    data = pd.read_csv('data//Ping.csv',header=None,squeeze=True,index_col=0).to_dict()
    for i in data.values():
        break
    return HttpResponse(data)
   

def send_data(prameter):
    points_info = Point_Info.objects.filter(parameter = prameter)
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
    # Set_Color_info(color_list)
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
    counts = InsertColorInfoTechnology()
    context = {
        'info' :Color_Info.objects.all().distinct(),
        'len': len(list(Color_Info.objects.all())),
        '2G' :counts[0],
        '3G':counts[1],
        '4G':counts[2],
        '5G' :counts[3]

    }
    return render(request,'test_circle_chart.html',context)

def update_points(request):
    # points = Point_Info.objects.all().update(region = "tehranpars")
    points = Table.objects.filter(parameter = "Code").update(parameter = "CellId")
    return HttpResponse("updated")
import pickle

def Point_Popup(prameter):
    
    points_list = []
    Messages = []
    color_list = []
    contex = {}
    r = redis.Redis(host='localhost', port=6379, db=0)
    if r.get("context"+prameter) == None:  
        points_info = Point_Info.objects.filter(parameter = prameter)     
         # create location list with messages
        for i in range(len(points_info)) :
            l = []
            color_list.append(points_info[i].color)
        
            message = "Time : "+str(points_info[i].time)+"//"+"Loc : ("+str(points_info[i].latitude)+"/"+str(points_info[i].longitude)+")"+"//"+"Node id : "+str(points_info[i].node)+"//"+"-------------------------------"+"//"+"Technology : "+str(points_info[i].technology)+"//"+"ARFCN : "+str(points_info[i].arfcn)+"//"+"Code : "+str(points_info[i].code)+"//"+"PLMNID : "+str(points_info[i].plmnId)+"//"+"LAC : "+str(points_info[i].lac)+"//"+"Cell id : "+str(points_info[i].cellId)+"//"+"Scan Tech : "+str(points_info[i].scan)+"//"+"Power : "+str(points_info[i].power)+"//"+"Quality : "+str(points_info[i].quality)+"//"+"-------------------------------"+"//"+"Color : "+str(points_info[i].color)
            l.append(float(points_info[i].latitude))
            l.append(float(points_info[i].longitude))
            points_list.append(l)
            Messages.append(message)
        contex = {
        "popup_message" :'hello world',
        "circule_poses":[points_list],
        "circule_color":color_list,
        "circule_messages" : Messages, 
        "marker_poses":[35.7600,51.5200]
        
    }
        # r.set("Messages",''.join(map(str,Messages)))
        # t = ''.join(map(str,Messages))
        # temp_str_Messages = "Messages"+prameter
        # temp_str_pints = "points"+prameter
        # temp_str_color = "color"+prameter
        # r.set(temp_str_Messages,str(Messages))
        # r.set(temp_str_pints,str(points_list))
        # r.set(temp_str_color,str(color_list))
        # print()
        # l = bytes([Messages,points_list,color_list])
        # print(r.get(temp_str_Messages))
        # print(r.get(temp_str_color))
        # r.lpush(prameter,r.lpop("Messages"))
        r.set("context"+prameter,pickle.dumps(contex))
        print("from DB")
    else:
        # print(r.lpop("Messages"))

        # Messages = list(r.get("Messages"+prameter))
        # points_list = list(r.get("points"+prameter))
        # color_list = list(r.get("color"+prameter))
        # print(Messages)
    # Set_Color_info(color_list)
        contex = pickle.loads(r.get("context"+prameter))
    return contex


def Redis(request):
    r = redis.Redis(host='localhost', port=6379, db=0)
    # pipe = r.pipeline()
    # pipe.set('foo', 'bar')
    # pipe.get('foo')
    # context =  Point_Popup("RSRP")
    # print(context)
    # print((r.get("Messages").decode('UTF-8')))
    # r.delete("RSRP")
    # st = str(r.get("pointsRSRP"))
    # op = st.strip('][').split(', ')
    # print(op[1])
    print(pickle.loads(r.get("contextRSRP"))["circule_messages"][2])
    return HttpResponse(pickle.loads(r.get("contextRSRP")))



def update(request):
    names = ["EXCELLENT","VERY GOOD","GOOD","FAIR","POOR","VERY POOR","BAD",
    "Very Bad","Awful","No Coverage","Null","Total"]
    ranges = Ranges.objects.filter(parameter="RSRP")
    j = 0
    for i in ranges:
        i.name = names[j]
        j+=1
        # Ranges.objects.update(i)
        i.save()
    return HttpResponse("done")

def insert_static_info(request):
    dict_from_csv = pd.read_csv('data//info_SigRSSI.csv', header=None, index_col=0, squeeze=True).to_dict()
    print(dict_from_csv)
    return HttpResponse("done")