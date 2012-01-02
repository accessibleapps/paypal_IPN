from collections import OrderedDict
import urllib

class PayPalAPIError(RuntimeError):
    pass

class VerificationError(PayPalAPIError):
    pass


class PayPalIPNListener(object):
    PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'
    SANDBOX_URL = 'https://sandbox.paypal.com/cgi-bin/webscr'

    def __init__(self, sandbox=False):
        super(PayPalIPNListener, self).__init__()
        if sandbox:
            self.PAYPAL_URL = self.SANDBOX_URL

    def process_request(self, url):
        self.verify_request(url)
        return self.decode_request(url)

    def verify_request(self, url):
        url = urllib.urlencode(url)
        new_url = "cmd=_notify-validate&%s" % url
        full_url = '%s?%s' % (self.PAYPAL_URL, new_url)
        confirmation_request = urllib.urlopen(full_url)
        data = confirmation_request.read()
        if data != "VERIFIED":
            raise VerificationError("Unable to verify PayPal IPN message. PayPal returned %r" % data)
        return True


    def decode_request(self, data):
        new = OrderedDict(data)
        for key, value in data.iteritems():
            if isinstance( value, list ) and len( value ) == 1:
                new[key] = value[0]
        return new
