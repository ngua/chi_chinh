from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}, {self.email}')"

    def __str__(self):
        return f'{self.name} ({self.email}), {self.date.strftime("%D %H:%M")}'
