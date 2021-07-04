# Generated by Django 3.2.4 on 2021-07-02 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_account_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(default=0, max_length=7000, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user.account')),
                ('following', models.ForeignKey(default=0, max_length=7000, on_delete=django.db.models.deletion.CASCADE, related_name='following', to='user.account')),
            ],
            options={
                'db_table': 'follows',
            },
        ),
    ]
