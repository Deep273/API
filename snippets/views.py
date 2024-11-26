from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User


@csrf_exempt
def snippet_list(request):
   """
   List all code snippets, or create a new snippet.
   """
   if request.method == 'GET':
       snippets = Snippet.objects.all()
       serializer = SnippetSerializer(snippets, many=True)
       return JsonResponse(serializer.data, safe=False)

   elif request.method == 'POST':
       data = JSONParser().parse(request)
       serializer = SnippetSerializer(data=data)
       if serializer.is_valid():
           serializer.save()
           return JsonResponse(serializer.data, status=201)
       return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
   """
   Retrieve, update or delete a code snippet.
   """
   try:
       snippet = Snippet.objects.get(pk=pk)
   except Snippet.DoesNotExist:
       return HttpResponse(status=404)

   if request.method == 'GET':
       serializer = SnippetSerializer(snippet)
       return JsonResponse(serializer.data)

   elif request.method == 'PUT':
       data = JSONParser().parse(request)
       serializer = SnippetSerializer(snippet, data=data)
       if serializer.is_valid():
           serializer.save()
           return JsonResponse(serializer.data)
       return JsonResponse(serializer.errors, status=400)

   elif request.method == 'DELETE':
       snippet.delete()
       return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def snippet_list(request):
   """
   List all code snippets, or create a new snippet.
   """
   if request.method == 'GET':
       snippets = Snippet.objects.all()
       serializer = SnippetSerializer(snippets, many=True)
       return Response(serializer.data)

   elif request.method == 'POST':
       serializer = SnippetSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
   """
   Retrieve, update or delete a code snippet.
   """
   try:
       snippet = Snippet.objects.get(pk=pk)
   except Snippet.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)

   if request.method == 'GET':
       serializer = SnippetSerializer(snippet)
       return Response(serializer.data)

   elif request.method == 'PUT':
       serializer = SnippetSerializer(snippet, data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   elif request.method == 'DELETE':
       snippet.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_user(request):
    """
    Create a new user.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Создаем пользователя и хешируем его пароль
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Функция для получения списка пользователей
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()  # Получаем всех пользователей
    serializer = UserSerializer(users, many=True)  # Сериализуем всех пользователей
    return Response(serializer.data)  # Возвращаем данные в формате JSON


# Функция для получения/обновления/удаления конкретного пользователя
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer