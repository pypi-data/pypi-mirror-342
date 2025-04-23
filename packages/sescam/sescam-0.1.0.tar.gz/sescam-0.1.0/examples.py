SLOTS_RESPONSE = """{
	"codModelo": 150000134,
	"codPerso": "09752785A",
	"codModoVisita": 3,
	"codTipoVisita": "TD",
	"fecha": "06/05/2025",
	"hora": "12:25",
	"nomAgenda": "FORTES ALVAREZ, JOSE LUIS",
	"nomModoVisita": "Telefónica",
	"nomTVisita": "TELECONSULTA DEMANDA",
	"numero": 1
}"""

SLOT_REQUEST = """{
    "codModelo": 150000134,
    "codPerso": "09752785A",
    "codModoVisita": 3,
    "codTipoVisita": "TD",
    "fecha": "06/05/2025",
    "hora": "12:25",
    "nomAgenda": "FORTES ALVAREZ, JOSE LUIS",
    "nomModoVisita": "Telefónica",
    "nomTVisita": "TELECONSULTA DEMANDA",
    "numero": 1,            

    "codPersoReg": "MSDWEB",
    "nota": "Teléfono: 645224162. "
}"""

APPOINTMENT_RESPONSE = """{
	"codModelo": 150000134,
    "codPerso": "09752785A",
	"codModoVisita": 3,
	"codTipoVisita": "TD",
	"fecha": "08/05/2025",
	"hora": "16:10",
	"nomAgenda": "FORTES ALVAREZ, JOSE LUIS",
	"nomModoVisita": "Telefónica",
	"nomTVisita": "TELECONSULTA DEMANDA",
	"numero": 1,

    "anulable": true,
	"cip": "NTSN830962911014",
	"codCentro": "11021510",
	"esVideoconsulta": false,
    "nomProfesionalRealizador": "JOSE LUIS FORTES ALVAREZ",
	"numSolic": 794860741,
	"videoconsultaFinalizada": false
}"""

OLD_APPOINTMENT_RESPONSE = """{
    "codModelo": 150000134,
    "codPerso": "09752785A",
    # Missing codModoVisita
    "codTipoVisita": "DE",
    "fecha": "08/04/2025",
    "hora": "08:00",
    "nomAgenda": "MODELO 2007",
    # Missing nomModoVisita
    "nomTVisita": "DEMANDA",
    "numero": 1,

    "anulable": false,
    "cip": "NTSN830962911014",
    "codCentro": "11021510",
    "esVideoconsulta": false,
    "nomProfesionalRealizador": "JOSE LUIS FORTES ALVAREZ",
    "numSolic": 793494915,
    "videoconsultaFinalizada": false

    "imprimirJustificante": true,
    "nhc": "6778961",
}"""