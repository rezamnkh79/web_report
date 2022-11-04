from django.shortcuts import render
import os
import re


# Create your views here.
def GeneralInfo(request):
    directory = os.path.join(os.getcwd(), "data/datas/table")
    f = open(os.path.join(directory, 'Test Info-nodesInfo_tableWidget----.csv'), 'r')
    Nodes = []

    for data in f:
        data = data.split('@')
        print(data)
        try:
            if data[0] == "N":
                continue

            n = data[0]
            name = data[1]
            imsi = (data[2])
            imei = (data[3])
            type = (data[4])
            t = (data[5])
            status = (data[6])
            data_info = (data[7])
            roaming = data[8]
            desc = data[9]
            Nodes.append(
                {
                    "n": n,
                    "name": name,
                    "imsi": imsi,
                    "imei": imei,
                    "type": type,
                    "t": t,
                    "status": status,
                    "data": data_info,
                    "roaming": roaming,
                    "desc": desc,

                }
            )
        except:
            continue

    f.close()
    context = {
        "nodes": Nodes
    }
    f = open(os.path.join(directory, 'Test Info-generalInfoTable_tableWidget----.csv'), 'r')
    general_info = []
    for data in f:
        data = data.split('@')
        # jump from first data
        if data[0] == "Param":
            continue
        Param = (data[0])
        Description = str(data[1])
        general_info.append(
            {
                "param": Param,
                "description": Description,
            }
        )
    context.update({
        "general_info": general_info,
    })
    f.close()

    f = open(os.path.join(directory, 'Test Info-procInfoTable_tableWidget----.csv'), 'r')
    general_analysis = []
    for data in f:
        data = data.split('@')
        # jump from first data
        if data[0] == "Param":
            continue
        Param = (data[0])
        Count = str(data[1])
        general_analysis.append(
            {
                "param": Param,
                "count": Count,
            }
        )
    context.update({
        "general_analysis": general_analysis,
    })
    f.close()

    return render(request, 'introduce_general.html', context=context)


def SpeedInfo(request):
    directory = os.path.join(os.getcwd(), "data/datas/table")
    f = open(os.path.join(directory, 'Test Info-speedStatistic_hidden_tableWidget----.csv'), 'r')
    static = []

    for data in f:
        data = data.split('@')
        try:
            if data[0] == "Sample Num":
                continue

            Sample_Num = data[0]
            Average = data[1]
            Std = (data[2])
            Variance = (data[3])
            Median = (data[4])
            Maximum = (data[5])
            Minimum = (data[6])

            static.append(
                {
                    "Sample_Num": Sample_Num,
                    "Average": Average,
                    "Std": Std,
                    "Variance": Variance,
                    "Median": Median,
                    "Median": Median,
                    "Maximum": Maximum,
                    "Minimum": Minimum,

                }
            )
        except:
            continue

    f.close()
    context = {
        "static": static
    }
    f = open(os.path.join(directory, 'Test Info-speedRange_tableWidget----.csv'), 'r')
    ranges = []
    for data in f:
        data = data.split('@')
        # jump from first data
        if data[0] == "Param":
            continue
        Color = (data[0])
        Name = (data[1])
        Range = data[2]
        ranges.append(
            {
                "Color": Color,
                "Name": Name,
                'Range': Range,
            }
        )
    context.update({
        "ranges": ranges,
    })
    f.close()

    f = open(os.path.join(directory, 'Test Info-speedLegend_tableWidget----.csv'), 'r')
    info = []
    for data in f:
        data = data.split('@')
        # jump from first data
        if data[0] == "Color":
            continue
        Color = (data[0])
        Name = (data[1])
        Count = data[2]
        Distance = data[3]
        Distribution = data[4]
        info.append(
            {
                "Color": Color,
                "Name": Name,
                "Count": Count,
                "Distance": Distance,
                "Distribution": Distribution,
            }
        )
    context.update({
        "info": info,
    })
    f.close()
    print(context)
    return render(request, 'speed.html', context=context)
