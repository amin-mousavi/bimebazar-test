# Generated by Django 4.0.1 on 2022-01-29 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='type',
            field=models.CharField(choices=[('Third', 'ثالث'), ('Body', 'بدنه')], max_length=25),
        ),
    ]
