# SESCAM API Client

This project is a Python 3 library that provides an interface to the **Mi Salud Digital** API from the **Servicio de Salud de Castilla-La Mancha (SESCAM)**.

## Features

With this library, you can:

- **Authenticate** using a patient's CIP (Personal Health ID).
- **Retrieve personal patient data**, including name, date of birth, and assigned health center.
- **List available appointment types** (e.g., medical consultations, vaccinations, etc.).
- **Check available appointment slots** for a specific type of service.
- **Book an appointment**, whether in-person or by phone, for both doctors and nurses, or for flu and COVID vacunations.
- **View upcoming scheduled appointments**.
- **Cancel existing appointments**.

## Intended Use

This client is designed to facilitate appointment management with the Castilla-La Mancha public healthcare system. It can be used for personal projects, custom integrations, or administrative tools.

## Requirements

- Python 3.8 or later
- Dependencies listed in `pyproject.toml` (mainly `requests`)

## Disclaimer

This project is provided for educational purposes only. Any use of this API should comply with the official terms and policies of the SESCAM healthcare system.

Part of the code was generated using AI tools, as an
experiment to check how helpful it can be in developing
a new project from scratch.
