# Generated by Django 4.2.4 on 2023-11-02 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_likes_for_replies_likes_for_subreplies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='threadscontent',
            name='no_of_comments',
            field=models.IntegerField(default=0),
        ),
    ]
