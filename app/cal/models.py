# from datetime import datetime, timedelta
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tittle = models.CharField(max_length=100,
                              blank=True,
                              null=True,
                              default=None)
    notes = models.CharField(max_length=1000,
                             blank=True,
                             null=True,
                             default=None)
    date = models.DateField()
    time = models.TimeField(null=True)

    pub_date = models.DateTimeField(
        'date published', auto_now=True)
    # def was_added_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.tittle


class SpecialEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.CharField(max_length=1000,
                             blank=True,
                             null=True,
                             default=None)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    pub_date = models.DateTimeField(
        'date published', auto_now=True)

    class Meta:
        ordering = ['date', 'time']


# class SpecialEvent(models.Model):
#     date = models.DateField()
#     # poop = models.BooleanField('Do you poop today?', default=False)
#     pub_date = models.DateTimeField(
#         'date published', auto_now=True)
#     def __str__(self):
#         return self.date


# class UserManager(BaseUserManager):
#     """
#     Django требует, чтобы кастомные пользователи определяли свой собственный
#     класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
#     же самого кода, который Django использовал для создания User (для демонстрации).
#     """

#     def create_user(self, username, email, password=None):
#         """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
#         if username is None:
#             raise TypeError('Users must have a username.')

#         if email is None:
#             raise TypeError('Users must have an email address.')

#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()

#         return user

#     class Meta:
#         abstract = False

#     def create_superuser(self, username, email, password):
#         """ Создает и возввращет пользователя с привилегиями суперадмина. """
#         if password is None:
#             raise TypeError('Superusers must have a password.')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     # Каждому пользователю нужен понятный человеку уникальный идентификатор,
#     # который мы можем использовать для предоставления User в пользовательском
#     # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
#     # повышения скорости поиска в дальнейшем.
#     username = models.CharField(db_index=True, max_length=100, unique=True)

#     # Так же мы нуждаемся в поле, с помощью которого будем иметь возможность
#     # связаться с пользователем и идентифицировать его при входе в систему.
#     # Поскольку адрес почты нам нужен в любом случае, мы также будем
#     # использовать его для входы в систему, так как это наиболее
#     # распространенная форма учетных данных на данный момент (ну еще телефон).
#     email = models.EmailField(db_index=True, unique=True)

#     # Когда пользователь более не желает пользоваться нашей системой, он может
#     # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
#     # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
#     # пользователям способ деактивировать учетку вместо ее полного удаления.
#     # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
#     # далее анализировать информацию.
#     is_active = models.BooleanField(default=True)

#     # Этот флаг определяет, кто может войти в административную часть нашего
#     # сайта. Для большинства пользователей это флаг будет ложным.
#     is_staff = models.BooleanField(default=False)

#     # Временная метка создания объекта.
#     created_at = models.DateTimeField(auto_now_add=True)

#     # Временная метка показывающая время последнего обновления объекта.
#     updated_at = models.DateTimeField(auto_now=True)

#     # Дополнительный поля, необходимые Django
#     # при указании кастомной модели пользователя.

#     # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
#     # для входа в систему. В данном случае мы хотим использовать почту.
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     # Сообщает Django, что определенный выше класс UserManager
#     # должен управлять объектами этого типа.
#     objects = UserManager()

#     def __str__(self):
#         """ Строковое представление модели (отображается в консоли) """
#         return self.email

#     @property
#     def token(self):
#         """
#         Позволяет получить токен пользователя путем вызова user.token, вместо
#         user._generate_jwt_token(). Декоратор @property выше делает это
#         возможным. token называется "динамическим свойством".
#         """
#         return self._generate_jwt_token()

#     def get_full_name(self):
#         """
#         Этот метод требуется Django для таких вещей, как обработка электронной
#         почты. Обычно это имя фамилия пользователя, но поскольку мы не
#         используем их, будем возвращать username.
#         """
#         return self.username

#     def get_short_name(self):
#         """ Аналогично методу get_full_name(). """
#         return self.username

#     def _generate_jwt_token(self):
#         """
#         Генерирует веб-токен JSON, в котором хранится идентификатор этого
#         пользователя, срок действия токена составляет 1 день от создания
#         """
#         dt = datetime.now() + timedelta(days=1)

#         token = jwt.encode({
#             'id': self.pk,
#             'exp': int(dt.strftime('%s'))
#         }, settings.SECRET_KEY, algorithm='HS256')

#         return token.decode('utf-8')
