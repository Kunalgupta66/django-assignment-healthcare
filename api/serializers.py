from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Patient, Doctor, PatientDoctorMapping


class RegisterSerializer(serializers.ModelSerializer):
    # assignment asks: name, email, password
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        name = validated_data.pop("name")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # use email as username for simplicity
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=name
        )
        user.set_password(password)
        user.save()
        return user


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "name", "age", "gender", "created_at", "user"]
        read_only_fields = ["id", "created_at", "user"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "created_at"]
        read_only_fields = ["id", "created_at"]


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        """Ensure the mapping patient belongs to the requesting user."""
        request = self.context["request"]
        patient = attrs.get("patient")
        if patient.user_id != request.user.id:
            raise serializers.ValidationError("You can only map doctors to your own patients.")
        return attrs


