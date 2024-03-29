# Generated by Django 5.0.1 on 2024-03-26 15:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("film", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="filmy",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Aktor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("imie", models.CharField(max_length=32)),
                ("nazwisko", models.CharField(max_length=32)),
                ("filmy", models.ManyToManyField(blank=True, to="film.film")),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="aktorzy",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExtraInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "czas_trwania",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "gatunek",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (4, "Dramat"),
                            (0, "Inne"),
                            (1, "Horror"),
                            (2, "Komedia"),
                            (3, "Sci-fi"),
                        ],
                        null=True,
                    ),
                ),
                ("rezyser", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "filmy",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="film.film",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="einfo",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ocena",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recenzja", models.TextField(blank=True, default="")),
                ("gwiazdki", models.PositiveSmallIntegerField(default=5)),
                (
                    "film",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="film.film",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="oceny",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
