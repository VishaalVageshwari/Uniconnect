# Generated by Django 2.2 on 2019-04-23 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20190422_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorship',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutors', to='courses.Courses'),
        ),
    ]
