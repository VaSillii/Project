from django import forms
from django.forms import ModelForm

from orders.models import Order


class FormOrderWork(ModelForm):
    client = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput, label="Клиент:")
    master = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput, label="Исполнитель:")
    spec_order = forms.CharField(max_length=100, label="Специализация:")
    type_work = forms.CharField(max_length=100, label="Тип работы:")
    date_of_completion = forms.DateField(
        widget=forms.DateInput(format=('%d-%m-%Y')), label="Дата выполнения работ:")
    price = forms.IntegerField(min_value=0, widget=forms.IntegerField, label="Стоимость работы:")

    # Стилизация формы
    def __init__(self, *args, **kwargs):
        super(FormOrderWork, self).__init__(*args, **kwargs)

        for item in self.fields:
            self.fields[item].widget = forms.TextInput(attrs={'class': 'form-control'})

    class Meta:
        model = Order
        fields = '__all__'
