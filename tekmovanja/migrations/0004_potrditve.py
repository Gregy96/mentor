# Generated by Django 2.1.1 on 2018-10-11 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tekmovanja', '0003_mentor_potrjen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Potrditve',
            fields=[
                ('ID_Potrditve', models.AutoField(primary_key=True, serialize=False)),
                ('ID_Potrditelj', models.ForeignKey(on_delete=None, related_name='Potrditelj', to='tekmovanja.Mentor')),
                ('ID_Zahteva', models.ForeignKey(on_delete=None, related_name='Zahteva', to='tekmovanja.Mentor')),
            ],
        ),
    ]
