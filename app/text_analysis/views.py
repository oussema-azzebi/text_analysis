from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import extract_names, get_person_infos_from_wikidata


@api_view(['POST'])
def person_infos(request, text):
    """
    Get person's infos from a text.
    """

    print(type(text))
    lst_names = extract_names(text)
    print("---------------------extract lst_names: ", lst_names)
    get_person_infos_from_wikidata(lst_names)
    return Response({"data":"ok"})
    #serializer = SnippetSerializer(data=request.data)
    #if serializer.is_valid():
    #    serializer.save()
    #    return Response(serializer.data, status=status.HTTP_201_CREATED)
    #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
