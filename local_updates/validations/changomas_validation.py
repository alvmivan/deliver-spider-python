from local_updates.local_update import LocalValidation


class ChangomasValidationForUrls(LocalValidation):

    @property
    def providers(self):
        return ['changomas']

    @property
    def column_name(self):
        return 'url'

    def validation(self, item):
        prefix = 'https://www.changomas.com.ar'
        if not item.startswith(prefix):
            return f'URL does not start with {prefix}'
        return True


# another validation for: changomas, carrefour,coope,garbarino,fravega,gili,hipertehuelche
# make a get with the url and expect a 200 response

class Get200LocalValidationBase(LocalValidation):

    @property
    def providers(self):
        return ['changomas', 'carrefour', 'coope', 'garbarino', 'fravega', 'gili', 'hipertehuelche']

    def validation(self, item):
        import requests
        response = requests.get(item)
        if response.status_code != 200:
            return f'Got status code {response.status_code} for url {item}'
        return True


class PhotoLocalValidation(Get200LocalValidationBase):

    @property
    def column_name(self):
        return 'photo'


class URLLocalValidation(Get200LocalValidationBase):

    @property
    def column_name(self):
        return 'url'
