from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ajabcapital',
        'USER': 'ajabcapital',
        'PASSWORD': 'o94u3n3jJJKS21032sjdu34nsnlp223'
    }
}

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, "..", "fixtures"),
)

try:
    from .local import *
except ImportError:
    pass