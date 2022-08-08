from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import (extract_names,
                    get_person_infos_from_wikidata,
                    extract_names_frequency,
                    remove_duplicates
                   )

from .models import Person
from .serializers import PersonSerializer

from .models import Frequency
from .serializers import FrequencySerializer


@api_view(['POST'])
def person_infos(request, text):
    """
    Get person's infos from a text.
    """
    lst_names = extract_names(text)
    if not len(lst_names):
        return
    names_frequency = extract_names_frequency(lst_names)
    print("---------------------extract lst_names: ", lst_names)
    print("---------------------names frequency: ", names_frequency)
    lst_names = remove_duplicates(lst_names)
    print("-------- lst name not duplicate : ", lst_names)
    res = get_person_infos_from_wikidata(lst_names, names_frequency)
    return Response(res)


@api_view(['GET'])
def person_listing(request):
    """
    Listing all person.
    """
    if request.method == 'GET':
        lst_person = Person.objects.all()
        serializer = PersonSerializer(lst_person, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def freq_listing(request):
    """
    Listing all person frequency.
    """
    if request.method == 'GET':
        lst_frequency = Frequency.objects.all()
        serializer = FrequencySerializer(lst_frequency, many=True)
        return Response(serializer.data)
