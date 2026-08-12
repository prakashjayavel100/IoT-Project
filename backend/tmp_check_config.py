from app.config import settings
print('uri_blank', settings.MONGODB_URI.get_secret_value() == '')
print('uri_length', len(settings.MONGODB_URI.get_secret_value()))
