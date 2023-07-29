# Generated by Django 4.2.3 on 2023-07-29 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_users_date_of_birth_alter_userprofile_games'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='games',
            field=models.CharField(choices=[('ALL', 'All Games'), ('Cricket', 'Cricket'), ('Football', 'Football')], default='All', max_length=10),
        ),
    ]