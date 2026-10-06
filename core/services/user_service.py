"""
UserService - User business logic
"""
from django.core.cache import cache

class UserService:
    @staticmethod
    def get_user_profile(user_id):
        cache_key = f"user_{user_id}"
        user = cache.get(cache_key)
        if user:
            return user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        cache.set(cache_key, user, timeout=3600)
        return user
    