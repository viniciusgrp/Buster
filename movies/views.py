from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        movie = Movie.objects.all()

        result_page = self.paginate_queryset(movie, request, view=self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
    

    def post(self, request: Request) -> Response:
        data = request.data

        serializer = MovieSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(serializer.data, status.HTTP_201_CREATED) 
    

class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data)
    

    def patch(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
    

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class MovieOrderView(APIView):
    permission_classes = [IsAuthenticated]

    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)

        self.check_object_permissions(request, movie)

        serializer = MovieOrderSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        serializer.save( user=request.user, movie=movie)

        return Response(serializer.data, status.HTTP_201_CREATED)
    