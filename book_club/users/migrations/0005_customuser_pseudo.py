# Generated by Django 3.1.14 on 2023-11-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_email_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pseudo',
            field=models.CharField(blank='False', default='Anonymous', max_length=255),
        ),
    ]
