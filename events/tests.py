from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import now
from datetime import timedelta
from .models import Event, Registration


# ========================
# Pengujian CRUD
# ========================

class EventModelTestCase(TestCase):
	def setUp(self):
		# Membuat Event untuk pengujian
		self.event = Event.objects.create(
			title="Test Event",
			description="Event for testing CRUD",
			date=now() + timedelta(days=5),
			location="Virtual",
			capacity=10,
		)

	def test_create_event(self):
		# Menguji bahwa event dibuat dengan benar
		self.assertEqual(self.event.title, "Test Event")

	def test_read_event(self):
		# Menguji bahwa event dapat diambil dari database
		event = Event.objects.get(id=self.event.id)
		self.assertEqual(event.title, "Test Event")

	def test_update_event(self):
		# Menguji bahwa event dapat diperbarui
		self.event.title = "Updated Event"
		self.event.save()
		self.assertEqual(Event.objects.get(id=self.event.id).title, "Updated Event")

	def test_delete_event(self):
		# Menguji bahwa event dapat dihapus
		event_id = self.event.id
		self.event.delete()
		self.assertFalse(Event.objects.filter(id=event_id).exists())


class RegistrationModelTestCase(TestCase):
	def setUp(self):
		# Membuat Event dan Registration untuk pengujian
		self.event = Event.objects.create(
			title="Test Event",
			description="Event for testing registration",
			date=now() + timedelta(days=5),
			location="Virtual",
			capacity=10,
		)
		self.registration = Registration.objects.create(
			event=self.event,
			participant_name="Test User",
			participant_email="test@example.com",
		)

	def test_create_registration(self):
		# Menguji bahwa registrasi dibuat dengan benar
		self.assertEqual(self.registration.participant_email, "test@example.com")

	def test_read_registration(self):
		# Menguji bahwa registrasi dapat diambil dari database
		registration = Registration.objects.get(id=self.registration.id)
		self.assertEqual(registration.participant_name, "Test User")

	def test_update_registration(self):
		# Menguji bahwa registrasi dapat diperbarui
		self.registration.participant_name = "Updated User"
		self.registration.save()
		self.assertEqual(
			Registration.objects.get(id=self.registration.id).participant_name,
			"Updated User",
		)

	def test_delete_registration(self):
		# Menguji bahwa registrasi dapat dihapus
		registration_id = self.registration.id
		self.registration.delete()
		self.assertFalse(Registration.objects.filter(id=registration_id).exists())


# ========================
# Pengujian Validasi Kapasitas
# ========================

class RegistrationValidationTestCase(APITestCase):
	def setUp(self):
		# Membuat Event dengan kapasitas terbatas
		self.event = Event.objects.create(
			title="Test Event",
			description="Event for testing capacity validation",
			date=now() + timedelta(days=5),
			location="Virtual",
			capacity=2,  # Kapasitas hanya 2 peserta
		)

	def test_registration_under_capacity(self):
		# Mendaftar hingga kapasitas masih tersedia
		payload1 = {
			"event": self.event.id,
			"participant_name": "User 1",
			"participant_email": "user1@example.com",
		}
		payload2 = {
			"event": self.event.id,
			"participant_name": "User 2",
			"participant_email": "user2@example.com",
		}

		# POST ke API register
		response1 = self.client.post("/events/register/", payload1)
		response2 = self.client.post("/events/register/", payload2)

		self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

	def test_registration_over_capacity(self):
		# Membuat pendaftar melewati batas kapasitas
		payload1 = {
			"event": self.event.id,
			"participant_name": "User 1",
			"participant_email": "user1@example.com",
		}
		payload2 = {
			"event": self.event.id,
			"participant_name": "User 2",
			"participant_email": "user2@example.com",
		}
		payload3 = {
			"event": self.event.id,
			"participant_name": "User 3",
			"participant_email": "user3@example.com",
		}

		# POST ke API register
		self.client.post("/events/register/", payload1)
		self.client.post("/events/register/", payload2)
		response3 = self.client.post("/events/register/", payload3)

		self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)  # Kegagalan
		self.assertIn(
			"Event is fully booked.",
			response3.data["non_field_errors"],
		)
