from rest_framework import serializers
from .models import Movie, RatingsMovies, MovieOrder
from accounts.models import Account
from accounts.serializers import AccountSerializer


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, default=None, allow_null=True)
    rating = serializers.ChoiceField(choices=RatingsMovies.choices, default=RatingsMovies.G)
    synopsis = serializers.CharField(default=None, allow_null=True)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj: Movie) -> str:
        return obj.user.email

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)
    

class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField( read_only=True)
    title = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.SerializerMethodField()
    buyed_at = serializers.DateTimeField(read_only=True)

    def get_title(self, obj: Movie)  -> str:
        return obj.movie.title

    def get_buyed_by(self, obj: Account)  -> str: 
        return obj.user.email 
    
    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)