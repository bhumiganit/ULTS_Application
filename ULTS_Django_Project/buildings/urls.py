from django.urls import path
from . import views

urlpatterns = [
    path('',views.homePage),
    path('addRow',views.addRow),
    path('getRowSerialNumber',views.getRowSerialNumber),
    path('updateBuildingData',views.updateBuildingData),
    path('deleteRow',views.deleteRow),
    path('uploadshpfile',views.uploadshpfile),
]