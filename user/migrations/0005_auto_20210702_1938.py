# Generated by Django 3.2.4 on 2021-07-02 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(max_length=7000, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user.account'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(max_length=7000, on_delete=django.db.models.deletion.CASCADE, related_name='following', to='user.account'),
        ),
    ]