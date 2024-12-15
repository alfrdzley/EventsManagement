from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from events import views
from events.views import RegistrationCreateView

urlpatterns = [
	path('events/', views.EventList.as_view()),
	path('events/<int:pk>/', views.EventDetail.as_view()),
	path('events/register/', RegistrationCreateView.as_view(), name='register'),
	path('events/statistics/', views.EventStatistics.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
