# Generated by Django 4.2.4 on 2023-11-29 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_threadscontent_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threadscontent',
            name='content_img',
            field=models.ImageField(default='default/default_image.png', upload_to='content_images/'),
        ),
    ]
