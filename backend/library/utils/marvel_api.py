import marvelous

from django.conf import settings
from django.core.cache import cache

class MarvelApiCache:
    def get(self, key):
        print('Cache for '+key)
        print(cache.get('marvel_api:' + key))
        return cache.get('marvel_api:' + key)

    def store(self, key, value):
        cache.set('marvel_api:' + key, value, 3600)

def get_client():
    return marvelous.api(settings.MARVEL_API['PUBLIC_KEY'], settings.MARVEL_API['PRIVATE_KEY'], cache=MarvelApiCache())

