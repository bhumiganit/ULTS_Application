import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.gdal import DataSource
from .models import Building_Details
import pandas as pd
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import HttpResponseRedirect
from sqlalchemy import create_engine
import os
# Create your views here.

from django.contrib.gis.geos import GEOSGeometry
import geopandas as gp

def homePage(request):
    buildingData = Building_Details.objects.filter().order_by('Serial_Number')
    return render(request, 'homepage.html',{'buildingData':buildingData})
    
def addRow(request):
    print("inside add row")
    if request.method == 'GET':
        Building_Details.objects.create(Name_of_Building="")
        returnData = {"rowAdd":'row added successfully!'}
        datacontext = json.dumps(returnData)
        return JsonResponse(datacontext,safe=False)

def getRowSerialNumber(request):
    data = Building_Details.objects.filter()
    Building_Serial_Number  = [i.Serial_Number for i in Building_Details.objects.filter()]
    print(Building_Serial_Number)
    returnData = {"rowNumber":Building_Serial_Number[-1]}
    datacontext = json.dumps(returnData)
    return JsonResponse(datacontext,safe=False)

def updateBuildingData(request):
    print("updating Building")
    try:
        buildingSerialNumber = request.GET.get('buildingSerialNumber')
        buildingName_ = request.GET.get('buildingName_')
        buildingAddress_ = request.GET.get('buildingAddress_')
        buildingNumber_ = request.GET.get('buildingNumber_')
        buildingLocation_ = request.GET.get('buildingLocation_')
        if buildingLocation_.count('SRID') == 0:
            lat = buildingLocation_.split(",")[0]
            long = buildingLocation_.split(",")[1]
            pnt = GEOSGeometry(f"POINT({long} {lat})")
        elif buildingLocation_.count('SRID') == 1:
            lat = buildingLocation_.split('(')[-1].split(')')[0].split(" ")[1]
            long = buildingLocation_.split('(')[-1].split(')')[0].split(" ")[0]
            pnt = GEOSGeometry(f"POINT({long} {lat})") 
              
        if Building_Details.objects.filter(Serial_Number=buildingSerialNumber).exists():
            Building_Details.objects.filter(Serial_Number=buildingSerialNumber).update(Name_of_Building=buildingName_,
                                                                                    Location=buildingAddress_,
                                                                                    Building_Number = buildingNumber_,
                                                                                    GeometricLocation = pnt)
            returnData = {"info":"Building data updated Successfully!"}
            datacontext = json.dumps(returnData)
            return JsonResponse(datacontext,safe=False)
        else:
            returnData = {"info":"Building data updated failed\nPlease check your Database!"}
            datacontext = json.dumps(returnData)
            return JsonResponse(datacontext,safe=False)
    except Exception as UpdateBuildingExp:
        print(UpdateBuildingExp)
        return HttpResponse(f"Error:{UpdateBuildingExp}\nPlease check your Input")
        
def deleteRow(request):
    print("deleting a row")
    buildingSerialNumber2 = request.GET.get('buildingSerialNumber')
    if Building_Details.objects.filter(Serial_Number=buildingSerialNumber2).exists():
        Building_Details.objects.filter(Serial_Number=buildingSerialNumber2).delete()
        returnData = {"info":"Row deleted!"}
        datacontext = json.dumps(returnData)
        return JsonResponse(datacontext,safe=False)
    else:
        returnData = {"info":"It seems row is missing in your Database!"}
        datacontext = json.dumps(returnData)
        return JsonResponse(datacontext,safe=False)

@csrf_exempt
def uploadshpfile(request):
    print("inside uploadshpfile")
    if request.method == 'POST':
        if request.FILES:
            try:
                myfile2 = request.FILES['file1']
                fs = FileSystemStorage()
                filename = fs.save(myfile2.name, myfile2)
                uploaded_file_url = fs.url(filename)
                print(uploaded_file_url)
                abs_filePath = os.path.abspath(__file__)
                os.chdir(os.path.dirname(abs_filePath))
                os.chdir('..')
                pathstr = os.path.basename(uploaded_file_url)
                pathstr_ = str(pathstr)
                sfl = gp.read_file(pathstr_,enabled_drivers=["ESRI Shapefile"])
                engine = create_engine("postgresql://postgres:resql@localhost:5432/ULTS_Test")  
                # print(sfl)
                pathstr_ = pathstr_.replace('zip','')
                pathstr_ = pathstr_.replace('.','')
                if pathstr_.count('_') > 1:
                    table_name = pathstr_.split('_')[0]
                table_name = pathstr_
                sfl.to_postgis(table_name,engine)
                
                # return HttpResponseRedirect('/') 
                return HttpResponse("File uploaded successfully!")
            except Exception as e:
                print(e)
                print("something went wrong ;\n Please check your input file\nor database credentials")
                return HttpResponse(f"Error:{e}\nsomething went wrong ;\n Please check your input file\nor database credentials")
            finally:
                if os.path.exists(pathstr_+".zip"):
                    os.remove(pathstr_+".zip")
                
        elif not request.FILES:
            return HttpResponse("Please select a file to proceed!")
        
    
    
    
    