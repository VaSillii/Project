from django.db import models
from django.utils import timezone

from accounts.models import Specialization, TypeWork, UserAccount


class Order(models.Model):
    client = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='client', verbose_name='Заказчик')
    master = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='master', verbose_name='Исполнитель')
    spec_order = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name='Специализация заказа')
    type_work = models.ForeignKey(TypeWork, on_delete=models.CASCADE, verbose_name='Тип работы')
    date_of_completion = models.DateField(default=timezone.now, verbose_name="Дата выполнения работы", null=True)
    price = models.IntegerField(default=0, verbose_name='Стоимость работы')

    def __str__(self):
        return 'исполнитель: {}; тип работы: {}'.format(self.master, self.type_work)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

