from django.urls import path, include

urlpatterns = [
   path('worktime/', include('worktime_api.urls')),
]