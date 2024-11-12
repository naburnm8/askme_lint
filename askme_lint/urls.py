from django.contrib import admin
from django.urls import path, include
import app

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
]
