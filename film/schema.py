import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Film, ExtraInfo, Ocena, Aktor



class Filters(graphene.InputObjectType):
    tytul_zawiera = graphene.String(default_value="")
    rok_mniejszy_od = graphene.Int(default_value=2000)
    nazwisko_aktora = graphene.String(default_value="")
    short = graphene.Boolean(default_value=True)

#
# Typy
#

class FilmType(DjangoObjectType):
    class Meta:
        model = Film
        fields = ("id", "tytul", "rok", "opis", "premiera", "imdb_points", "owner", "extrainfo")

    stary_nowy_film = graphene.String(default_value="")
    rok2 = graphene.Int()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class ExtraInfoType(DjangoObjectType):
    class Meta:
        model = ExtraInfo
        convert_choices_to_enum = False
        fields = ("id", "czas_trwania", "gatunek", "rezyser", "filmy", "owner")


class OcenaType(DjangoObjectType):
    class Meta:
        model = Ocena
        fields = "__all__"


class AktorType(DjangoObjectType):
    class Meta:
        model = Aktor
        fields = "__all__"

#
# Query
#

class Query(graphene.ObjectType):
    filmy = graphene.List(FilmType, filters=Filters())
    aktorzy = graphene.List(AktorType, filters=Filters())
    # film_wg_id = graphene.Field(FilmType, id=graphene.ID(required=True))
    # extrainfo = graphene.List(ExtraInfoType)
    # extrainfo_wg_id = graphene.Field(ExtraInfoType, id=graphene.String())
    # oceny = graphene.List(OcenaType)
    # oceny_wg_filmu = graphene.List(OcenaType, film_tytul_contains = graphene.String(default_value=""))
    # aktorzy = graphene.List(AktorType, nazwisko_zawiera=graphene.String(default_value=""))


    def resolve_filmy(root, info, filters):
        filmy = Film.objects.all()
        for f in filmy:
            if f.rok < filters.rok_mniejszy_od:
                f.stary_nowy_film = "Stary film"
            else:
                f.stary_nowy_film = "Nowy film"
        if len(filters.tytul_zawiera) > 0:
            films = Film.objects.filter(tytul__contains=filters.tytul_zawiera)
            for f in films:
                if f.rok < filters.rok_mniejszy_od:
                    f.stary_nowy_film = "Stary film"
                else:
                    f.stary_nowy_film = "Nowy film"
            return films
        return filmy


    def resolve_film_wg_id(root, info, id):
        f = Film.objects.get(pk=id)
        f.rok2 = int(f.rok) + 10

        return f


    def resolve_extrainfo(root, info):
        return ExtraInfo.objects.all()


    def resolve_extrainfo_wg_id(root, info, id):
        einfo = ExtraInfo.objects.get(pk=id)
        return einfo


    def resolve_oceny(root, info):
        return Ocena.objects.all()


    def resolve_oceny_wg_filmu(root, info, film_tytul_contains):
        oceny = Ocena.objects.all()
        if film_tytul_contains is not None:
            o = Ocena.objects.filter(film__tytul__contains=film_tytul_contains)
            return o

        return oceny


    def resolve_aktorzy(root, info, filters):
        aktorzy = Aktor.objects.all()
        if len(filters.nazwisko_aktora) > 0:
            aktor = Aktor.objects.filter(nazwisko__contains=filters.nazwisko_aktora)
            return aktor
        return aktorzy


#
# Mutacje
#


class FilmCreateMutation(graphene.Mutation):
    class Arguments:
        tytul = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        imdb_points = graphene.Decimal()
        owner_id = graphene.ID()

    film = graphene.Field(FilmType)

    @classmethod
    def mutate(cls, root, info, tytul, opis, rok, imdb_points, owner_id):
        film = Film.objects.create(tytul=tytul, opis=opis, rok=rok, imdb_points=imdb_points, owner_id=owner_id)
        return FilmCreateMutation(film=film)


class FilmUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tytul = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        imdb_points = graphene.Decimal()
        premiera = graphene.Date(default_value=None)
        owner_id = graphene.ID()

    film = graphene.Field(FilmType)

    @classmethod
    def mutate(cls, root, info, id, tytul, opis, rok, imdb_points, premiera, owner_id):
        film = Film.objects.get(pk=id)
        film.opis = opis
        film.rok = rok
        film.premiera = premiera
        film.imdb_points = imdb_points
        film.owner_id=owner_id
        film.save()
        return FilmUpdateMutation(film=film)


class FilmDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    film = graphene.List(FilmType)

    @classmethod
    def mutate(cls, root, info, id):
        film = Film.objects.get(pk=id).delete()
        film = Film.objects.all()
        return FilmDeleteMutation(film=film)


class Mutation(graphene.ObjectType):
    create_film = FilmCreateMutation.Field()
    update_film = FilmUpdateMutation.Field()
    delete_film = FilmDeleteMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


