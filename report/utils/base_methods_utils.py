import os
import redis
from typing import List

from django.http import HttpResponse
import pandas as pd
import pickle
from django.shortcuts import render
from map.models import *

color_list = []


def InsertColorInfoTechnology():
    dict_from_csv = pd.read_csv('data//serving.csv', header=None, index_col=0, squeeze=True)
    count3G = 0
    count2G = 0
    count4G = 0
    count5G = 0
    for i in list(dict_from_csv[5]):
        if i == 4:
            count4G += 1
        elif i == 2:
            count2G += 1
        elif i == 3:
            count3G += 1
        else:
            count5G += 1

    count2G = int(count2G / len(list(dict_from_csv[5])) * 100)
    count3G = int(count3G / len(list(dict_from_csv[5])) * 100)
    count4G = int(count4G / len(list(dict_from_csv[5])) * 100)
    count5G = int(count5G / len(list(dict_from_csv[5])) * 100)
    return ([count2G, count3G, count4G, count5G])


def Set_Color(color_val):
    colors_dict = {"#00703c": "Excellent", "#00a032": "Very Good", "#00d228": "Good", "#ffff00": "Fair",
                   "#ffaa00": "Poor", "#fa6400": "Very Poor", "#ff0000": "Bad",
                   "#dc143c": "Very Bad", "#820000": "Awful", "#aaaaaa": "No Coverage", "#000000": "Null",
                   "#ffffff": "Total"}
    keys = [k for k, v in colors_dict.items() if v == color_val]
    return keys[0]


def Point_Popup(prameter):
    points_list = []
    Messages = []
    color_list = []
    contex = {}
    r = redis.Redis(host='localhost', port=6379, db=0)
    if r.get("context" + prameter) == None:

        points_info = Point_Info.objects.filter(parameter=prameter)
        # create location list with messages
        for i in range(len(points_info)):
            l = []
            color_list.append(points_info[i].color)

            message = "Time : " + str(points_info[i].time) + "//" + "Loc : (" + str(
                points_info[i].latitude) + "/" + str(points_info[i].longitude) + ")" + "//" + "Node id : " + str(
                points_info[i].node) + "//" + "-------------------------------" + "//" + "Technology : " + str(
                points_info[i].technology) + "//" + "ARFCN : " + str(points_info[i].arfcn) + "//" + "Code : " + str(
                points_info[i].code) + "//" + "PLMNID : " + str(points_info[i].plmnId) + "//" + "LAC : " + str(
                points_info[i].lac) + "//" + "Cell id : " + str(points_info[i].cellId) + "//" + "Scan Tech : " + str(
                points_info[i].scan) + "//" + "Power : " + str(points_info[i].power) + "//" + "Quality : " + str(
                points_info[i].quality) + "//" + "-------------------------------" + "//" + "Color : " + str(
                points_info[i].color)
            l.append(float(points_info[i].latitude))
            l.append(float(points_info[i].longitude))
            points_list.append(l)
            Messages.append(message)
        contex = {
            "popup_message": 'hello world',
            "circule_poses": [points_list],
            "circule_color": color_list,
            "circule_messages": Messages,
            "marker_poses": [35.7600, 51.5200]

        }
        r.set("context" + prameter, pickle.dumps(contex))
        print("from DB")
    else:
        print("redis")
        contex = pickle.loads(r.get("context" + prameter))
    return contex


def Redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    print(pickle.loads(r.get("contextRSRP"))["circule_messages"][2])
    return HttpResponse(pickle.loads(r.get("contextRSRP")))


def update():
    names = ["EXCELLENT", "VERY GOOD", "GOOD", "FAIR", "POOR", "VERY POOR", "BAD",
             "Very Bad", "Awful", "No Coverage", "Null", "Total"]
    ranges = Ranges.objects.filter(parameter="RSRP")
    j = 0
    for i in ranges:
        i.name = names[j]
        j += 1
        i.save()
    return HttpResponse("done")


def insert_static_info():
    dict_from_csv = pd.read_csv('data//PLMN_Id.csv', header=None).to_dict()
    color_code = list(dict_from_csv[0].values())
    color_name = list(dict_from_csv[1].values())
    count_color = list(dict_from_csv[2].values())
    distance = list(dict_from_csv[3].values())
    distribution = list(dict_from_csv[4].values())
    for i in range(1, len(color_code)):
        Table.objects.create(parameter="PLMN_Id", name=color_name[i], count=count_color[i]
                             , color=color_code[i], distance=distance[i], distribution=distribution[i])

    return HttpResponse("done")


def insert_table_result():
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
    for i in range(1, len(count)):
        Result_Table.objects.create(parameter="second", count=count[i], timestamp=timestamp[i], tech=tech[i],
                                    arfcn=arfcn[i], pci=pci[i], plmn_id=plmn_id[i]
                                    , sinr_result=int(sinr[i][8:]), sinr_color=sinr[i][0:7], rsrp_color=rsrp[i][0:7],
                                    rsrp_result=rsrp[i][8:], rsrq_color=rsrq[i][0:7], rsrq_result=rsrq[i][8:],
                                    rssi_color=rssi[i][0:7],
                                    rssi_result=rssi[i][8:])
    return HttpResponse("done")


