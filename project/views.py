from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from project.models import * 
from project.serializers import *

from drf_yasg.utils import swagger_auto_schema


from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser 
  

@swagger_auto_schema(methods=['POST'], request_body=ProjectSerializer)
@api_view(['GET', 'POST'])
@csrf_exempt
def project_list(request): 
    """ 
    List all project, or create a new project 
    """
    if request.method == 'GET': 
        project = Project.objects.all() 
        serializer = ProjectSerializer(project, many=True) 
        return JsonResponse(serializer.data, safe=False) 
  
    elif request.method == 'POST': 
        data = JSONParser().parse(request) 
        serializer = ProjectSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data, status=201) 
        return JsonResponse(serializer.errors, status=400) 
  
  
@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=ProjectSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def project_detail(request, pk): 
    try: 
        project = Project.objects.get(pk=pk) 
    except Project.DoesNotExist: 
        return HttpResponse(status=404) 
  
    if request.method == 'GET': 
        serializer = ProjectSerializer(project) 
        return JsonResponse(serializer.data) 
  
    elif request.method == 'PUT': 
        data = JSONParser().parse(request) 
        serializer = ProjectSerializer(project, data=data) 
  
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data) 
        return JsonResponse(serializer.errors, status=400) 
  
    elif request.method == 'DELETE': 
        project.delete() 
        return HttpResponse(status=204) 
    



