from django.contrib import admin
from django.contrib.admin import ModelAdmin

from catalog.models import Breed, Kennel, BreedInKennel, Announcement

from catalog.models import AnnouncementPetPhoto, AnnouncementParentPhoto  # добавлены временно, для разработки


@admin.register(Breed)
class BreedAdmin(ModelAdmin):
    list_display = ('name',)
    fields = ('name',)


@admin.register(Kennel)
class KennelAdmin(ModelAdmin):
    list_display = ('id', 'title', 'owner_name', 'user', 'is_verified')
    fields = ('id', 'title', 'owner_name', 'user', 'phone', 'email', 'description', 'photo', 'documents', 'is_verified',
              'created_at',)
    readonly_fields = ('id', 'created_at',)


@admin.register(BreedInKennel)
class BreedInKennelAdmin(ModelAdmin):
    list_display = ('id', 'kennel', 'breed',)
    fields = ('id', 'kennel', 'breed',)
    readonly_fields = ('id',)


@admin.register(Announcement)
class AnnouncementAdmin(ModelAdmin):
    list_display = ('id', 'kennel', 'title')
    readonly_fields = ('id', 'updated_at')
# todo readonly вернуть 'created_at' после корректировки дат обьявлений на проде


# Админки только для разработки
@admin.register(AnnouncementPetPhoto)
class PetPhotoAdmin(ModelAdmin):
    list_display = ('id', 'announcement', 'image')
    fields = ('id', 'announcement', 'image')
    readonly_fields = ('id',)


@admin.register(AnnouncementParentPhoto)
class ParentPhotoAdmin(ModelAdmin):
    list_display = ('id', 'announcement', 'image')
    fields = ('id', 'announcement', 'image')
    readonly_fields = ('id',)
