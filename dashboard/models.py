"""
Mirror of uiwiz-backend api.UserProfile for read-only use.
Uses the same DB table (api_userprofile); managed=False so we don't run migrations.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Unmanaged mirror of api.UserProfile; table api_userprofile."""
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="dashboard_profile")
    gemini_api_key_encrypted = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(max_length=1000, blank=True, null=True)

    @property
    def gemini_api_key(self):
        """Decrypt the key for display if encryption key is available."""
        if not self.gemini_api_key_encrypted:
            return None
        
        from django.conf import settings
        from cryptography.fernet import Fernet
        
        key = getattr(settings, "ENCRYPTION_KEY", "")
        if not key:
            return self.gemini_api_key_encrypted
            
        try:
            f = Fernet(key.encode())
            return f.decrypt(self.gemini_api_key_encrypted.encode()).decode()
        except Exception:
            # Fallback to display the encrypted/raw value if decryption fails
            return self.gemini_api_key_encrypted

    class Meta:
        managed = False
        db_table = "api_userprofile"

    def __str__(self):
        return f"Profile of {self.user.username}"


class ChatSession(models.Model):
    """Unmanaged mirror of api.ChatSession; table api_chatsession."""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="admin_chat_sessions")
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "api_chatsession"

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ChatMessage(models.Model):
    """Unmanaged mirror of api.ChatMessage; table api_chatmessage."""
    session = models.ForeignKey(ChatSession, on_delete=models.DO_NOTHING, related_name="messages")
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "api_chatmessage"

    def __str__(self):
        return f"{self.session_id} - {self.role}: {self.content[:20]}"
