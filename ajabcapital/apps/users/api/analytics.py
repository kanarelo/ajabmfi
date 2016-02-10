from django.db.models import Sum, Avg, Max, Q, Count

from .. import models as user_models

def get_top_new_users(limit=10):
	users = user_models.User.objects.all().order_by('-created_by')[:limit]
	return users

def get_most_active_users():
	users = user_models.User.objects.all().order_by('created_by')[:limit]
	return users

def get_password_expired_users():
	users = []
	return users