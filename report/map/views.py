from statistics import variance
import redis
from time import time


from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
import json


from .models import Ranges, Color_Info, Point_Info, Region,Static_Info,Table,Result_Table
import datetime
import pandas as pd
import os
import pickle


color_list = []

def InsertColorInfoTechnology():
    dict_from_csv = pd.read_csv('data//serving.csv', header=None, index_col=0, squeeze=True)
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
    dict_from_csv = pd.read_csv('data//data.csv', header=None, index_col=0, squeeze=True).to_dict()

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

def RSRQ(request):
    points = Point_Popup("RSRQ")
    statics = Static_Info.objects.filter(parameter = "RSRQ")
    context = {
        'info' : Color_Info.objects.filter(parameter = "RSRQ").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "RSRQ"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
    return render(request, 'map/RSRQ.html',context=context)
    
def RSSI(request):

    points = Point_Popup("RSSI")
    statics = Static_Info.objects.filter(parameter = "RSSI")
    context = {
        'info' : Color_Info.objects.filter(parameter = "RSSI").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'ranges':Ranges.objects.filter(parameter = "RSSI"),
        "marker_poses":[35.7600,51.5200],
       
        
    }
    context.update(points)
    temp =points["circule_poses"][0]
    context.update({"circule_poses":[temp]})
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

    context = {
        'info' :Table.objects.filter(parameter = "code").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l':l,
        "circule_poses":[points_list],
        "circule_messages" : Messages, 
       "marker_poses":[35.7600,51.5200],
        
    }  
    return render(request, 'Code.html',context=context)
def ARFCN_Code(request):
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
        'info' :Table.objects.filter(parameter = "Arfcn-Code").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l':l,
        "circule_poses":[points_list],
        "circule_color":list_color,
        "circule_messages" : Messages, 
       "marker_poses":[35.7600,51.5200],
        
    }
    return render(request, 'map/ARFCN_Code.html',context=context)


def Cell_Id(request):
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
        'info' :Table.objects.filter(parameter = "Cell_Id").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l':l,
        "circule_poses":[points_list],
        "circule_color":list_color,
        "circule_messages" : Messages, 
       "marker_poses":[35.7600,51.5200],
        
    }
    return render(request, 'map/ARFCN_Code.html',context=context)    


def PLMN_Id(request):
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
        'info' :Table.objects.filter(parameter = "PLMN_Id").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l':l,
        "circule_poses":[points_list],
        "circule_color":list_color,
        "circule_messages" : Messages, 
       "marker_poses":[35.7600,51.5200],
        
    }
    return render(request, 'map/PLMN.html',context=context)    
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
def Scan_result_cell(request):
   
    
    context = {
        'info' :Result_Table.objects.filter(parameter = "first").distinct(),
        
        
    }
    return render(request, 'producer//scan_result.html',context=context)
def Scan_result_neighbor(request):
   
    
    context = {
        'info' :Result_Table.objects.filter(parameter = "second").distinct(),
        
        
    }
    return render(request, 'producer//scan_result.html',context=context)

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
    return render(request,'map/index.html')

def test_line_chart(request):
    return render(request,'test_line_chart.html')

