from celery import shared_task

from menu.models import Restaurant
from user.models import User


@shared_task
def set_votes_to_default():
    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        restaurant.votes = 0
        restaurant.save()
    users = User.objects.all()

    for user in users:
        user.votes = False
        user.save()
