from django.db import models
from django.utils.timezone import now

from accounts.models import User


class Breed(models.Model):
    """порода"""

    name = models.CharField(
        primary_key=True,
        db_index=True,
        max_length=200,
        verbose_name="название породы",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "порода"
        verbose_name_plural = "породы"
        ordering = ("name",)
        db_table = "breed"


class Kennel(models.Model):
    """заводчик"""

    id = models.AutoField
    title = models.CharField(
        db_index=True,
        max_length=200,
        verbose_name="название питомника",
        unique=True,
    )
    owner_name = models.CharField(
        max_length=200, verbose_name="имя заводчика", null=True, blank=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="владелец (пользователь)"
    )
    phone = models.CharField(
        max_length=15,
        verbose_name=" контактный телефон",
        null=False,
        blank=False,
    )
    email = models.EmailField(
        verbose_name="контактный е-майл", null=True, blank=True
    )
    description = models.TextField(
        verbose_name="описание", null=True, blank=True, max_length=1000
    )

    photo = models.ImageField(
        verbose_name="фото заводчика", upload_to="kennels/photo", blank=True
    )
    documents = models.FileField(
        verbose_name="документ / архив документов",
        upload_to="kennels/documents",
        blank=True,
    )
    is_verified = models.BooleanField(
        verbose_name="документы подтверждены", default=False
    )

    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "заводчик"
        verbose_name_plural = "заводчики"
        ordering = ("title",)
        db_table = "kennel"


class BreedInKennel(models.Model):
    """порода, которой занимается питомник"""

    id = models.AutoField
    kennel = models.ForeignKey(
        Kennel, on_delete=models.CASCADE, verbose_name="питомник", related_name='kennel_info'
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name="breed_name",
        verbose_name="порода",
    )

    def __str__(self):
        return f"{self.kennel} : {self.breed}"

    class Meta:
        unique_together = ("kennel", "breed")
        verbose_name = (
            "порода, которой занимается питомник"  # обьявление о выводке
        )
        verbose_name_plural = "породы в питомниках"  # обьявление о выводке
        ordering = ("kennel", "id")
        db_table = "breed_in_kennel"


class Announcement(models.Model):
    """обьявление"""

    id = models.AutoField
    title = models.CharField(
        db_index=True,
        max_length=100,
        null=False,
        blank=False,
        verbose_name="название обьявления",
    )
    kennel = models.ForeignKey(
        Kennel,
        on_delete=models.CASCADE,
        verbose_name="заводчик",
    )
    breed = models.ForeignKey(
        Breed, on_delete=models.CASCADE, verbose_name="порода"
    )
    birthday = models.DateField(
        null=False, verbose_name="дата рождения щенков"
    )
    male_count = models.PositiveIntegerField(
        default=0, verbose_name="количество мальчиков"
    )
    female_count = models.PositiveIntegerField(
        default=0, verbose_name="количество девочек"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="описание щенков", max_length=1000
    )
    city = models.CharField(max_length=50, verbose_name="город", null=False)
    parents_description = models.TextField(
        verbose_name="описание родителей",
        blank=True,
        null=True,
        max_length=500,
    )
    is_transportable = models.BooleanField(
        verbose_name="можно отправить в другой город", default=False
    )
    with_documents = models.BooleanField(
        verbose_name="наличие документов на щенков"
    )
    price = models.PositiveIntegerField(default=0, verbose_name="цена")
    created_at = models.DateTimeField(db_index=True, default=now)
    updated_at = models.DateTimeField(db_index=True, default=now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "обьявление"
        verbose_name_plural = "обьявления"
        db_table = "announcement"
        ordering = ("-created_at",)


class AnnouncementPetPhoto(models.Model):
    id = models.AutoField
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        verbose_name="обьявление",
        related_name="pet_photo",
    )
    image = models.ImageField(
        verbose_name="фото щенков",
        upload_to="announcements/pet_photos",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "фотография щенка"
        verbose_name_plural = "фотографии щенков"
        db_table = "announcement_pet_photo"
        ordering = ("announcement", "id")


class AnnouncementParentPhoto(models.Model):
    id = models.AutoField
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        verbose_name="обьявление",
        related_name="parent_photo",
    )
    image = models.ImageField(
        verbose_name="фото родителей",
        upload_to="announcements/parent_photos",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "фотография родителя"
        verbose_name_plural = "фотографии родителей"
        db_table = "announcement_parent_photo"
        ordering = ("announcement", "id")
