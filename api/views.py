from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Patient, Doctor, PatientDoctorMapping
from .permissions import IsOwner
from .serializers import (
    RegisterSerializer, PatientSerializer, DoctorSerializer, MappingSerializer
)


# --- Auth: Register ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# --- Auth: Email-based Login ---
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Accepts 'email' instead of 'username' for login.
    Internally maps to the user's username (we set username=email at registration).
    """
    def validate(self, attrs):
        # move email -> username so parent class works
        email = self.initial_data.get("email")
        if email and not self.initial_data.get("username"):
            # ensure a user exists; if not, let parent raise the standard error
            user = get_object_or_404(User, email=email)
            self.initial_data["username"] = user.username
        return super().validate(self.initial_data)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


# --- Patient CRUD ---
class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


# --- Doctor CRUD (read open, write auth) ---
class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# --- Mappings ---
class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only mappings for my patients
        return PatientDoctorMapping.objects.filter(patient__user=self.request.user)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class MappingDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__user=self.request.user)


# GET /api/mappings/<patient_id>/
class PatientMappingsView(generics.ListAPIView):
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        return PatientDoctorMapping.objects.filter(
            patient_id=patient_id,
            patient__user=self.request.user
        )

