# Generated by Django 4.1.3 on 2022-11-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0002_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='color',
            field=models.CharField(choices=[('teal', 'TEAL'), ('green', 'GREEN'), ('emerald', 'EMERALD'), ('blue', 'BLUE'), ('cyan', 'CYAN'), ('red', 'RED'), ('orange', 'ORANGE'), ('black', 'BLACK'), ('violet', 'VIOLET'), ('pink', 'PINK'), ('yellow', 'YELLOW')], default='cyan', max_length=8),
        ),
    ]
