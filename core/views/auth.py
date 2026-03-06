from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from core.services.auth import hash_password, authenticate_user
from core.services.jwt import generate_access_token, generate_refresh_token
from core.models import User
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
	permission_classes = [AllowAny]
	
	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		user = User.objects.create(
			email=serializer.validated_data["email"],
			first_name=serializer.validated_data["first_name"],
			last_name=serializer.validated_data["last_name"],
			patronymic=serializer.validated_data.get("patronymic", ""),
			password_hash=hash_password(serializer.validated_data["password"]),
		)
		# по умолчанию даём роль user
		from core.models import Role, UserRole
		user_role, _ = Role.objects.get_or_create(name="user")
		UserRole.objects.get_or_create(user=user, role=user_role)
		
		return Response({"message": "Пользователь создан"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
	permission_classes = [AllowAny]
	
	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		user = authenticate_user(serializer.validated_data["email"], serializer.validated_data["password"])
		if not user:
			return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
		
		access = generate_access_token(user.id)
		refresh = generate_refresh_token(user.id)
		
		return Response({
			"access_token": access,
			"refresh_token": refresh,
			"user": UserProfileSerializer(user).data
		})


class ProfileView(APIView):
	def get(self, request):
		if not request.user:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		return Response(UserProfileSerializer(request.user).data)
	
	def patch(self, request):
		if not request.user:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		
		serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
	def delete(self, request):
		if not request.user:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		
		request.user.is_active = False
		request.user.save()
		return Response({"message": "Аккаунт деактивирован"}, status=status.HTTP_200_OK)
	