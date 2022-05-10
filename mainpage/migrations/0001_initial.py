# Generated by Django 4.0.3 on 2022-05-08 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Сокращённое наименование')),
                ('full_name', models.CharField(max_length=50, verbose_name='Полное наименование')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Наименование')),
            ],
        ),
        migrations.CreateModel(
            name='USD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Стоимость')),
                ('timestamp', models.DateTimeField(verbose_name='Время')),
                ('id_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.currency')),
                ('id_resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.resource')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст статьи')),
                ('time_stamp', models.DateTimeField()),
                ('id_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.currency')),
                ('id_resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.resource')),
            ],
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast', models.FloatField(verbose_name='Прогноз')),
                ('id_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.currency')),
            ],
        ),
        migrations.CreateModel(
            name='EUR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Стоимость')),
                ('timestamp', models.DateTimeField(verbose_name='Время')),
                ('id_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.currency')),
                ('id_resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.resource')),
            ],
        ),
    ]