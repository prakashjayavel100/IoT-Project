from app.config import settings

print('MONGODB_URI_repr:', repr(settings.MONGODB_URI.get_secret_value()))
print('DATABASE_NAME:', settings.DATABASE_NAME)
