from logging import getLogger
logger = getLogger().getChild('paypal_IPN.listener')

from collections import OrderedDict
import requests

try:
    text_type = unicode
except NameError:
    text_type = str


class PayPalAPIError(RuntimeError):
    pass

class VerificationError(PayPalAPIError):
    pass


class PayPalIPNListener(object):
    PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'
    SANDBOX_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'

    def __init__(self, sandbox=False):
        super(PayPalIPNListener, self).__init__()
        self.sandbox = sandbox
        if sandbox:
            self.url = self.SANDBOX_URL
        else:
            self.url = self.PAYPAL_URL

    def process_request(self, url):
        self.verify_request(url)
        return self.decode_request(url)

    def verify_request(self, url):
        data = OrderedDict()
        data['cmd'] = '_notify-validate'
        for k, v in url.items():
            if isinstance(v, text_type):
                v = v.encode('UTF-8')
            data[k] = v
        confirmation_request = requests.post(self.url, data)
        data = confirmation_request.content
        if data != b"VERIFIED":
            raise VerificationError("Unable to verify PayPal IPN message. PayPal returned %r from verification URL %r" % (data, self.url))
        return True

    def decode_request(self, data):
        new = OrderedDict(data)
        for key, value in data.items():
            if isinstance( value, list ) and len( value ) == 1:
                new[key] = value[0]
        return new
