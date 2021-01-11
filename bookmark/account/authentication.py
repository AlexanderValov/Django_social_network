from django.contrib.auth.models import User


class EmailAuthBackend(object):
    '''Выполняет аутентификацию пользователя по e-mail. '''

    def authenticate(self, request, username=None, password=None):
        # пытается получить пользователя, соответствующего указанным электронной почте и 
        # паролю, с помощью метода check_password() модели пользователя. 
        # Этот метод выполняет шифрование пароля и сравнивает результат с тем, 
        # который хранится в базе данных;
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        # получает пользователя по ID, который задается как аргумент user_id.
        # Django использует бэкэнд, который аутентифицировал пользователя,
        # чтобы получать объект User на протяжении всей сессии.
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
