from django.db import models


class BookModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title
