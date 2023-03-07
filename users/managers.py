from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):
    """
    Create user function. Required fields are passed here.
    """

    def create_user(self, username, email, first_name, last_name, phone, password=None, role='user'):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, last_name, phone, password=None, role='admin'):
        """
        Create superuser function. Use 'createsuperuser' command
        """

        user = self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role=role
        )

        user.save(using=self._db)
        return user
