# Generated by Django 4.1.2 on 2022-10-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_ticket_image_alter_review_user_alter_ticket_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
