# Generated by Django 2.1.1 on 2018-09-26 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('ID_Mentor', models.AutoField(primary_key=True, serialize=False)),
                ('Ime', models.CharField(max_length=35)),
                ('Priimek', models.CharField(max_length=50)),
                ('UpIme', models.CharField(max_length=35)),
                ('Geslo', models.CharField(max_length=50)),
                ('mail', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sodeluje',
            fields=[
                ('ID_Sodeluje', models.AutoField(primary_key=True, serialize=False)),
                ('Mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tekmovanja.Mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Sola',
            fields=[
                ('ID_Sola', models.AutoField(primary_key=True, serialize=False)),
                ('Ime_Sola', models.CharField(max_length=50)),
                ('Vrsta_Sola', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Tekmovanje',
            fields=[
                ('ID_Tekmovanje', models.AutoField(primary_key=True, serialize=False)),
                ('Ime_Tekmovanje', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Uci',
            fields=[
                ('ID_Uci', models.AutoField(primary_key=True, serialize=False)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tekmovanja.Mentor')),
                ('sola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tekmovanja.Sola')),
            ],
        ),
        migrations.AddField(
            model_name='sodeluje',
            name='Tekmovanje',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tekmovanja.Tekmovanje'),
        ),
    ]