import json
import logging
import requests

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Magic_mirror(NeuronModule):

    def __init__(self, **kwargs):
        super(Magic_mirror, self).__init__(**kwargs)

        # input variables
        self.mm_url = kwargs.get('mm_url', None)
        self.notification = kwargs.get('notification', None)
        self.payload = kwargs.get('payload', None)

        # check parameters
        if self._is_parameters_ok():

            if isinstance(self.payload, dict):
                self.payload = json.dumps(self.payload)

            self.parameters = {
                "notification": self.notification,
                "payload": self.payload
            }

            logger.debug(self.neuron_name + " call Magic Mirror MMM-kalliope-API: %s" % self.mm_url)

            r = None
            try:
                r = requests.post(url=self.mm_url, data=self.parameters)
            except requests.ConnectionError:
                logger.debug(self.neuron_name + " Error, MM URL connection error: %s" % self.mm_url)

            if r is not None:
                self.status_code = r.status_code
                self.content = r.content
                # we try to load into a json object the content. So Kalliope can use it to talk
                try:
                    self.content = json.loads(self.content.decode())
                except ValueError:
                    logger.debug(self.neuron_name + "cannot get a valid json from returned content")
                    pass
                self.response_header = r.headers

                message = {
                    "status_code": self.status_code,
                    "content": self.content,
                    "response_header": self.response_header
                }

                self.say(message)

    def _is_parameters_ok(self):

        if self.mm_url is None:
            raise InvalidParameterException("Missing mm_url parameter")

        if self.notification is None:
            raise InvalidParameterException("Missing notification parameter")

        if self.payload is None:
            raise InvalidParameterException("Missing payload parameter")

        return True
