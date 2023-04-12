import requests
from django.urls import reverse
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.forms import BaseFormSet, formset_factory
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.middleware import csrf
from django.views import View

from rest_framework import status, generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.views import APIView

from .pagination import DefaultPagination
from .serializers import (
    SurveySerializer,)
from .models import (Survey, User, Customer)

from .permissions import IsOwnerOrReadOnly

# Create your views here.


class SurveyViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'option', 'post']
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticatedOrReadOnly()]
        return [IsOwnerOrReadOnly()]



    def get_serializer_context(self):
        if self.request.method == 'GET':
            return {'customer_id': self.request.user.id, 'request': self.request}
        
        return {'customer_id': self.request.user.id, 'request': self.request, 'survey': self.kwargs['survey_pk']}


class CreateSurveyView(View):
    def get(self, request):
        return render(request, 'base/create_survey.html')

class EditSurveyView(View):
    def get(self, request, pk):
        return render(request, 'base/edit_survey.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'base/login.html')