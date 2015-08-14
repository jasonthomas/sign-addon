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
swig (for M2Crypto)
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

### Swig + M2Crypto on OSX ###
I ran into issues getting M2Crypto to build on OSX. Use the following brew formula to get it working:
```
brew uninstall swig --force
brew install homebrew/versions/swig304
brew link homebrew/versions/swig304
```
