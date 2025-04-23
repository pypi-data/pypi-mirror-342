#!/usr/bin/env python3

import sys

from sescam import SescamAPI
from sescam.model import AppointmentType, Slot, SlotRequest


def get_sooner_slot_for_type(appointment_type: AppointmentType) -> Slot:
    result = api.get_available_slots_for_medical_appointments(appointment_type)
    if result is None:
        return

    sooner_slot = None

    for slot in result:
        if sooner_slot is None:
            sooner_slot = slot
            continue
    
        if sooner_slot.timeslot < slot.timeslot:
            continue
    
        sooner_slot = slot
    
    return sooner_slot


#cip = "SGLC831212911017"
cip = "NTSN830962911014"
mobile = "645224162"

api = SescamAPI(cip)
api.authenticate()

slot1 = get_sooner_slot_for_type(AppointmentType.MEDICAL)
slot2 = get_sooner_slot_for_type(AppointmentType.TELEPHONE_MEDICAL)

if slot1 and slot2:
    slot = slot1 if slot1.timeslot <= slot2.timeslot else slot2

else:
    slot = slot1 if slot1 else slot2

print(f"Sooner slot available: {slot}")
appointments = sorted(api.get_appointments(), key=lambda x: x.timeslot)
# appointments = api.get_appointments()

if appointments:
    print(f"Sooner appointment: {appointments[0]}")

appointment_request = SlotRequest.from_dict(slot.to_dict())
appointment_request.note = f"Teléfono: {mobile}"
appointment_request.origin_name = "MSDWEB"

if appointments:
    if slot.timeslot >= appointments[0].timeslot:
        print("You're having your best choice")
        sys.exit(0)
    
    else:
        api.cancel_appointment(appointments[0])

api.book_appointment(appointment_request)

# print(api.cancel_appointment(appointments[0]))
