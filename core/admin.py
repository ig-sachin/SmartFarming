from django.contrib import admin
from .models import Blog,CropInfo,PreviousCropPred,FertilizerInfo,PreviousFertilizerPred,CropState

# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('bid','name','date')

@admin.register(CropInfo)
class CropInfoAdmin(admin.ModelAdmin):
    list_display=('id','name')

@admin.register(FertilizerInfo)
class FertilizerInfoAdmin(admin.ModelAdmin):
    list_display=('id','name')

@admin.register(PreviousCropPred)
class PreviousCropPredAdmin(admin.ModelAdmin):
    list_display=('id','nitrogen','phosphorous','potassium','crop')

@admin.register(PreviousFertilizerPred)
class PreviousFertilizerPredAdmin(admin.ModelAdmin):
    list_display=('id','nitrogen','phosphorous','potassium','fertilizer')

@admin.register(CropState)
class CropStateAdmin(admin.ModelAdmin):
    list_display=('id','stateName','districtName','cropYear')