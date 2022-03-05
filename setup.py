from setuptools import setup

setup(
 name = "paypal_IPN",
 version = "0.16",
 author = "Christopher Toth",
 author_email = "q@q-continuum.net",
 description = "Simple PayPal IPN Listener",
 packages = ['paypal_IPN'],
 install_requires = ['requests'],
)
