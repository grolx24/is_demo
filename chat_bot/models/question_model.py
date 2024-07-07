from django.db import models


class Question(models.Model):
    user_id = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)
    wait_next = models.BinaryField()
    question = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from User {self.user_id} at {self.timestamp}"
