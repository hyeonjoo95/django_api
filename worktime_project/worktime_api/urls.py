from django.urls import path, include
from . import views

urlpatterns = [
    path('record/', views.WorkTimeRecordAPIView.as_view()),
    path('list/<int:user_id>/', views.WorkTimeListAPIView.as_view()),
    path('detail/<int:pk>/', views.WorkTimeDetailAPIView.as_view()),
]