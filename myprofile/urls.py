from django.urls import path
from .views import (
    MyProfileView, ContactInfoView,
    WorkExperienceListCreateView, WorkExperienceDetailView,
    EducationListCreateView, EducationDetailView,
    BadgeListCreateView, BadgeDetailView,
    WorkPreferenceView,
    AdditionalInfoView, AdditionalLinkListCreateView, AdditionalLinkDetailView
)

urlpatterns = [
    path("profile/", MyProfileView.as_view(), name="my-profile"),

    path("contact/", ContactInfoView.as_view(), name="my-contact-info"),
    path("contact/<int:user_id>/", ContactInfoView.as_view(), name="user-contact-info"),

    path("work-experiences/", WorkExperienceListCreateView.as_view(), name="work-exp-list"),
    path("work-experiences/<int:pk>/", WorkExperienceDetailView.as_view(), name="work-exp-detail"),

    path("educations/", EducationListCreateView.as_view(), name="education-list"),
    path("educations/<int:pk>/", EducationDetailView.as_view(), name="education-detail"),

    path("badges/", BadgeListCreateView.as_view(), name="badge-list"),
    path("badges/<int:pk>/", BadgeDetailView.as_view(), name="badge-detail"),

    path("work-preference/", WorkPreferenceView.as_view(), name="work-preference"),

    path("additional-info/", AdditionalInfoView.as_view(), name="additional-info"),
    path("additional-links/", AdditionalLinkListCreateView.as_view(), name="additional-links"),
    path("additional-links/<int:pk>/", AdditionalLinkDetailView.as_view(), name="additional-link-detail"),
]
