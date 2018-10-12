# Generated by Django 2.1.1 on 2018-10-10 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tekmovanja', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uci',
            name='mentor',
        ),
        migrations.RemoveField(
            model_name='uci',
            name='sola',
        ),
        migrations.AddField(
            model_name='mentor',
            name='sola',
            field=models.ForeignKey(default=1, on_delete=None, to='tekmovanja.Sola'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Uci',
        ),
    ]
