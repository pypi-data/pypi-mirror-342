"""Module for API access utilities."""

import requests

from sescam.model import Appointment, AppointmentType, Patient, Slot


class SescamAPI:
    """Class representing a session with the Sescam API."""
    BASE_URL = "https://sescam.jccm.es/misaluddigital/citacion-primaria/api/v1/mi-salud-digital/"
    
    def __init__(self, cip: str):
        self.cip = cip
        self.token = None
        self.headers = {}
        
    def authenticate(self) -> bool:
        """
        Authenticates the user and sets the Authorization token.
        """
        url = self.BASE_URL + "identificarme"
        payload = {"cip": self.cip}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
            return True
        else:
            print(f"Authentication failed with status code {response.status_code}.")
            return False

    def get_patient_data(self) -> Patient:
        """
        Retrieves patient data using the provided CIP.
        """
        if not self.token:
            raise Exception("Authentication required before calling this method.")

        url = self.BASE_URL + f"pacientes/{self.cip}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return Patient.response.json()
        
        raise Exception(f"Failed to get patient data: {response.status_code}")

    def get_available_slots_for_medical_appointments(self, appointment_type: AppointmentType) -> list[Slot]:
        """
        Retrieves available slots for medical appointments by type (e.g., "TD").
        """
        if not self.token:
            raise Exception("Authentication required before calling this method.")

        url = self.BASE_URL + f"pacientes/{self.cip}/tramites/{appointment_type.value}/huecos"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            for slot in data:
                slot.update({"nomModoVisita": appointment_type})
            if data:  # Check if there are any available slots
                return [Slot.from_dict(slot) for slot in data]
            else:
                print("No available slots for this type of appointment.")
                return None
        elif response.status_code == 204:
            print("There is no available slots for this type of appointment.")
        else:
            raise Exception(f"Failed to get available slots for this type of appointment: {response.status_code}")

    def get_appointments(self) -> list[Slot]:
        """
        Fetches all appointments for the patient.
        
        Returns:
            list[Slot]: A list of Slot objects representing the patient's appointments.
        """
        if not self.token:
            raise Exception("Authentication required before calling this method.")

        url = self.BASE_URL + f"pacientes/{self.cip}/citas"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            return [Appointment.from_dict(item) for item in data]
        elif response.status_code == 204:
            return []
        
        else:
            print(f"Failed to get appointments: {response.status_code} - {response.text}")
            return None

    def book_appointment(self, slot: Slot) -> bool:
        if not self.token:
            raise Exception("Authentication required before calling this method.")

        url = self.BASE_URL + f"pacientes/{self.cip}/citas"
        payload = slot.to_dict()
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 201:
            return True
        else:
            print(f"Booking failed: {response.status_code} - {response.text}")
            return False

    def cancel_appointment(self, appointment: Appointment) -> bool:
        if not self.token:
            raise Exception("Authentication required before calling this method.")
        
        url = self.BASE_URL + f"pacientes/{self.cip}/citas/{appointment.cancel_code}"
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 200:
            return True

        response.raise_for_status()
