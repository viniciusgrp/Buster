from django.db import models

class RatingsMovies(models.TextChoices):
    # G, PG, PG-13, R e NC-17
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"

class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True)
    rating = models.CharField(max_length=20, choices=RatingsMovies.choices, default=RatingsMovies.G)
    synopsis = models.TextField(null=True)

    user = models.ForeignKey(
        'accounts.Account', related_name='movies', on_delete=models.CASCADE
    )

class MovieOrder(models.Model):    
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE, related_name="movie_orders")
    user = models.ForeignKey("accounts.Account",on_delete=models.CASCADE, related_name="user_movie_orders")

    buyed_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)