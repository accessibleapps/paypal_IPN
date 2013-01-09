from logging import getLogger
logger = getLogger().getChild('paypal_IPN.listener')

from collections import OrderedDict
import requests


class PayPalAPIError(RuntimeError):
    pass

class VerificationError(PayPalAPIError):
    pass


class PayPalIPNListener(object):
    PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'
    SANDBOX_URL = 'https://sandbox.paypal.com/cgi-bin/webscr'

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
        arg = ""
        data = collections.OrderedDict()
        data['cmd'] = '_notify-validate'
        for k, v in url.iteritems():
            if isinstance(v, unicode):
                v = v.encode('UTF-8')
            data[k] = v
        confirmation_request = requests.post(self.url, data)
        data = confirmation_request.content
        if data != "VERIFIED":
            raise VerificationError("Unable to verify PayPal IPN message. PayPal returned %r from verification URL %r" % (data, full_url))
        return True


    def decode_request(self, data):
        new = OrderedDict(data)
        for key, value in data.iteritems():
            if isinstance( value, list ) and len( value ) == 1:
                new[key] = value[0]
        return new
