import base64
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class AppointmentType(Enum):
    UNKNOWN = ""
    MEDICAL = "DE"
    TELEPHONE_MEDICAL = "TD"
    NURSING = "DEENF"
    TELEPHONE_NURSING = "TDENF"
    FLU_VACUNATION = "VG"
    COVID_VACUNATION = "VC"

    @property
    def code(self) -> int:
        """Field for codModoVisita field."""
        match self.value:
            case "DE":
                return 2
            case "TD":
                return 3
            case "DEENF":
                return 4
            case "TDENF":
                return 5
            case "VG":
                return 6
            case "VC":
                return 7

    @property
    def modename(self) -> str:
        """Field for nomModoVisita."""
        match self.value:
            case "DE":
                return ""
            case "TD":
                return "Telefónica"
            case "DEENF":
                return ""
            case "TDENF":
                return ""
            case "VG":
                return ""
            case "VC":
                return ""


@dataclass
class Patient:
    """
    Represents a patient in the SESCAM healthcare system.
    """ 
    cip: str
    first_name: str
    last_name1: str
    last_name2: str
    birth_date: datetime
    phone: Optional[str] = None
    phone2: Optional[str] = None
    primary_doctor: Optional[str] = None
    assigned_nurse: Optional[str] = None
    health_center: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Patient":
        """Creates a Patient from the provided data dictionary."""
        return cls(
            cip=data.get("cip", ""),
            first_name=data.get("nombre"),
            last_name1=data.get("apellido1"),
            last_name2=data.get("apellido2"),
            birth_date=datetime.strptime(data.get("fechaNacimiento", "01/01/1970"), "%d/%m/%Y"),
            phone=data.get("telefono"),
            phone2=data.get("telefono2"),
            primary_doctor=data.get("medicoCabecera"),
            assigned_nurse=data.get("enfermeroAsignado"),
            health_center=data.get("centro"),
        )

    def full_name(self) -> str:
        """
        Returns the full name of the patient.
        """
        return f"{self.first_name} {self.last_name1} {self.last_name2}"


@dataclass
class Slot:
    """Represents a time slot for a medical appointment, such as a teleconsultation."""
    model_code: int
    person_code: str
    appointment_type: AppointmentType
    timeslot: datetime
    agenda_name: str
    description: str
    number: int  # The number of available slots at this time

    @classmethod
    def from_dict(cls, data: dict) -> 'Slot':
        """Creates a Slot object from the provided data dictionary."""
        date = data.get("fecha", "01/01/1970")
        time_minute = data.get("hora", "09:00")
        timeslot = datetime.strptime(f"{date} {time_minute}", "%d/%m/%Y %H:%M")
        appointment_type = AppointmentType(data.get("codTipoVisita", ""))
        return cls(
            model_code=data.get("codModelo", 0),
            person_code=data.get("codPerso", ""),
            appointment_type=appointment_type,            
            timeslot=timeslot,
            agenda_name=data.get("nomAgenda", ""),
            description=data.get("nomTVisita", ""),
            number=data.get("numero", 0),
        )
    
    def to_dict(self) -> dict[str, any]:
        return {
            "codModelo": self.model_code,
            "codPerso": self.person_code,
            "codModoVisita": self.appointment_type.code,
            "codTipoVisita": self.appointment_type.value,
            "fecha": self.timeslot.strftime("%d/%m/%Y"),
            "hora": self.timeslot.strftime("%H:%M"),
            "nomAgenda": self.agenda_name,
            "nomModoVisita": self.appointment_type.modename,
            "nomTVisita": self.description,
            "numero": self.number,
        }

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the slot.
        """
        return f"{self.timeslot} - {self.appointment_type.modename} in {self.agenda_name} agenda"


@dataclass
class SlotRequest(Slot):
    """Represents a time slot to ask for a medical appointment, such as a teleconsultation."""
    origin_name: str
    note: str

    @classmethod
    def from_dict(cls, data: dict) -> "SlotRequest":
        """Creates a SlotRequest object from the provided data dictionary."""
        date = data.get("fecha", "01/01/1970")
        time_minute = data.get("hora", "09:00")
        timeslot = datetime.strptime(f"{date} {time_minute}", "%d/%m/%Y %H:%M")
        appointment_type = AppointmentType(data.get("codTipoVisita", ""))
        return cls(
            model_code=data.get("codModelo", 0),
            person_code=data.get("codPerso", ""),
            appointment_type=appointment_type,            
            timeslot=timeslot,
            agenda_name=data.get("nomAgenda", ""),
            description=data.get("nomTVisita", ""),
            number=data.get("numero", 0),
            origin_name=data.get("codPersoReg", ""),
            note=data.get("nota", "")
        )

    def to_dict(self) -> dict[str, any]:
        """Return a equivalent dictionary for the object."""
        data = super().to_dict()
        data.update({
            "codPersoReg": self.origin_name,
            "nota": self.note,
        })
        return data


@dataclass
class Appointment(Slot):
    """Represent an appointment slot."""

    annulable: bool
    cip: str
    health_center_code: str
    is_videocall: bool
    doctor_name: str
    request_id: int
    videocall_ended: bool

    @classmethod
    def from_dict(cls, data: dict) -> "Appointment":
        """Creates an Appointment object from the provided data dictionary."""
        date = data.get("fecha", "01/01/1970")
        time_minute = data.get("hora", "09:00")
        timeslot = datetime.strptime(f"{date} {time_minute}", "%d/%m/%Y %H:%M")
        appointment_type = AppointmentType(data.get("codTipoVisita", ""))
        return cls(
            model_code=data.get("codModelo", 0),
            person_code=data.get("codPerso", ""),
            appointment_type=appointment_type,            
            timeslot=timeslot,
            agenda_name=data.get("nomAgenda", ""),
            description=data.get("nomTVisita", ""),
            number=data.get("numero", 0),
            annulable=data.get("anulable", False),
            cip=data.get("cip", ""),
            health_center_code=data.get("codCentro", ""),
            is_videocall=data.get("esVideoconsulta", False),
            doctor_name=data.get("nomProfesionalRealizador", ""),
            request_id=data.get("numSolic"),
            videocall_ended=data.get("videoconsultaFinalizada", False),
        )
    
    def to_dict(self) -> dict[str, any]:
        """Generate the equivalent dictionary to this object."""
        data = super().to_dict()
        data.update({
            "anulable": self.annulable,
	        "cip": self.cip,
	        "codCentro": self.health_center_code,
	        "esVideoconsulta": self.is_videocall,
            "nomProfesionalRealizador": self.doctor_name,
	        "numSolic": self.request_id,
	        "videoconsultaFinalizada": self.videocall_ended,
        })

        return data
 
    @property
    def cancel_code(self) -> str:
        """"""
        raw = "|".join([
            str(self.model_code),
            self.person_code,
            self.appointment_type.value,
            self.timeslot.strftime("%d/%m/%Y"),
            self.timeslot.strftime("%H:%M"),
            str(self.number),
            str(self.request_id)
        ])
        return base64.b64encode(raw.encode()).decode()
