# Generated by Django 3.0.6 on 2020-06-15 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_completion', models.DateField(default=django.utils.timezone.now, null=True, verbose_name='Дата выполнения работы')),
                ('price', models.IntegerField(default=0, verbose_name='Стоимость работы')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('spec_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Specialization', verbose_name='Специализация заказа')),
                ('type_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.TypeWork', verbose_name='Тип работы')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
