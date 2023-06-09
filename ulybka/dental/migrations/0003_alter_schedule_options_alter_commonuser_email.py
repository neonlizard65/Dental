# Generated by Django 4.2.1 on 2023-05-21 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dental', '0002_alter_commonuser_dob_alter_commonuser_patronym_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Расписание', 'verbose_name_plural': 'Расписание'},
        ),
        migrations.AlterField(
            model_name='commonuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Эл. почта'),
        ),
    ]
