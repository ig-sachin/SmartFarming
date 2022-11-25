from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('crop/', views.crop, name="crop"),
    path('crop-state-wise', views.cropStateWise, name="cropStateWise"),
    path('fertilizer/', views.fertilizer, name="fertilizer"),
    path('plant/', views.plant, name="plant"),
    path('blogs/', views.blogs, name="blog"),
    path('submit-blog', views.submitBlog, name="submitBlog"),
    path('blogs/<int:bid>/', views.view_blog, name="viewBlog"),
    # path('push-crop-data/', views.pushCropData, name="pushCropData"),
    path('crop-year-state-wise', views.showCropStateWise, name="pushCropData"),
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)