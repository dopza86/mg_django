import jwt
import os
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.base import ContentFile

from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .permissions import IsSelf
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, UserPasswordSerializer
from .models import User
from django.contrib.auth.hashers import make_password

# Create your views here.


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def me(self, request):
        me = request.user
        serializer = UserSerializer(me)
        return Response(serializer.data)

    @action(detail=True, methods=["put"])
    def update_user(self, request, pk):
        user = User.objects.get(pk=pk)

        if user is not None:
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                user = serializer.save()

                return Response(UserSerializer(user).data)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=["put"])
    # def update_password(self, request, pk):
    #     user = User.objects.get(pk=pk)

    #     if user is not None:
    #         serializer = UserPasswordSerializer(user,
    #                                             data=request.data,
    #                                             partial=True)

    #         if serializer.is_valid():

    #             user = serializer.save()

    #             return Response(UserPasswordSerializer(user).data)
    #         else:
    #             return Response(serializer.errors,
    #                             status=status.HTTP_400_BAD_REQUEST)
    #         return Response()
    #     else:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode({"pk": user.pk},
                                     settings.SECRET_KEY,
                                     algorithm="HS256")
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # restauth 로 로그인 구현
    @action(detail=False)
    def kakao_login(self, request):
        app_key = os.environ.get("KAKAO_KEY")
        redirect_uri = "http://127.0.0.1:8000/api/v1/users/kakao_callback/"

        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
        )

    @action(detail=False)
    def kakao_callback(self, request):
        try:
            app_key = os.environ.get("KAKAO_KEY")
            code = request.GET.get("code")
            redirect_uri = "http://127.0.0.1:8000/api/v1/users/kakao_callback/"
            post_data = {
                "grant_type": "authorization_code",
                "client_id": app_key,
                "redirect_uri": redirect_uri,
                "code": code,
            }
            token_request = requests.post(
                f"https://kauth.kakao.com/oauth/token", data=post_data)
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise Exception(f"{error}")

            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                )

                profile_json = profile_request.json()
                kakao_account = profile_json.get("kakao_account")
                properties = profile_json.get("properties")
                profile = kakao_account.get("profile")
                email = kakao_account.get("email", None)
                nickname = properties.get("nickname")
                profile_image = properties.get("profile_image")
                try:
                    user = User.objects.get(username=nickname)
                    if user.login_method == User.LOGIN_WEB:
                        raise Exception(
                            f"이미 가입된 회원입니다 아이디와 비밀번호 입력을 통해 로그인을 해주세요 ")

                    if user.login_method == User.LOGIN_GOOGLE:
                        raise Exception(f"이미 가입된 회원입니다 구글로 로그인을 해주세요 ")
                except User.DoesNotExist:
                    user = User.objects.create(
                        username=nickname,
                        email=email,
                        login_method=User.LOGIN_KAKAO,
                    )
                    user.set_unusable_password()
                    user.save()

                    if profile_image is not None:
                        photo_request = requests.get(profile_image)

                        user.avatar.save(f"{nickname}-사진",
                                         ContentFile(photo_request.content))
                login(request, user)

                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_200_OK)
        except:
            raise Exception(f"오류 발생")

    @action(detail=False, methods=["post"])
    def complete_email_verification(self, request):
        email_secret = request.data.get("email_secret")
        try:
            user = User.objects.get(email_secret=email_secret)
            user.email_verified = True
            user.email_secret = ""
            user.save()

        except models.User.DoesNotExist:

            pass
        return Response(status=status.HTTP_200_OK)
