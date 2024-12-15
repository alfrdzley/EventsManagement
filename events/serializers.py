from django.utils.timezone import now
from rest_framework import serializers
from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['id', 'title', 'description', 'date', 'location', 'capacity']

	# Validasi tambahan saat membuat atau mengupdate data
	def validate_date(self, value):
		if value < now():
			raise serializers.ValidationError("Event Tidak Boleh di Masa Lalu")
		return value


class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Registration
		fields = ['id', 'event', 'participant_name', 'participant_email']

	def validate(self, data):
		event = data['event']
		if event.registrations.count() >= event.capacity:
			raise serializers.ValidationError("Event is fully booked.")
		return data
