# Generated by Django 3.0.4 on 2020-05-14 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200508_0004'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-appreciated_answer', '-id']},
        ),
    ]
