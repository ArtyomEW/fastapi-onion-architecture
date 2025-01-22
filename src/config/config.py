from decouple import config


DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')


SECRET_KEY = config('JWT_SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

ALGORITHM = config('ALGORITHM')

DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT: str = "%Y-%m-%d"
