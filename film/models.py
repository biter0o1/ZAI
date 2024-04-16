from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender = User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Film(models.Model):
    tytul = models.CharField(max_length=64, blank=False, unique=True)
    rok = models.PositiveSmallIntegerField(blank=False)
    opis = models.TextField(default="")
    premiera = models.DateField(null=True, blank=True)
    imdb_points = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='filmy', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.tytul_z_rokiem()

    def tytul_z_rokiem(self):
        return "{} ({})".format(self.tytul, str(self.rok))


class ExtraInfo(models.Model):
    GATUNEK = {
        (0, 'Inne'),
        (1, 'Horror'),
        (2, 'Komedia'),
        (3, 'Sci-fi'),
        (4, 'Dramat')
    }
    czas_trwania = models.PositiveSmallIntegerField(null=True, blank=True)
    gatunek = models.PositiveSmallIntegerField(choices=GATUNEK, null=True, blank=True)
    rezyser = models.CharField(max_length=50, blank=True, null=True)
    filmy = models.OneToOneField(Film, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='einfo', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.reprezentacja()

    def reprezentacja(self):
        for g in list(self.GATUNEK):
            if g[0] == self.gatunek:
                gok = g[1]
        return "Id zestawu: {}, film: {}, gatunek: {}, czas trwania: {}, reżyser: {}".format(
            self.id, self.filmy.tytul, gok, self.czas_trwania, self.rezyser)


class Ocena(models.Model):
    recenzja = models.TextField(default="", blank=True)
    gwiazdki = models.PositiveSmallIntegerField(default=5)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='oceny', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        rec = self.recenzja[:20] + ' ...'
        return "Film: {}, gwiazdki: {}, recenzja: {}".format(self.film.tytul, str(self.gwiazdki), rec)


class Aktor(models.Model):
    imie = models.CharField(max_length=32)
    nazwisko = models.CharField(max_length=32)
    filmy = models.ManyToManyField(Film, blank=True)
    owner = models.ForeignKey(User, related_name='aktorzy', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{} {}, gra w {} filmach z bazy danych".format(self.imie, self.nazwisko, str(self.filmy.count()))

