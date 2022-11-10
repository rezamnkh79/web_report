import redis
from time import time
from typing import List

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import pandas as pd

from .models import Ranges, Color_Info, Point_Info, Region, Static_Info, Table, Result_Table
from utils.base_methods_utils import *


def Map(request):
    return render(request, 'map.html')


color_list = []


def RSRP(request):
    points = Point_Popup("Scan_Neighbor_SigPow.csv")
    statics = Static_Info.objects.filter(parameter="Map-Scan-Neighbor-SigPow-4G-Avg.csv")
    info_list: List[Color_Info] = []
    names = []
    infos = Color_Info.objects.filter(parameter="Map-Scan-Neighbor-SigPow-4G-Avg.csv").distinct()
    for info in infos:
        if info.name not in names:
            info_list.append(info)
            names.append(info.name)
    context = {
        'info': info_list,
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'ranges': Ranges.objects.filter(parameter="Map-Scan-Neighbor-SigPow-4G-Avg.csv"),
        "marker_poses": [35.7600, 51.5200],

    }
    context.update(points)
    temp = points["circule_poses"][0]
    context.update({"circule_poses": [temp]})
    return render(request, 'map/Scans_on_map.html', context=context)


def RSRQ(request):
    points = Point_Popup("RSRQ")

    info_list: List[Color_Info] = []
    names = []
    infos = Color_Info.objects.filter(parameter="Map-Scan-Neighbor-SigQual-4G-Avg.csv").distinct()
    for info in infos:
        if info.name not in names:
            info_list.append(info)
            names.append(info.name)

    statics = Static_Info.objects.filter(parameter="Map-Scan-Neighbor-SigQual-4G-Avg.csv")
    context = {
        'info': info_list,
        'statics': statics,
        'ranges': Ranges.objects.filter(parameter="Map-Scan-Neighbor-SigQual-4G-Avg.csv"),
        "marker_poses": [35.7600, 51.5200],

    }
    context.update(points)
    temp = points["circule_poses"][0]
    context.update({"circule_poses": [temp]})
    return render(request, 'map/Scans_on_map.html', context=context)


def RSSI(request):
    points = Point_Popup("RSSI")
    info_list: List[Color_Info] = []
    names = []
    infos = Color_Info.objects.filter(parameter="Map-Scan-Neighbor-SigRSSI-4G-Avg.csv").distinct()
    for info in infos:
        if info.name not in names:
            info_list.append(info)
            names.append(info.name)
    statics = Static_Info.objects.filter(parameter="Map-Scan-Neighbor-SigRSSI-4G-Avg.csv")
    context = {
        'info': infos,
        'len': len(list(Color_Info.objects.all())),
        'statics': statics,
        'ranges': Ranges.objects.filter(parameter="Map-Scan-Neighbor-SigRSSI-4G-Avg.csv"),
        "marker_poses": [35.7600, 51.5200],

    }
    context.update(points)
    temp = points["circule_poses"][0]
    context.update({"circule_poses": [temp]})
    return render(request, 'map/Scans_on_map.html', context=context)


