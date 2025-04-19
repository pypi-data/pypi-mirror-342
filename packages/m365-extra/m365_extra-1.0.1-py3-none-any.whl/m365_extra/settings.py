import os
from pathlib import Path
from zut import load_dotenv, get_secret

BASE_DIR = Path(__file__).resolve().parent.parent

_app_dir = Path(os.environ.get('APPDATA') or '~/local/share/m365-extra').expanduser().joinpath('m365-extra')

load_dotenv()
if (_value := BASE_DIR.joinpath('.env')).exists():
    load_dotenv(_value)
if (_value := _app_dir.joinpath('.env')).exists():
    load_dotenv(_value)

if _value := os.environ.get('M365_DATA_DIR'):
    DATA_DIR = Path(_value)
elif _value := os.environ.get('DATA_DIR'):
    DATA_DIR = Path(_value).joinpath('m365')
elif (_value := BASE_DIR.joinpath('data')).exists():
    DATA_DIR = _value
elif _app_dir.exists():
    DATA_DIR = _app_dir
else:
    DATA_DIR = Path.cwd().joinpath('data')

HTTPS_PROXY = os.environ.get('HTTPS_PROXY', '__wpad__')
if HTTPS_PROXY == '0':
    HTTPS_PROXY = None

TENANT_ID = os.environ.get('M365_TENANT_ID')
APP_ID = os.environ.get('M365_APP_ID')
CLIENT_SECRET_KEY = get_secret('M365_CLIENT_SECRET_KEY')
