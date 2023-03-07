from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, UserDetailsSerializer, LoginSerializer
from .models import User


class UserCreateView(CreateAPIView):
    """
    Create a new user
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserProfile(RetrieveUpdateDestroyAPIView):
    """
    Get user profile
    """

    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer

    def get_object(self) -> int:
        queryset = self.filter_queryset(self.get_queryset())
        user_id = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, user_id)
        return user_id


class UserLogout(GenericAPIView):
    """
    Logout user with redirect to login page
    """

    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login-user'))


class UserLoginView(GenericAPIView):
    """
    Login user with redirect to link list page
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect(reverse('link-list'))
