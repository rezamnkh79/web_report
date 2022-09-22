from django.shortcuts import render

from map.models import Ranges, Point_Info,Result_Table


color_list = []


def Scan_result_cell(request):
   
    
    context = {
        'info' :Result_Table.objects.filter(parameter = "first").distinct(),
        
        
    }
    return render(request, 'scan_result.html',context=context)

def Scan_result_neighbor(request):
   
    
    context = {
        'info' :Result_Table.objects.filter(parameter = "second").distinct(),
        
        
    }
    return render(request, 'scan_result.html',context=context)

def PowerPieChart(request):

    context =computepiechert("RSRP")
    context.update({
        "ranges":Ranges.objects.filter(parameter="Map-Scan-Neighbor-SigPow-4G-Avg.csv")
    })
    return render(request,'scan_chart/pie_chart.html',context)

def QualityPieChart(request):

    context =computepiechert("RSRQ")
    context.update({
        "ranges":Ranges.objects.filter(parameter="Map-Scan-Neighbor-SigQual-4G-Avg.csv")
    })
    return render(request,'pie_chart.html',context)
    

def computepiechert(parameter):
    total_points = Point_Info.objects.filter(parameter=parameter)
    Very_Good =len( Point_Info.objects.filter(parameter=parameter,color="#00a032 ").values_list('color'))/len(total_points)
    Good = len(Point_Info.objects.filter(parameter=parameter,color="#00d228").values_list('color'))/len(total_points)
    Fair = len(Point_Info.objects.filter(parameter=parameter,color="#ffff00").values_list('color'))/len(total_points)
    Poor = len(Point_Info.objects.filter(parameter=parameter,color="#ffaa00").values_list('color'))/len(total_points)
    Bad = len(Point_Info.objects.filter(parameter=parameter,color="#ff0000").values_list('color'))/len(total_points)
    Very_Bad = len(Point_Info.objects.filter(parameter=parameter,color="#dc143c").values_list('color'))/len(total_points)
    Awful = len(Point_Info.objects.filter(parameter=parameter,color="#820000 ").values_list('color'))/len(total_points)
    No_Coverage = len(Point_Info.objects.filter(parameter=parameter,color="#aaaaaa ").values_list('color'))/len(total_points)
    print(Very_Good)
    result = {
        "Very_Good":round(Very_Good*100, 2),
        "Good":round(Good*100, 2),
        "Fair":round(Fair*100, 2),
        "Poor":round(Poor*100, 2),
        "Bad":round(Bad*100, 2),
        "Very_Bad":round(Very_Bad*100, 2),
        "Awful":round(Awful*100, 2),
        "No_Coverage":round(No_Coverage*100, 2),
        "Total":total_points,
    }
    return result  

def test_line_chart(request):
    context={
        "Exelent":[]
        
    }
    return render(request,'test_line_chart.html')
