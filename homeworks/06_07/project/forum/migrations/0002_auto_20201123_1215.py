# Generated by Django 3.1.2 on 2020-11-23 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='forum.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
