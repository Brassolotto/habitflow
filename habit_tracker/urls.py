from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing'),  # Landing page como raiz
    path('users/', include('users.urls')),
    path('habits/', include('habits.urls')),
]
