# Generated by Django 2.2 on 2019-04-13 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
                ('uoc', models.IntegerField()),
                ('prerequisites', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
    ]
