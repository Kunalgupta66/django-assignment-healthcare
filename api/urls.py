from django.urls import path
from .views import (
    RegisterView, EmailTokenObtainPairView, PatientListCreateView, PatientDetailView,
    DoctorListCreateView, DoctorDetailView, MappingListCreateView, MappingDetailView, PatientMappingsView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", EmailTokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("patients/", PatientListCreateView.as_view(), name="patients"),
    path("patients/<int:pk>/", PatientDetailView.as_view(), name="patient_detail"),

    path("doctors/", DoctorListCreateView.as_view(), name="doctors"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(), name="doctor_detail"),

    path("mappings/", MappingListCreateView.as_view(), name="mappings"),
    path("mappings/<int:pk>/", MappingDetailView.as_view(), name="mapping_detail"),
    path("mappings/<int:patient_id>/", PatientMappingsView.as_view(), name="patient_mappings"),
]
