from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from catalog.models import (
    Announcement,
    Kennel,
    Breed,
    AnnouncementPetPhoto,
    AnnouncementParentPhoto,
)

from catalog.serializers.kennels import KennelViewSerializer


class PetPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = Base64ImageField()
    announcement = serializers.PrimaryKeyRelatedField(
        queryset=Announcement.objects.all()
    )

    class Meta:
        model = AnnouncementPetPhoto
        fields = ("id", "announcement", "image")


class ParentPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = Base64ImageField()
    announcement = serializers.PrimaryKeyRelatedField(
        queryset=Announcement.objects.all()
    )

    class Meta:
        model = AnnouncementParentPhoto
        fields = ("id", "announcement", "image")


class AnnouncementGetSerializer(serializers.ModelSerializer):

    kennel = KennelViewSerializer(many=False)
    breed = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all())

    pet_photos = PetPhotoSerializer(
        source="pet_photo", many=True, required=False
    )

    parent_photos = ParentPhotoSerializer(
        source="parent_photo", many=True, required=False
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "kennel",
            "breed",
            "male_count",
            "female_count",
            "birthday",
            "with_documents",
            "price",
            "city",
            "is_transportable",
            "description",
            "parents_description",
            "pet_photos",
            "parent_photos",
            "created_at",
            "updated_at",
        )


class AnnouncementPostSerializer(serializers.ModelSerializer):

    kennel = serializers.PrimaryKeyRelatedField(queryset=Kennel.objects.all())
    breed = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all())

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "kennel",
            "breed",
            "male_count",
            "female_count",
            "birthday",
            "with_documents",
            "price",
            "city",
            "is_transportable",
            "description",
            "parents_description",
        )


class AnnouncementPostPutSerializer(serializers.ModelSerializer):

    kennel = KennelViewSerializer(many=True)
    breed = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all())

    pet_photos = PetPhotoSerializer(
        source="pet_photo", many=True, required=False
    )

    parent_photos = ParentPhotoSerializer(
        source="parent_photo", many=True, required=False
    )

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "kennel",
            "breed",
            "male_count",
            "female_count",
            "birthday",
            "with_documents",
            "price",
            "city",
            "is_transportable",
            "description",
            "parents_description",
            "pet_photos",
            "parent_photos",
            "created_at",
            "updated_at",
        )

