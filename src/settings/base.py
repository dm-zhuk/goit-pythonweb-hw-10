import configparser
import pathlib


path = pathlib.Path(__file__).parent.joinpath("config.ini")
parser = configparser.ConfigParser()
if not path.exists():
    raise FileNotFoundError(f"Configuration file not found at {path}")
parser.read(path)

try:
    DB_USER = parser.get("DATABASE", "USER")
    DB_PASSWORD = parser.get("DATABASE", "PASSWORD")
    DB_DOMAIN = parser.get("DATABASE", "DOMAIN")
    DB_NAME = parser.get("DATABASE", "DB_NAME", fallback="contacts_db")
    DB_PORT = parser.get("DATABASE", "PORT", fallback="5432")
except configparser.NoOptionError as e:
    raise ValueError(f"Missing option in config.ini: {e}")
