# Generated by Django 5.0.6 on 2024-08-05 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(auto_created=True,primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_profiles/')),
                ('password', models.CharField(max_length=16)),
                ('usertype', models.CharField(max_length=20)),
            ],
        ),
    ]