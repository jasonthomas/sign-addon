Add-on Signer
===================

This script will:
* Submit a request to the specified signing service and return a signed file

## Requirements ##

The following system packages need to be install before you begin:
```
git
pip
python
virtualenv
```

## Installation ##
```
git clone https://github.com/jasonthomas/sign-addon.git
cd sign-addon
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Usage ##
```
source ./venv/bin/activate
./sign.py -s https://example.com/path /path/to/file
Enter username: foobar
Enter password:
/path/to/file signed!

```
