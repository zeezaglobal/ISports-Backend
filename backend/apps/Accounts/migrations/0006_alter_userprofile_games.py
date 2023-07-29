# Generated by Django 4.2.3 on 2023-07-29 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_users_is_active_users_is_admin_users_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='games',
            field=models.CharField(choices=[('ALL', 'All Games'), ('Cricket', 'Cricket'), ('Football', 'Football')], default='All', max_length=10),
        ),
    ]
