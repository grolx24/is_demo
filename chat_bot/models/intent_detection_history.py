from django.db import models


class IntentDetectionHistory(models.Model):
    input_message = models.TextField()
    intent_response = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    goal = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['input_message', 'goal'], name='unique_input_message_goal')
        ]

    def __str__(self):
        return self.input_message
