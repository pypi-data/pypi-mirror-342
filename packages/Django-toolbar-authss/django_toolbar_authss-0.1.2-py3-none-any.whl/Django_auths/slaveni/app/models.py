from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
        ('canceled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    date_time = models.DateTimeField()
    payment_type = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('card', 'Банковская карта')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    status_cancel = models.CharField(max_length=255, blank=True, null=True)
    other_service_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Заявка от {self.user.username} на {self.service.name}"