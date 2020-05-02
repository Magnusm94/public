from datetime import datetime


# Only got to start working on this project yet. Going to implement with Django
class customer:

    def __init__(self):

        self.about = None
        self.contacts = []
        self.bills = {
            'Alle regninger': [],
            'Betalte regninger': [],
            'Ubetalte regninger': [],
            'Forfalte regninger': [],
            'Fakturamotaker': None,
            'Faktura addresse': None,
            'Faktura epost': None,
            'Totalt betalt': 0,
            'Totalt ubetalt': 0,
            'Forfallsdato': None
        }
        self.website = []
        self.app = []
        self.preferences = []
        self.history = []
        self.feedback = []
        self.practical_info = {
            'Fast kunde': False,
            'Prøveuke': False,
            'Kjørerute': None,
            'Pris': None,
            'Bytteperson': None,
            'Selger': None,
            'Registrert': datetime.now(),
            'Registrert av': None
        }

    def get_about(self):
        return self.about

    def set_about(self, firmanavn, addresse, organisasjonsnummer, telefon, epost):
        try:
            self.about = {
                'Firmanavn': firmanavn,
                'Addresse': addresse,
                'Organisasjonsnummer': organisasjonsnummer,
                'Telefon': telefon,
                'E-post': epost
            }
            return True

        except TypeError:
            return False

    def get_organisation_number(self):
        try:
            return self.about['Organisasjonsnummer']
        except:
            return None

    def get_contact_info(self):
        return self.contacts

    def get_main_contact(self):
        try:
            for contact in self.contacts:
                if contact['Hovedkontakt']:
                    return contact
        except:
            return None

    def get_contact_by_name(self, fornavn):
        try:
            for contact in self.contacts:
                if contact['Fornavn'] == fornavn:
                    return contact
        except:
            return None

    def edit_contact(self, **kwargs):
        for x, z in locals():
            if z is not None:
                for person in self.contacts:
                    if person[x] == z:
                        self.contacts[person] = locals()
                        return True

    def add_contact(self, *args, **kwargs):
        if 'hovedkontakt' in kwargs.keys() and kwargs['hovedkontakt'] is True:

            for contact in self.contacts['Hovedkontakt']:
                if contact['Hovedkontakt']:
                    contact['Hovedkontakt'] = False
                    break
        self.contacts.append(locals())
        return True

    # Needs sql part
    def website_new_user(self):
        self.website.append({
            'Brukernavn': None,
            'Passord': None,
            'Epost': None,
            'Bekreftet bruker': False,
            'Firma admin': None,
            'Profil': [],
            'Bestillinger': [],
            'Tilbakemeldinger': [],
            'Bilder': [],
            'Kommentarer': [],
            'Antall besøk': [],
            'Preferanser': [],
            'Fakturaoversikt': [],
            'Innstillinger': [],
            'Aktiv': True,
            'Registreringstid': datetime.now()
        })