def computepiechert(parameter):
    total_points = Point_Info.objects.filter(parameter=parameter)
    Very_Good = len(Point_Info.objects.filter(parameter=parameter, color="#00a032 ").values_list('color')) / len(
        total_points)
    Good = len(Point_Info.objects.filter(parameter=parameter, color="#00d228").values_list('color')) / len(total_points)
    Fair = len(Point_Info.objects.filter(parameter=parameter, color="#ffff00").values_list('color')) / len(total_points)
    Poor = len(Point_Info.objects.filter(parameter=parameter, color="#ffaa00").values_list('color')) / len(total_points)
    Bad = len(Point_Info.objects.filter(parameter=parameter, color="#ff0000").values_list('color')) / len(total_points)
    Very_Bad = len(Point_Info.objects.filter(parameter=parameter, color="#dc143c").values_list('color')) / len(
        total_points)
    Awful = len(Point_Info.objects.filter(parameter=parameter, color="#820000 ").values_list('color')) / len(
        total_points)
    No_Coverage = len(Point_Info.objects.filter(parameter=parameter, color="#aaaaaa ").values_list('color')) / len(
        total_points)
    print(Very_Good)
    result = {
        "Very_Good": round(Very_Good * 100, 2),
        "Good": round(Good * 100, 2),
        "Fair": round(Fair * 100, 2),
        "Poor": round(Poor * 100, 2),
        "Bad": round(Bad * 100, 2),
        "Very_Bad": round(Very_Bad * 100, 2),
        "Awful": round(Awful * 100, 2),
        "No_Coverage": round(No_Coverage * 100, 2),
        "Total": total_points,
    }
    return result


def InsertARFNTable():
    dict_from_csv = pd.read_csv('map//Map-Serving Cell-ARFCN_Code---.csv', header=None, index_col=0, squeeze=True)
    for i in range(1, len(list(dict_from_csv[1]))):
        #   table = Table.objects.create(color =list(dict_from_csv[1].keys())[i],name = list(dict_from_csv[1])[i],count = list(dict_from_csv[2])[i],distance = list(dict_from_csv[3])[i],distribution = list(dict_from_csv[4])[i],tech = list(dict_from_csv[5])[i],band = list(dict_from_csv[6])[i],freq =list(dict_from_csv[7])[i])
        table = Table.objects.create(parameter="Arfcn-Code", color=list(dict_from_csv[1].keys())[i],
                                     name=list(dict_from_csv[1])[i], count=list(dict_from_csv[2])[i],
                                     distance=list(dict_from_csv[3])[i], distribution=list(dict_from_csv[4])[i],
                                     tech=list(dict_from_csv[5])[i])

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
    for i in range(1, len(latitude)):
        l = []

        # color = Color[i].split(' ')

        color = Color[i].replace('*', '')

        if color == '':
            color_list.append("#aaaaaa")
            loop_color = "#aaaaaa"

        else:
            color = (color.split('('))[-1].replace(')', '')

            loop_color = str(Set_Color((color)))
            color_list.append(loop_color)

        message = "Time : " + str(Time[i]) + "//" + "Loc : (" + str(latitude[i]) + "/" + str(
            longitude[i]) + ")" + "//" + "Node id : " + str(
            Node[i]) + "//" + "-------------------------------" + "//" + "Technology : " + str(
            technology[i]) + "//" + "ARFCN : " + ARFCN[i] + "//" + "Code : " + code[i] + "//" + "PLMNID : " + PLMNID[
                      i] + "//" + "LAC : " + LAC[i] + "//" + "Cell id : " + str(
            CellID[i]) + "//" + "Scan Tech : " + str(Scan[i]) + "//" + "Power : " + str(
            Power[i]) + "//" + "Quality : " + str(
            Quality[i]) + "//" + "-------------------------------" + "//" + "Color : " + str(Color[i])
        # l.append(format(float(point.latitude),".6f"))
        # l.append(format(float(point.longitude),".6f"))
        l.append(float(latitude[i]))
        l.append(float(longitude[i]))
        points_list.append(l)
        Messages.append(message)
    regions = Region.objects.all()
    contex = {
        "popup_message": 'hello world',
        #  "circule_poses":[[35.6926, 51.40000],[35.6926, 51.40110],[35.6926, 51.45000],[35.6926, 51.46000]],
        "circule_poses": [points_list],
        "circule_color": color_list,
        "circule_messages": Messages,
        "marker_poses": [35.7600, 51.5200],
        "regions": regions,
        "range": range(len(regions)),
    }
    print(len([points_list]))
    return render(request, 'map.html', contex)


# here store data form csv file in database
def Data(request):
    # get info of points like distribution and finally store in database as model color info
    info_path = os.path.join("map", "CSV", "SigPow.csv")
    dict_from_csv_info = pd.read_csv('map//CSV//SigPow.csv', header=None, index_col=0, squeeze=True)

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
    region = Region.objects.get(region_name="tehranpars")

    for i in range(1, len(latitude)):
        loop_color = ''
        if '*' in Power[i]:
            continue
        # color = Color[i].split(' ')

        color = Color[i].replace('*', '')

        if color == '':
            color_list.append("#aaaaaa")
            loop_color = "#aaaaaa"

        else:
            color = (color.split('('))[-1].replace(')', '')
            loop_color = str(Set_Color((color)))
            color_list.append(loop_color)

        Point_Info.objects.create(parameter="RSSI", time=Time[i], node=Node[i], latitude=latitude[i],
                                  longitude=longitude[i], technology=technology[i], arfcn=ARFCN[i], code=code[i],
                                  plmnId=PLMNID[i],
                                  lac=LAC[i], color=loop_color, cellId=CellID[i], scan=Scan[i], power=Power[i],
                                  quality=Quality[i], region=region)
    return HttpResponse("done")


def set_color_info():
    data = pd.read_csv('data//Ping.csv', header=None, squeeze=True, index_col=0).to_dict()
    for i in data.values():
        break
    return HttpResponse(data)
