# Generated by Django 3.0.1 on 2019-12-28 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0007_complaint_sub_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='level',
            field=models.CharField(default='department', max_length=20),
        ),
    ]
