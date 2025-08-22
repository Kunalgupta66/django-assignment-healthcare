from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Welcome to the Healthcare API 🚀",
        "endpoints": {
            "register": "/api/auth/register/",
            "login": "/api/auth/login/",
            "patients": "/api/patients/",
            "doctors": "/api/doctors/",
            "mappings": "/api/mappings/"
        }
    })

urlpatterns = [
    path("", home),   # root path now works
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
