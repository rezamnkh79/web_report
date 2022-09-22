import redis
from typing import List

from django.http import HttpResponse
import pandas as pd
import os
import pickle

from django.conf import settings

from pathlib import Path
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'report.settings')
from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

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
    else:
        contex = pickle.loads(r.get("context" + prameter))
    return contex


def Redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
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


def ReadPointInfoData():
    directory = os.path.join(os.getcwd(), "data/datas/datas")
    # r = redis.Redis(host='localhost', port=6379, db=0)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                # TODO delete file name from catch
                # r.delete(file)
                f = open(os.path.join(directory, file), 'r')
                for data in f:
                    data = data.split(',')
                    # jump from first data
                    if data[0] == "Timestamp":
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
                    for i in range(1, len(latitude)):
                        loop_color = ''
                        if '*' in Power:
                            continue

                        color = Color.replace('*', '')
                        if color == '':
                            color_list.append("#aaaaaa")
                            loop_color = "#aaaaaa"

                        else:
                            color = (color.split('('))[-1].replace(')', '')
                            loop_color = str(Set_Color((color)))
                            color_list.append(loop_color)
                        # TODO set file name as parameter name
                        Point_Info.objects.create(parameter=file, time=Time, node=Node, latitude=latitude,
                                                  longitude=longitude,
                                                  technology=technology, arfcn=ARFCN, code=code, plmnId=PLMNID,
                                                  lac=LAC, color=loop_color, cellId=CellID, scan=Sig_tech, power=Power,
                                                  quality=Quality)
                f.close()
    return HttpResponse("done")


def ReadColorInfoData():
    directory = os.path.join(os.getcwd(), "data/datas/legend")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                # TODO delete file name from catch
                f = open(os.path.join(directory, file), 'r')
                for data in f:
                    data = data.split('@')
                    # jump from first data
                    if data[0] == "Color":
                        continue
                    color = (data[0])
                    name = str(data[1])
                    count = (data[2])
                    distance = (data[3])
                    distribution = (data[4])
                    tech = None
                    band = None
                    freq = None
                    try:
                        tech = (data[5])
                    except:
                        tech = ''
                    try:
                        band = (data[6])
                    except:
                        band = ''
                    try:
                        freq = (data[7])
                    except:
                        freq = ''

                    if data[1] == "Total":
                        count = data[2].split(' ')[0]
                        distance = data[3].split(' ')[0]
                        distribution = data[4].split(' ')[0]

                    # TODO set file name as parameter name
                    Color_Info.objects.create(parameter=file, color_range=color, name=name, count=count,
                                              distance=distance,
                                              distribution=distribution, tech=tech, band=band, freq=freq)
                f.close()
    return HttpResponse("done")


def ReadTestTableData():
    directory = os.path.join(os.getcwd(), "data/datas/table")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                # TODO delete file name from catch
                f = open(os.path.join(directory, file), 'r')
                for data in f:
                    data = data.split('@')
                    # jump from first data
                    if len(data) > 10 and len(data) < 13:
                        if data[0] == "Count":
                            continue
                        count = (data[0])
                        timestamp = (data[1])
                        tech = (data[2])
                        band = data[3]
                        arfcn = (data[4])
                        pci = (data[5])
                        plmn_id = (data[6])
                        rsrp = (data[7])
                        rsrq = (data[8])
                        rssi = (data[9])
                        sinr = (data[10])
                        Result_Table.objects.create(parameter=file, count=count, timestamp=timestamp, tech=tech,
                                                    band=band, arfcn=arfcn, pci=pci, plmn_id=plmn_id
                                                    , sinr_result=int(sinr[8:]), sinr_color=sinr[0:7],
                                                    rsrp_color=rsrp[0:7], rsrp_result=rsrp[8:], rsrq_color=rsrq[0:7],
                                                    rsrq_result=rsrq[8:], rssi_color=rssi[0:7],
                                                    rssi_result=rssi[8:])

                f.close()
    return HttpResponse("done")


def ReadStaticData():
    directory = os.path.join(os.getcwd(), "data/datas/static")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f = open(os.path.join(directory, file), 'r')
                for data in f:
                    data = data.split('@')
                    # jump from first data
                if data[0] == "Count":
                    continue
                count = (data[0])
                mean = (data[1])
                max = (data[2])
                min = data[3]
                median = (data[4])
                mode = (data[5])
                std = (data[6])
                variance = (data[7])
                ci = str(data[8])

                Static_Info.objects.create(parameter=file, count=count, mean=mean, max=max, min=min, median=median,
                                           mode=mode,
                                           std=std, variance=variance, ci=ci)

                f.close()
    return HttpResponse("done")


def ReadRangeData():
    directory = os.path.join(os.getcwd(), "data/datas/info")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                f = open(os.path.join(directory, file), 'r')
                for data in f:
                    data = data.split('@')
                    # jump from first data
                    if data[0] == "Color":
                        continue
                    tech = None
                    if len(data) == 4:
                        color = (data[0])
                        name = (data[1])
                        tech = data[2]
                        rang = (data[3])

                    else:
                        color = (data[0])
                        name = (data[1])
                        rang = (data[2])
                    Ranges.objects.create(parameter=file, name=name, rang=rang, color=color, tech=tech)

                f.close()
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


if __name__ == "__main__":
    Color_Info.objects.all().delete()
    Table.objects.all().delete()
    Static_Info.objects.all().delete()
    Ranges.objects.all().delete()
    ReadPointInfoData()
    ReadRangeData()
    ReadStaticData()
    ReadTestTableData()
    ReadColorInfoData()
