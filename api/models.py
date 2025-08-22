from django.db import models
from django.conf import settings

class Patient(models.Model):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female"), ("other", "Other")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patients"
    )
    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.age})"


class Doctor(models.Model):
    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="mappings")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="patients")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("patient", "doctor")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient.name} → {self.doctor.name}"
