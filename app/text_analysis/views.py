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
    try:
        lst_names = extract_names(text)
        if not len(lst_names):
            content = {'msg': 'no person found in text'}
            return Response(content, status=status.HTTP_200_OK)
        names_frequency = extract_names_frequency(lst_names)
        lst_names = remove_duplicates(lst_names)
        res = get_person_infos_from_wikidata(lst_names, names_frequency)
        return Response(res)
    except Exception as e:
        content = {'error': str(e)}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def person_listing(request):
    """
    Listing all person or create a new person
    """
    if request.method == 'GET':
        lst_person = Person.objects.all()
        serializer = PersonSerializer(lst_person, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def freq_listing(request):
    """
    Listing all person frequency or update frequency for a person
    """
    if request.method == 'GET':
        lst_frequency = Frequency.objects.all()
        serializer = FrequencySerializer(lst_frequency, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        person_id = request.data.get('person')
        try:
            instance = Frequency.objects.get(person=person_id)
        except Frequency.DoesNotExist:
            instance=None
        serializer = FrequencySerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['GET'])
def stat_popular_names(request):
    """
        list the popular names analyzed in the texts
    """
    if request.method == 'GET':
        final_stat = []
        lst_frequency = Frequency.objects.all().order_by('-freq')
        serializer = FrequencySerializer(lst_frequency, many=True)
        for element in serializer.data:
            person_id = element["person"]
            freq = element["freq"]
            instance = Person.objects.get(id=person_id)
            popular_name = instance.name
            final_stat.append({"name" : popular_name,
                                "appearance frequency" : freq})
        return Response(final_stat)
