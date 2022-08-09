from rest_framework import serializers

from .models import Person, Frequency


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'occupation', 'gender', 'birthday', 'sex',
                'nationality', 'image_link')

class FrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequency
        fields = ('id', 'person', 'freq')
