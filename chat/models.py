from django.db import models
import uuid


class ChatSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    visitor_name = models.CharField(max_length=100, blank=True, default='Visiteur')
    visitor_email = models.EmailField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-last_activity']
        verbose_name = 'Session chat'
        verbose_name_plural = 'Sessions chat'

    def __str__(self):
        return f"Chat #{str(self.session_id)[:8]} — {self.visitor_name}"


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('visitor', 'Visiteur'),
        ('bot', 'Bot automatique'),
        ('admin', 'Équipe La Une'),
    ]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"[{self.sender}] {self.content[:50]}"
