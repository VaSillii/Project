from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.db.models import Avg
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # username = self.model.normalize_username(username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        _default_profile, _ = Profile.objects.get_or_create(surname="Service", name=":", patronymic=":")
        extra_fields.setdefault('profile', _default_profile)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UsernameValidator(RegexValidator):
    regex = r'^[\w.-]+$'
    message = 'Enter a valid username. This value may contain only letters, ' \
              'numbers, and /./-/_ characters.'
    flags = 0


class BaseAccount(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = "аккаунт"
        verbose_name_plural = "аккаунты"
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.profile:
            full_name = '%s %s %s' % (self.profile.surname.capitalize(),
                                      self.profile.name.capitalize(),
                                      self.profile.patronymic.capitalize())
        else:
            full_name = "-empty-"
        return full_name.strip()

    get_full_name.short_description = 'ФИО'

    def get_short_name(self):
        """Return the short name for the user."""
        if self.profile:
            full_name = '%s %s. %s.' % (self.profile.surname.capitalize(),
                                        self.profile.name[0:1].upper(),
                                        self.profile.patronymic[0:1].upper())
        else:
            full_name = "-empty-"
        return full_name.strip()
    #
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class UserAccount(BaseAccount):
    class Meta(BaseAccount.Meta):
        swappable = 'AUTH_USER_MODEL'


class Profile(models.Model):
    PATH = 'UserAvatar/'
    PATTERN = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    POSITIONS = (
        ('master', 'Мастер'),
        ('programmer', 'Программист'),
        ('client', 'Заказчик'),
        ('guest', 'Гость')
    )
    position = models.CharField(max_length=30, verbose_name="Позиция", choices=POSITIONS, default='guest')

    surname = models.CharField(max_length=100, verbose_name="Фамилия", null=False, blank=False)
    name = models.CharField(max_length=100, verbose_name="Имя", null=False, blank=False)
    patronymic = models.CharField(max_length=100, verbose_name="Отчество", null=False, blank=False)
    dob = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    phone_number = models.CharField(max_length=12, validators=[RegexValidator(PATTERN)], verbose_name="Номер телефона")
    about_me = models.TextField(blank=True, null=True, verbose_name="О себе")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")
    photo = models.ImageField(upload_to=PATH, blank=True, null=True, verbose_name='Фото пользователя')
    specialization = models.ForeignKey('Specialization', blank=True, null=True, on_delete=models.CASCADE,
                                       verbose_name='Специализация')
    education = models.ForeignKey('Education', blank=True, null=True, on_delete=models.CASCADE,
                                  verbose_name='Образование')
    work_price = models.ForeignKey('WorkPrice', blank=True, null=True, on_delete=models.CASCADE,
                                   verbose_name='Стоимоть работы')

    def get_avatar(self):
        if not self.photo:
            return '/static/img/user_blank.jpg'
        return self.photo.url

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    def get_choice_position(self):
        return dict(self.POSITIONS)

    avatar_tag.short_description = 'Avatar'

    def __str__(self):
        return "{surname} {name} {patronymic}".format(surname=self.surname, name=self.name, patronymic=self.patronymic)

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"


class Specialization(models.Model):
    name = models.CharField(max_length=200, verbose_name='Специализация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"


class Education(models.Model):
    name_university = models.ForeignKey('NameEducationalInstitution', on_delete=models.CASCADE,
                                        verbose_name='Университет')
    faculty = models.CharField(max_length=300, verbose_name='Факультет')
    specialization = models.CharField(max_length=300, verbose_name='Специальность')
    graduation_date = models.DateField(verbose_name="Дата окончания")

    def __str__(self):
        return self.name_university.name

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образования"


class NameEducationalInstitution(models.Model):
    name = models.CharField(max_length=400, verbose_name="Название учебного заведения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Университет"
        verbose_name_plural = "Университеты"


class WorkPrice(models.Model):
    type_work = models.ForeignKey('TypeWork', on_delete=models.CASCADE, verbose_name="Тип работы")
    price = models.IntegerField(default=0, verbose_name="Цена")

    def __str__(self):
        return "{} {}".format(self.type_work, self.price)

    class Meta:
        verbose_name = "Стоимсоть работы"
        verbose_name_plural = "Стоимость работ"


class TypeWork(models.Model):
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name='Специализация')
    name = models.CharField(max_length=150, verbose_name="Тип работы")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип работы"
        verbose_name_plural = "Типы работ"


class Comment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="profile_user", verbose_name='Пользователь')
    user_comment = models.ForeignKey(UserAccount,
                                     on_delete=models.CASCADE,
                                     related_name="comment_user",
                                     verbose_name='Комментирующий Пользователь')
    text_message = models.TextField(verbose_name='Коментарий')
    assessment = models.IntegerField(default=0,
                                     validators=[MinValueValidator(0), MaxValueValidator(5)],
                                     verbose_name='Оценка работы пользователя')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания", null=True)

    @staticmethod
    def avd_assessment(user_id):
        comment = Comment.objects.filter(user_id=user_id)
        avg_review = comment.aggregate(Avg('assessment'))['assessment__avg']
        return avg_review

    def __str__(self):
        return 'user_comment: {}, message: {}'.format(self.user, self.text_message)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