def Technology(request):
    color_list_technology = []
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []
    # create location list and tech list
    for i in range(len(points_info)):
        l = []
        if points_info[i].technology == "4G":

            list_color.append("#0008ff")
        elif points_info[i].technology == "3G":

            list_color.append("#ff00e6")
        elif points_info[i].technology == "2G":

            list_color.append("#00ffff")
        else:
            list_color.append("#32cd32")

        message = "Time : " + str(points_info[i].time) + "//" + "Loc : (" + str(points_info[i].latitude) + "/" + str(
            points_info[i].longitude) + ")" + "//" + "Node id : " + str(
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
    l = [1]

    # TODO change parameter to file name Map-Serving "Cell-Technology---.csv"
    context = {
        'info': Color_Info.objects.filter(parameter="Map-Serving Cell-Technology---.csv").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l': l,
        "circule_poses": [points_list],
        "circule_color": list_color,
        "circule_messages": Messages,
        "marker_poses": [35.7600, 51.5200],

    }

    return render(request, 'map/TechnologyInfo.html', context=context)


def ARFCN(request):
    # TODO get corroct data from db
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []

    for i in range(len(points_info)):
        l = []

        message = "Time : " + str(points_info[i].time) + "//" + "Loc : (" + str(points_info[i].latitude) + "/" + str(
            points_info[i].longitude) + ")" + "//" + "Node id : " + str(
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

    context = {
        'info': Color_Info.objects.filter(parameter="Map-Serving Cell-ARFCN---.csv").distinct(),
        'len': len(list(Color_Info.objects.all())),
        "circule_poses": [points_list],
        "circule_color": list_color,
        "circule_messages": Messages,
        "marker_poses": [35.7600, 51.5200],

    }
    return render(request, 'map/ARFCN_CODE_table.html', context=context)


def Code(request):
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []

    for i in range(len(points_info)):
        l = []

        message = "Time : " + str(points_info[i].time) + "//" + "Loc : (" + str(points_info[i].latitude) + "/" + str(
            points_info[i].longitude) + ")" + "//" + "Node id : " + str(
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

    context = {
        'info': Color_Info.objects.filter(parameter="Map-Serving Cell-Code---.csv").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'l': l,
        "circule_poses": [points_list],
        "circule_messages": Messages,
        "marker_poses": [35.7600, 51.5200],

    }
    return render(request, 'map/ARFCN_Code.html', context=context)


def ARFCN_Code(request):
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []

    for i in range(len(points_info)):
        l = []
        message = "Time : " + str(points_info[i].time) + "//" + "Loc : (" + str(points_info[i].latitude) + "/" + str(
            points_info[i].longitude) + ")" + "//" + "Node id : " + str(
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
    context = {
        'info': Color_Info.objects.filter(parameter="Map-Serving Cell-ARFCN_Code---.csv").distinct(),
        "circule_poses": [points_list],
        "circule_color": list_color,
        "circule_messages": Messages,
        "marker_poses": [35.7600, 51.5200],

    }
    return render(request, 'map/ARFCN_Code.html', context=context)


def Cell_Id(request):
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []

    for i in range(len(points_info)):
        l = []
        message = "Time : " + str(points_info[i].time) + "//" + "Loc : (" + str(points_info[i].latitude) + "/" + str(
            points_info[i].longitude) + ")" + "//" + "Node id : " + str(
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

    context = {
        'info': Color_Info.objects.filter(parameter="Map-Serving Cell-Cell Id---.csv").distinct(),
        'len': len(list(Color_Info.objects.all())),
        "circule_poses": [points_list],
        "circule_color": list_color,
        "circule_messages": Messages,
        "marker_poses": [35.7600, 51.5200],

    }
    return render(request, 'map/ARFCN_Code.html', context=context)


def PLMN_Id(request):
    points_info = Point_Info.objects.all().distinct()
    points_list = []
    Messages = []
    list_color = []

    for i in range(len(points_info)):
        l = []

        message = "Time : " + str(points_info[i].time) + "//" + "Loc : (" + str(points_info[i].latitude) + "/" + str(
            points_info[i].longitude) + ")" + "//" + "Node id : " + str(
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
    l = [1]

    context = {
        'info': Color_Info.objects.filter(parameter="Map-Serving Cell-PLMN Id---.csv").distinct(),
        "circule_poses": [points_list],
        "circule_color": list_color,
        "circule_messages": Messages,
        "marker_poses": [35.7600, 51.5200],

    }
    return render(request, 'map/ARFCN_Code.html', context=context)


def LAC(request):
    points = Point_Popup("LAC")
    context = {
        'info': Color_Info.objects.filter(parameter="Map-Serving Cell-LAC---.csv").distinct(),
        'len': len(list(Color_Info.objects.all())),
        'object': Region.objects.all(),

    }
    context.update(points)
    return render(request, 'map/ARFCN_Code.html', context=context)


def test_line_chart(request):
    context = {
        "Exelent": []

    }
    return render(request, 'test_line_chart.html')


def TechPieChart(request):
    counts = InsertColorInfoTechnology()
    context = {
        'len': len(list(Color_Info.objects.all())),
        '2G': counts[0],
        '3G': counts[1],
        '4G': counts[2],
        '5G': counts[3]

    }
    return render(request, 'map/tech_pie_chart.html', context)
