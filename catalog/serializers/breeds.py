from rest_framework import serializers

from catalog.models import Breed, BreedInKennel


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ('name',)


class BreedInKennelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedInKennel
        fields = ('id', 'kennel', 'breed')
