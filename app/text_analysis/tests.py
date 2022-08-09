from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Person, Frequency

from .serializers import PersonSerializer, FrequencySerializer


PERSON_LISTING_URL = "http://127.0.0.1:8000/api/all_person_listing"
FREQUENCY_LISTING_URL = "http://127.0.0.1:8000/api/all_frequency_listing"
PERSON_INFOS_URL = "http://127.0.0.1:8000/api/person_infos/"

class PublicPersonListingApiTests(TestCase):
    """Test the publicly available Person listing API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_persons(self):
        """Test retrieving persons"""
        Person.objects.create(name='Charles',
                             occupation='actor',
                             gender='male',
                             birthday='22/07/2001',
                             sex='male',
                             nationality='France',
                             image_link='/test/img.png'
                         )
        Person.objects.create(name='Antoine',
                             occupation='teacher',
                             gender='male',
                             birthday='27/07/2005',
                             sex='male',
                             nationality='France',
                             image_link='/test/img2.png'
                         )

        res = self.client.get(PERSON_LISTING_URL)
        persons = Person.objects.all().order_by('-name')
        serializer = PersonSerializer(persons, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_person_successful(self):
        """Test creating a new person"""
        payload = {'name': 'Test person', 'occupation': 'actor'}
        self.client.post(PERSON_LISTING_URL, payload)

        exists = Person.objects.filter(
            name=payload['name'], occupation=payload['occupation']
        ).exists()
        self.assertTrue(exists)

    def test_create_person_invalid(self):
        """Test creating a new person with invalid payload"""
        payload = {'name': ""}
        res = self.client.post(PERSON_LISTING_URL, payload)
        #persons = Person.objects.all()
        #serializer = PersonSerializer(persons, many=True)
        #print("------- serializer data : ", serializer.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class PublicFrequencyListingApiTests(TestCase):
    """Test the publicly available Frequency listing API"""

    def setUp(self):
        self.client = APIClient()

    def test_update_frequency_successful(self):
        """Test update frequecy for a valid person"""
        instance = Person.objects.create(name='test',
                                     occupation='teacher',
                                     gender='male',
                                     birthday='27/07/2005',
                                     sex='male',
                                     nationality='France',
                                     image_link='/test/img2.png'
                                 )
        payload = {'person': instance.id, 'freq': 20}
        self.client.post(FREQUENCY_LISTING_URL, payload)
        exists = Frequency.objects.filter(
            person=payload['person'], freq=payload['freq']
        ).exists()
        self.assertTrue(exists)

    def test_update_frequency_invalid_person(self):
        """Test update frequency for an invalid person"""
        payload = {'person': 20, 'freq': 3}
        res = self.client.post(FREQUENCY_LISTING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class PublicPersonInfoApiTests(TestCase):
    """Test the publicity available Person info API"""

    def setUp(self):
        self.client = APIClient()

    def test_text_without_names(self):
        """Test with a text that contains no persons name"""
        text = "Hello captain ! Have a nice day"
        url = PERSON_INFOS_URL + text
        res = self.client.post(url)
        data_expected = {'msg': 'no person found in text'}
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, data_expected)

    def test_empty_text(self):
        """Test with an empty text as input"""
        text = ""
        url = PERSON_INFOS_URL + text
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_length_results_valid_text(self):
        """Test the number of elements of the results"""
        text = "Gary Oldman is an actor and Joe Cocker is a musician"
        url = PERSON_INFOS_URL + text
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_text_with_names(self):
        """Test with a text that contains names"""
        text = "Hello Charles Aznavour and Bob Marley"
        name_1_expected = "Bob Marley"
        name_2_expected = "Charles Aznavour"
        url = PERSON_INFOS_URL + text
        res = self.client.post(url)
        newlist = sorted(res.data, key=lambda d: d['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(newlist[0]["name"], name_1_expected)
        self.assertEqual(newlist[1]["name"], name_2_expected)

    def test_name_frequency(self):
        """Test the name frequency in a text"""
        text = "Hello Anthony Hopkins and Anthony Hopkins"
        url = PERSON_INFOS_URL + text
        self.client.post(url)
        instance = Person.objects.get(name="Anthony Hopkins")
        instance_2 = Frequency.objects.get(person=instance.id)
        self.assertEqual(instance_2.freq, 2)
