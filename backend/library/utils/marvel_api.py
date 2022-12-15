import marvelous

from django.conf import settings
from django.core.cache import cache

class MarvelApiCache:
    def get(self, key):
        print('Cache for '+key)
        cached_value = cache.get('marvel_api:' + key)
        if cached_value:
            print('Cache HIT for '+key)
        return cached_value

    def store(self, key, value):
        cache.set('marvel_api:' + key, value, 3600)

def get_client():
    return marvelous.api(settings.MARVEL_API['PUBLIC_KEY'], settings.MARVEL_API['PRIVATE_KEY'], cache=MarvelApiCache())

