from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from catalog.models import Kennel


class KennelViewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    id = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Kennel
        fields = ('id', 'title', 'owner_name', 'phone', 'email', 'description', 'photo')


class KennelPhotoSerializer(serializers.ModelSerializer):
    """сериализатор фотографии (для загрузки)"""
    photo = Base64ImageField(required=True)

    class Meta:
        model = Kennel
        fields = ('photo',)



