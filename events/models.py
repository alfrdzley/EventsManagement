from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class Event(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)  # Opsional
	date = models.DateTimeField()
	location = models.CharField(max_length=150)
	capacity = models.PositiveIntegerField()  # Hanya menerima bilangan positif

	def clean(self):
		# Validasi: Tanggal tidak boleh di masa lalu
		if self.date < datetime.now():
			raise ValidationError("Event date cannot be in the past.")


class Registration(models.Model):
	event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
	participant_name = models.CharField(max_length=255)
	participant_email = models.EmailField()

	def __str__(self):
		return f"{self.participant_name} - {self.event.title}"  # Peserta tidak bisa daftar 2x untuk event yang sama
