from rest_framework import generics
from rest_framework.generics import CreateAPIView

from .serializers import EventSerializer

from rest_framework.views import APIView
from django.db.models import Avg
from .models import Event

from rest_framework.response import Response
from rest_framework import status
from .models import Registration
from .serializers import RegistrationSerializer


class EventList(generics.ListCreateAPIView):
	"""
	Melihat daftar event yang ada dan membuat event baru
	"""
	queryset = Event.objects.all()
	serializer_class = EventSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Melihat, mengupdate, dan menghapus event yang ada
	"""
	queryset = Event.objects.all()
	serializer_class = EventSerializer


class RegistrationCreateView(CreateAPIView):
	"""
	Mendaftarkan peserta ke event
	"""
	queryset = Registration.objects.all()
	serializer_class = RegistrationSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return Response(
			{"message": "Registration successful!", "data": serializer.data},
			status=status.HTTP_201_CREATED
		)


class EventStatistics(APIView):
	"""
	Melihat statistik event
	"""
	def get(self, request):
		total_events = Event.objects.count()
		avg_capacity = Event.objects.aggregate(Avg('capacity'))['capacity__avg']
		total_participants = Registration.objects.count()
		return Response({
			"total_events": total_events,
			"avg_capacity": avg_capacity,
			"total_participants": total_participants
		})