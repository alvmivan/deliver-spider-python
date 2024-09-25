from unittest import TestCase

from local_updates.local_update import LocalValidation
from local_updates.validations.changomas_validation import ChangomasValidationForUrls, PhotoLocalValidation, \
    URLLocalValidation


# inherit to make unit test
class ValidateDataTest(TestCase):
    validations: list[LocalValidation] = [
        ChangomasValidationForUrls(),
        PhotoLocalValidation(),
        URLLocalValidation()
    ]

    def test_validate_data(self):
        # call perform_validation for each localValidation to get the list of errors
        for validation in self.validations:
            errors = validation.perform_validation()
            for error in errors:
                assert error == 'OK', f'Error found:\n {error}\n\n'

