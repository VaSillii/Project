from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import UserAccount, Profile, Education, NameEducationalInstitution, Comment


class FormRegister(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(), label="Email:")
    username = forms.CharField(max_length=100, label="Имя пользователя:")
    surname = forms.CharField(max_length=100, label="Фамилия:")
    name = forms.CharField(max_length=100, label="Имя:")
    patronymic = forms.CharField(max_length=100, label="Отчество:")
    phone_number = forms.CharField(max_length=12, label="Номер телефона:")
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    # Стилизация формы
    def __init__(self, *args, **kwargs):
        super(FormRegister, self).__init__(*args, **kwargs)

        for item in self.fields:
            self.fields[item].widget = forms.TextInput(attrs={'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # profile =
        if commit:
            prof = Profile.objects.create(
                surname=self.cleaned_data['surname'],
                name=self.cleaned_data['name'],
                patronymic=self.cleaned_data['patronymic'],
                phone_number=self.cleaned_data['phone_number'],
            )
            user.profile = prof
            user.save()
        return user

    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'password1', 'password2')


class FormEdit(ModelForm):
    surname = forms.CharField(max_length=100, label="Фамилия:")
    name = forms.CharField(max_length=100, label="Имя:")
    patronymic = forms.CharField(max_length=100, label="Отчество:")
    phone_number = forms.CharField(required=False, label="Номер телефона:")
    dob = forms.DateField(
        widget=forms.DateInput(format=('%d-%m-%Y')), required=False, label="Дата рождения:")
    about_me = forms.CharField(widget=forms.Textarea(), required=False, label="Обо мне:")
    addition_info = forms.CharField(widget=forms.Textarea(), required=False, label="Дополнмительная информация:")
    avatar_user = forms.FileField(required=False, widget=forms.FileInput, label="Фото:")
    position = forms.ChoiceField(choices=Profile.POSITIONS, label="Позиция")

    university = forms.CharField(required=False, label="Университет:")
    faculty = forms.CharField(max_length=300,  required=False, label="Факультет:")
    specialization = forms.CharField(max_length=300,  required=False, label="Специальность:")
    graduation_date = forms.DateField(
        widget=forms.DateInput(format=('%d-%m-%Y')), required=False, label="Дата окончания:")

    type_work = forms.CharField(required=False, label="Тип работ:")
    price = forms.CharField(required=False, label="Стоимость работ:")

    email = forms.EmailField(max_length=200, label="Email:")
    username = forms.CharField(max_length=100, label="Имя пользователя:")


    # Стилизация формы
    def __init__(self, *args, **kwargs):
        super(FormEdit, self).__init__(*args, **kwargs)

        for item in self.fields:
            self.fields[item].widget = forms.TextInput(attrs={'class': 'form-control'})

    class Meta:
        model = UserAccount
        fields = ('username', 'email',)


class FormComment(ModelForm):
    user = forms.CharField(required=False, label="Пользователь:")
    user_comment = forms.CharField(required=False, label="Комментирующий пользователь:")
    text_message = forms.CharField(widget=forms.Textarea(), required=False, label="Отзыв:")
    assessment = forms.IntegerField(required=False, min_value=0, max_value=5, widget=forms.IntegerField, label="Оценка (0-5):")

    # Стилизация формы
    def __init__(self, *args, **kwargs):
        super(FormComment, self).__init__(*args, **kwargs)

        for item in self.fields:
            self.fields[item].widget = forms.TextInput(attrs={'class': 'form-control'})

    class Meta:
        model = Comment
        fields = ('text_message', 'assessment',)
