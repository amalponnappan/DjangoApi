from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# following is the example of Generic views and Mixins api cretation

class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated]

    def get(self,req,id=None):
        if id:
            return self.retrieve(req)
        else:
            return self.list(req)
    def post(self,req):
        return self.create(req)
    def put(self,req,id=None):
        return self.update(req)
    def delete(self,req,id):
        return self.destroy(req,id)

# following is the example of Class based api cretation

class ArticleAPIView(APIView):
    def get(self,req):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    def post(self,req):
        serializer = ArticleSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):
    def get_object(self,pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    def get(self,req,pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    def put(self,req,pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,req,pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# following is the example of function based api cretation

# @csrf_exempt
@api_view(['GET','POST'])
def article_list(req):
    if req.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)
    elif req.method == 'POST':
        # data = JSONParser().parse(req)
        serializer = ArticleSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data,status=201)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors,status=400)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(req,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        # return HttpResponse(status=404)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if req.method == 'GET':
        serializer = ArticleSerializer(article)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)
    elif req.method =='PUT':
        # data = JSONParser().parse(req)
        # serializer = ArticleSerializer(article,data=data)
        serializer = ArticleSerializer(article,data=req.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data)
            return Response(serializer.data)
        # return JsonResponse(serializer.errors,status=400)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif req.method =='DELETE':
        article.delete()
        # return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)
