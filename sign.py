#!/usr/bin/env python
import argparse
import hashlib
import json
import re
import requests
import shutil
import sys
import tempfile
import zipfile
from base64 import b64decode
from signing_clients.apps import JarExtractor


class SigningError(Exception):
    pass


def call_signing(file_path, guid, endpoint):
    """Get the jar signature and send it to the signing server to be signed."""

    # We only want the (unique) temporary file name.
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_filename = temp_file.name

    # Extract jar signature.
    jar = JarExtractor(path=file_path,
                       outpath=temp_filename,
                       omit_signature_sections=True,
                       extra_newlines=True)

    response = requests.post(endpoint,
                             data={'addon_id': guid},
                             files={'file': (u'mozilla.sf',
                                    unicode(jar.signatures))})

    if response.status_code != 200:
        msg = u'Posting to add-on signing failed: {0}'.format(response.reason)
        raise SigningError(msg)

    pkcs7 = b64decode(json.loads(response.content)['mozilla.rsa'])
    jar.make_signed(pkcs7, sigpath=u'mozilla')
    shutil.move(temp_filename, file_path)

    print "{0} signed!".format(file_path)


def get_id(guid):
    """Return the addon GUID if <= 64 chars, or its sha256 hash otherwise.
    We don't want GUIDs longer than 64 chars: bug 1203365.
    """
    if len(guid) <= 64:
        return guid
    return hashlib.sha256(guid).hexdigest()


def get_guid(file_path):
    """Get e-mail guid of add-on."""
    z = zipfile.ZipFile(file_path)
    zlist = z.namelist()
    if 'install.rdf' in zlist:
        try:
            with z.open('install.rdf') as install:
                match = re.search(r'[\w\.-]+@[\w\.-]+', install.read())
                return get_id(match.group(0))
        except:
            print "Unexpected error:", sys.exc_info()[0]
            exit(1)
    elif 'manifest.json' in zlist:
        try:
            with z.open('manifest.json') as manifest:
                m = json.loads(manifest.read())
                return get_id(m['applications']['gecko']['id'])
        except:
            print "Unexpected error:", sys.exc_info()[0]
            exit(1)
    # we didn't find the guid, bail
    else:
        print "Could not find guid, check add-on"
        exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to sign")
    parser.add_argument("-g", "--guid",
                        help="Override guid",
                        action="store")
    parser.add_argument("-s", "--signer",
                        help="Signing Server Endpoint i.e."
                        "https://localhost/1.0/sign_addon",
                        action="store", required=True)

    args = parser.parse_args()

    if args.guid:
        guid = args.guid
    else:
        guid = get_guid(args.filename)

    call_signing(args.filename, guid, args.signer)


if __name__ == '__main__':
    main()
