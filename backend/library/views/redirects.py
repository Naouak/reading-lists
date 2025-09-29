import json
from urllib.request import urlopen

from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework.decorators import api_view, permission_classes

from library.models import Book


@api_view(['GET'])
@permission_classes([])
def read_online(request, book_id):
    if not book_id:
        return HttpResponseNotFound()

    book = Book.objects.filter(id=book_id).first()

    if not book:
        return HttpResponseNotFound()

    # noinspection PyBroadException
    try:
        url = book.read_online_url
        id = url[url.rfind("/")+1:]
        bifrost_url = f'https://bifrost.marvel.com/unison/legacy?digitalId={id}'
        serialized_data = urlopen(bifrost_url).read()
        data = json.loads(serialized_data)

        drn = data["data"]["dynamicQueryOrError"]["entity"]["contents"][0]["content"]["id"]

        final_url = f'https://marvel.smart.link/fiir7ec77?type=issue&drn={drn}&sourceId={book.external_id}'
        return HttpResponseRedirect(redirect_to=final_url)
    except:
        return HttpResponseRedirect(redirect_to=f'https://www.marvel.com/comics/issue/{book.external_id}/comics-collection')