from django.db import models

from LunchApp.settings import AUTH_USER_MODEL


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    class DayOfTheWeek(models.TextChoices):
        MONDAY = "Monday"
        TUESDAY = "Tuesday"
        WEDNESDAY = "Wednesday"
        THURSDAY = "Thursday"
        FRIDAY = "Friday"
        SATURDAY = "Saturday"
        SUNDAY = "Sunday"

    day_of_the_week = models.CharField(max_length=50, choices=DayOfTheWeek.choices)
    menu = models.TextField()
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menu"
    )

    def __str__(self) -> str:
        return self.day_of_the_week
