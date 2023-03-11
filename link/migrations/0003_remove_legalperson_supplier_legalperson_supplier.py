# Generated by Django 4.1.7 on 2023-03-11 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0002_alter_product_model_alter_product_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legalperson',
            name='supplier',
        ),
        migrations.AddField(
            model_name='legalperson',
            name='supplier',
            field=models.ManyToManyField(
                blank=True, related_name='sellers', to='link.businessunit'
            ),
        ),
    ]
