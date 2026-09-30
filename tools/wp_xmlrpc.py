"""Minimal WordPress XML-RPC client (sends through curl so it honours the HTTPS proxy)."""
import os, subprocess, xmlrpc.client

URL = 'https://www.elharamainwisata.com/xmlrpc.php'


def call(method, *params):
    body = xmlrpc.client.dumps(params, method, allow_none=True).encode()
    out = subprocess.run(['curl', '-sS', '-X', 'POST', URL, '-H', 'Content-Type: text/xml', '--data-binary', '@-'],
                         input=body, capture_output=True, check=True).stdout
    return xmlrpc.client.loads(out)[0][0]


def auth():
    return (1, os.environ['WP_USER'], os.environ['WP_APP_PASSWORD'])