def test_circle_chart(request):
    counts = InsertColorInfoTechnology()
    context = {
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
    dict_from_csv = pd.read_csv('data//PLMN_Id.csv', header=None).to_dict()
    color_code = list(dict_from_csv[0].values())
    color_name = list(dict_from_csv[1].values())
    count_color = list(dict_from_csv[2].values())
    distance = list(dict_from_csv[3].values())
    distribution = list(dict_from_csv[4].values())
    for i in range(1,len(color_code)):
        Table.objects.create(parameter = "PLMN_Id",name = color_name[i],count = count_color[i]
        ,color =color_code[i],distance = distance[i],distribution=distribution[i])
    
    return HttpResponse("done")

def insert_table_result(request):
    dict_from_csv = pd.read_csv('data//ScansTableNeighbor4G.csv', header=None).to_dict()
    # print(dict_from_csv)
    count = list(dict_from_csv[0].values())
    timestamp = list(dict_from_csv[1].values())
    tech = list(dict_from_csv[2].values())
    arfcn = list(dict_from_csv[3].values())
    pci = list(dict_from_csv[4].values())
    plmn_id = list(dict_from_csv[5].values())
    rsrp = list(dict_from_csv[6].values())
    rsrq = list(dict_from_csv[7].values())
    rssi = list(dict_from_csv[8].values())
    sinr = list(dict_from_csv[9].values())
    for i in range(1,len(count)):
        Result_Table.objects.create(parameter = "second",count=count[i],timestamp=timestamp[i],tech=tech[i],arfcn=arfcn[i],pci=pci[i],plmn_id=plmn_id[i]
        ,sinr_result=int(sinr[i][8:]),sinr_color=sinr[i][0:7],rsrp_color = rsrp[i][0:7],rsrp_result = rsrp[i][8:],rsrq_color = rsrq[i][0:7],rsrq_result=rsrq[i][8:],rssi_color=rssi[i][0:7],
        rssi_result=rssi[i][8:] )
    
    return HttpResponse("done")



def ReadPointInfoData(request):
    directory = os.path.join(os.getcwd(),"data/datas")
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f=open(os.path.join(directory,file), 'r')
                for data in f :
                    data = data.split('@')
                    #jump from first data
                    if data[0]== "Timestamp":
                        continue
                    Time = (data[0])
                    Node = (data[1])
                    latitude = (data[2])
                    longitude = (data[3])
                    technology = (data[4])
                    ARFCN = (data[5])
                    code = (data[6])
                    PLMNID = (data[7])
                    LAC = (data[8])
                    CellID = (data[9])
                    Sig_tech = (data[10])
                    Power = (data[11])
                    Quality = (data[12])
                    Color = (data[13])

                    for i in range(1,len(latitude)) :
                        loop_color = ''
                        if '*' in Power:
                            continue
                        
                        color = Color.replace('*','')
                        if  color == '' :
                            color_list.append("#aaaaaa")
                            loop_color="#aaaaaa"
                        
                        else:
                            color = (color.split('('))[-1].replace(')','')
                            loop_color = str(Set_Color((color)))
                            color_list.append(loop_color)
                        # TODO set file name as parameter name
                        Point_Info.objects.create(parameter=file,time = Time,node = Node,latitude = latitude,longitude = longitude,
                        technology = technology,arfcn = ARFCN,code = code,plmnId = PLMNID,
                        lac = LAC,color = loop_color,cellId = CellID,scan = Sig_tech,power = Power,quality = Quality)
                f.close()
    return HttpResponse("done")

def ReadColorInfoData(request):
    directory = os.path.join(os.getcwd(),"data/datas/legend")
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f=open(os.path.join(directory,file), 'r')
                for data in f :
                    data = data.split('@')
                    #jump from first data
                    print(data)
                    if data[0]== "Color":
                        continue
                    color = (data[0])
                    name = str(data[1])
                    count = (data[2])
                    distance = (data[3])
                    distribution = (data[4])
                    tech=None
                    
                    try:
                      tech = (data[5])
                    except:
                        tech= ''

                    if data[1]=="Total":
                        count=data[2].split(' ')[0]
                        distance=data[3].split(' ')[0]
                        distribution=data[4].split(' ')[0]

                    # TODO set file name as parameter name
                    Color_Info.objects.create(parameter=file,color_range=color,name=name,count=count,distance=distance,
                    distribution=distribution,tech=tech)
                f.close()
    return HttpResponse("done")

def ReadTestTableData(request):
    directory = os.path.join(os.getcwd(),"data/datas/table")
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f=open(os.path.join(directory,file), 'r')
                for data in f :
                    data = data.split('@')
                    #jump from first data
                    if len(data)>10 and len(data)<13:
                        if data[0]== "Count":
                            continue
                        count = (data[0])
                        timestamp = (data[1])
                        tech = (data[2])
                        band= data[3]
                        arfcn = (data[4])
                        pci = (data[5])
                        plmn_id = (data[6])
                        rsrp = (data[7])
                        rsrq = (data[8])
                        rssi = (data[9])
                        sinr = (data[10])
                        print(rsrp)
                        print(rsrq)
                        Result_Table.objects.create(parameter = file,count=count,timestamp=timestamp,tech=tech,band=band,arfcn=arfcn,pci=pci,plmn_id=plmn_id
                        ,sinr_result=int(sinr[8:]),sinr_color=sinr[0:7],rsrp_color = rsrp[0:7],rsrp_result = rsrp[8:],rsrq_color = rsrq[0:7],rsrq_result=rsrq[8:],rssi_color=rssi[0:7],
                        rssi_result=rssi[8:] )

                f.close()
    return HttpResponse("done")


def ReadStaticData(request):
    directory = os.path.join(os.getcwd(),"data/datas/static")
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f=open(os.path.join(directory,file), 'r')
                for data in f :
                    data = data.split('@')
                    #jump from first data
                if data[0]=="Count":
                    continue
                count = (data[0])
                mean = (data[1])
                max = (data[2])
                min= data[3]
                median = (data[4])
                mode = (data[5])
                std = (data[6])
                variance = (data[7])
                ci=str(data[8] )      

                Static_Info.objects.create(parameter = file,count=count,mean=mean,max=max,min=min,median=median,mode=mode,
                std=std,variance=variance,ci=ci)

                f.close()
    return HttpResponse("done")

def ReadRangeData(request):
    directory = os.path.join(os.getcwd(),"data/datas/info")
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f=open(os.path.join(directory,file), 'r')
                for data in f :
                    data = data.split('@')
                    print(data)
                    #jump from first data
                    if data[0]=="Color":
                        continue
                    tech=None
                    if len(data)==4:
                        color = (data[0])
                        name = (data[1])
                        tech = data[2]
                        rang = (data[3])
                    
                    else:
                        color = (data[0])
                        name = (data[1])
                        rang = (data[2])
                    Ranges.objects.create(parameter = file,name=name,rang= rang,color=color,tech=tech)

                f.close()
    return HttpResponse("done")