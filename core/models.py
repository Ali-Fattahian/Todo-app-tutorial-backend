from django.db import models
from django.contrib.auth import get_user_model

class Todo(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) # If the author object is deleted, Delete all todos related to it
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return f'{self.author.username}\'s Todo'
