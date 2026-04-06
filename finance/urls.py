from django.urls import path
from .views import RecordListCreateView, RecordDetailView, DashboardView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('records/', RecordListCreateView.as_view()),
    path('records/<int:pk>/', RecordDetailView.as_view()),
    path('dashboard/', DashboardView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]