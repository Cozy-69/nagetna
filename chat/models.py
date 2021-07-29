from django.db import models
from django.contrib.auth import get_user_model


user = get_user_model()
class Message(models.Model):
    sender = models.ForeignKey(user, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(user, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("date_created",)
    def __str__(self) :
        return f"{self.sender} --> {self.receiver}"