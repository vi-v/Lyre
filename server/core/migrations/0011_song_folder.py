# Generated by Django 2.0.5 on 2018-05-29 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20180529_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Folder'),
        ),
    ]
