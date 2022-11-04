import redis
from time import time
from typing import List
from django.shortcuts import render
from map.models import Ranges, Color_Info, Point_Info,Static_Info
import pickle


color_list = []




def Set_Color(color_val):
    colors_dict = {"#00703c":"Excellent","#00a032":"Very Good","#00d228":"Good","#ffff00":"Fair",
    "#ffaa00":"Poor","#fa6400":"Very Poor","#ff0000":"Bad",
    "#dc143c":"Very Bad","#820000":"Awful","#aaaaaa":"No Coverage","#000000":"Null","#ffffff":"Total"}
    keys = [k for k, v in colors_dict.items() if v == color_val]
    return keys[0]

# TEST
def PingTest(request):
    
    
    points = Point_Popup("RSRQ")

    info_list:List(Color_Info) = []
    names = []
    infos = Color_Info.objects.filter(parameter = "Map-Data Test-Delay-Ping--.csv").distinct()
    for info in infos:
        if info.name not in names:
            info_list.append(info)
            names.append(info.name)
            
    statics = Static_Info.objects.filter(parameter = "Map-Data Test-Delay-Ping--.csv")
    context = {
        'info' : info_list,
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "Map-Data Test-Delay-Ping--.csv"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
    return render(request, 'test_map.html',context=context)

def QoE(request):

    points = Point_Popup("RSRQ")

    info_list:List(Color_Info) = []
    names = []
    infos = Color_Info.objects.filter(parameter = "Map-Data Test-Delay-Jitter--.csv").distinct()
    for info in infos:
        if info.name not in names:
            info_list.append(info)
            names.append(info.name)
            
    statics = Static_Info.objects.filter(parameter = "Map-Data Test-Delay-Jitter--.csv")
    context = {
        'info' : info_list,
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "Map-Data Test-Delay-Jitter--.csv"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
    return render(request, 'test_map.html',context=context)

def DownLink(request):
    points = Point_Popup("RSRQ")
    print("sdjcbxknm")
    info_list:List(Color_Info) = []
    names = []
    infos = Color_Info.objects.filter(parameter = "Map-Data Test-Throughput-Download--.csv").distinct()
    for info in infos:
        if info.name not in names:
            info_list.append(info)
            names.append(info.name)
            
    statics = Static_Info.objects.filter(parameter = "Map-Data Test-Throughput-Download--.csv")
    context = {
        'info' : info_list,
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "Map-Data Test-Throughput-Download--.csv"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
    return render(request, 'test_map.html',context=context)


def DNS(request):
    points = Point_Popup("RSRQ")

    info_list:List(Color_Info) = []
    names = []
    infos = Color_Info.objects.filter(parameter = "Map-Data Test-DNS-A Records--.csv").distinct()
    for info in infos:
        if info.name not in names:
            info_list.append(info)
            names.append(info.name)
            
    statics = Static_Info.objects.filter(parameter = "Map-Data Test-DNS-A Records--.csv")
    context = {
        'info' : info_list,
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "Map-Data Test-DNS-A Records--.csv"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
    return render(request, 'test_map.html',context=context)


#check if in redis get from redis else get from db
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
        r.set("context"+prameter,pickle.dumps(contex))
        print("from DB")
    else:
        print("redis")
        contex = pickle.loads(r.get("context"+prameter))
    return contex
