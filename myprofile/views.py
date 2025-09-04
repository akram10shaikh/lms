# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import (
    ContactInfo, WorkExperience, Education,
     Badge, WorkPreference,
    AdditionalInfo, AdditionalLink
)
from .serializers import (
    UserProfileSerializer, ContactInfoSerializer,
    WorkExperienceSerializer, EducationSerializer,
    BadgeSerializer, WorkPreferenceSerializer,
    AdditionalInfoSerializer, AdditionalLinkSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdmin, IsStaffOrAdmin

User = settings.AUTH_USER_MODEL
class MyProfileView(APIView):
    #Get or update logged-in user's profile.
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ContactInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None):
        if request.user.role == "student":
            contact_info, _ = ContactInfo.objects.get_or_create(user=request.user)
        else:
            target_user = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id or request.user.id)
            contact_info, _ = ContactInfo.objects.get_or_create(user=target_user)

        serializer = ContactInfoSerializer(contact_info)
        return Response(serializer.data)

    def patch(self, request, user_id=None):
        if request.user.role == "student":
            # students can only update their own
            contact_info, _ = ContactInfo.objects.get_or_create(user=request.user)
        elif request.user.role == "admin":
            # admins can update anyone’s
            target_user = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id or request.user.id)
            contact_info, _ = ContactInfo.objects.get_or_create(user=target_user)
        else:
            return Response({"detail": "Permission denied"}, status=403)

        serializer = ContactInfoSerializer(contact_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class WorkExperienceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ["staff", "admin"]:
            return WorkExperience.objects.all()
        return WorkExperience.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer
    queryset = WorkExperience.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ["staff", "admin"]:
            return Education.objects.all()
        return Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class BadgeListCreateView(generics.ListCreateAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role in ["staff", "admin"]:
            return Badge.objects.all()
        return Badge.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BadgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BadgeSerializer
    queryset = Badge.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class WorkPreferenceView(generics.GenericAPIView):
    serializer_class = WorkPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        work_pref, created = WorkPreference.objects.get_or_create(user=request.user)

        serializer = self.get_serializer(work_pref, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        try:
            work_pref = WorkPreference.objects.get(user=request.user)
        except WorkPreference.DoesNotExist:
            return Response({"detail": "No work preference found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(work_pref)
        return Response(serializer.data)

class AdditionalInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        info, _ = AdditionalInfo.objects.get_or_create(user=request.user)
        serializer = AdditionalInfoSerializer(info)
        return Response(serializer.data)

    def patch(self, request):
        info, _ = AdditionalInfo.objects.get_or_create(user=request.user)
        serializer = AdditionalInfoSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class AdditionalLinkListCreateView(generics.ListCreateAPIView):
    serializer_class = AdditionalLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        info, _ = AdditionalInfo.objects.get_or_create(user=self.request.user)
        return info.links.all()

    def perform_create(self, serializer):
        info, _ = AdditionalInfo.objects.get_or_create(user=self.request.user)
        serializer.save(additional_info=info)


class AdditionalLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdditionalLinkSerializer
    queryset = AdditionalLink.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
