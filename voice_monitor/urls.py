from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path("", views.VoiceMonitorAPI.as_view(), name="extract_pitch_mean"),
]