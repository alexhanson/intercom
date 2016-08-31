import cherrypy
import pytz
from datetime import datetime, timedelta
from intercom import responses


def _get_now(app_config):
    return datetime.now(pytz.timezone(app_config['locale']['timezone']))


def _is_valid_grant_code(app_config, code):
    return code == app_config['grant']['code']


def _get_grant_timedelta(app_config):
    return timedelta(minutes=app_config['grant']['minutes'])


class IntercomRoot(object):
    def __init__(self):
        self._last_grant = None

    def _make_grant(self, app_config):
        self._last_grant = _get_now(app_config)
        return self._last_grant + _get_grant_timedelta(app_config)

    def _has_active_grant(self, app_config):
        if not self._last_grant:
            return False

        now = _get_now(app_config)
        return (now - self._last_grant) < _get_grant_timedelta(app_config)

    # `PhoneNumberToDial` and `ExpectedFrom` should be provided as querystring
    # parameters. `From` will be provided by Twilio.
    @cherrypy.expose
    def index(self, PhoneNumberToDial, ExpectedFrom, From, **junk):
        cherrypy.response.headers['Content-Type'] = 'text/xml'
        app_config = cherrypy.request.app.config

        if From == ExpectedFrom:
            if self._has_active_grant(app_config):
                return responses.grant(
                    grant_digits=app_config['twilio']['grant_digits'])
            else:
                return responses.accept(
                    timeout_seconds=app_config['twilio']['timeout_seconds'],
                    phone_number=PhoneNumberToDial)
        else:
            return responses.reject()

    @cherrypy.expose
    def grant(self, code=''):
        app_config = cherrypy.request.app.config

        if _is_valid_grant_code(app_config, code):
            end_datetime = self._make_grant(app_config)
            end_datetime_formatted = end_datetime.strftime('%Y-%m-%d %H:%M')
            return 'Grant extended until {}'.format(end_datetime_formatted)
        else:
            raise cherrypy.NotFound()
