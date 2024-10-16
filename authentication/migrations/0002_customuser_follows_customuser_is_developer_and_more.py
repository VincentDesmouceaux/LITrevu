# Generated by Django 5.1.1 on 2024-10-02 14:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='follows',
            field=models.ManyToManyField(limit_choices_to={'role': 'USER'}, to=settings.AUTH_USER_MODEL, verbose_name='suit'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_developer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('USER', 'User'), ('DEVELOPER', 'Developer')], default='USER', max_length=10),
        ),
    ]