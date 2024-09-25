import json

from flask import request

from api.endpoint import EndPoint

settings_path = "settings/settings.json"


class GetSettings(EndPoint):
    def path(self):
        return '/settings'

    def function(self):
        with open(settings_path) as f:
            settings = json.load(f)
        return settings

    def doc(self):
        return {
            'description': 'Get the settings of the API',
        }


class UpdateSettings(EndPoint):
    def method(self):
        return 'POST'

    def path(self):
        return '/update-settings'

    def function(self):
        request_json = request.json
        with open(settings_path, 'r+') as f:
            settings = json.load(f)
        with open(settings_path, 'w+') as f:
            for key in request_json.keys():
                if key in settings:
                    settings[key] = request_json[key]
            json.dump(settings, f,indent=4)

        return {}

    def doc(self):
        return {
            'description': 'Update the settings of the API',
            'parameters': {
                'settings': 'The new settings to be saved'
            }
        }
