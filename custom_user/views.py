from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema

from custom_user.models import CustomUser
from custom_user.serializers import *
from project.models import Project
from project.serializers import ProjectSerializer

from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser 

@swagger_auto_schema(method='post', request_body=SignUpSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        address = serializer.validated_data.get('address')
        #account_type = serializer.validated_data.get('account_type', 'basic')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            address=address
            #account_type=account_type
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=SignInSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'id': user.id}, status=status.HTTP_200_OK)



@swagger_auto_schema(method='get', responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def all(request):
    users = User.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(method='put', request_body=UserSerializer, responses={200: UserSerializer()})
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@swagger_auto_schema(method='get', responses={200: UserSerializer()})
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


  
@swagger_auto_schema(methods=['POST'], request_body=ProjectSerializer)
@api_view(['POST',])
@csrf_exempt
def add_project_to_user(request, custom_user_id): 
    #serializer = UpdatebillingSerializer(data=request.data)
    try: 
        custom_user = CustomUser.objects.get(id=custom_user_id) 
    except CustomUser.DoesNotExist: 
        return HttpResponse(status=404) 

    project_data = JSONParser().parse(request) 
    project_serializer = ProjectSerializer(data=project_data) 
    if project_serializer.is_valid(): 
        project_serializer.save() 
        project_id = project_serializer.data["id"]
        custom_user.projects.add(project_id)
        return JsonResponse(project_serializer.data, status=201) 
    
    return JsonResponse(project_serializer.errors, status=400) 
  
