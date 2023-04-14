import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from rest_framework import status, generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .pagination import DefaultPagination
from .serializers import (
    SurveySerializer,
    QuestionSerializer,
    OptionSerializer
    )
from .models import (
    Survey,
    Question,
    Option,
    User,
    Customer)

# Create your views here.


class SurveyViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'option', 'post']
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_serializer_context(self):
        if self.request.method in permissions.SAFE_METHODS or self.request.method == 'POST':
            return {'customer_id': self.request.user.id, 'request': self.request}
        
        return {'customer_id': self.request.user.id, 'request': self.request, 'survey': self.kwargs['pk']}



class QuestionViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', 'head', 'option', 'post', 'patch']
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    
    def get_serializer_context(self):
        if self.request.method == 'PATCH':
            return {'customer_id': self.request.user.id, 'request': self.request, 'survey': self.kwargs['survey_pk'], 'question': self.kwargs['pk']}
        return {'customer_id': self.request.user.id, 'request': self.request, 'survey': self.kwargs['survey_pk']}


class OptionViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', 'head', 'option', 'post', 'patch']
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'customer_id': self.request.user.id, 'request': self.request, 'survey': self.kwargs['survey_pk'], 'question': self.kwargs['question_pk']}

    def get_queryset(self):
        print(self.kwargs)
        return self.queryset.filter(question=Question.objects.get(id=self.kwargs['question_pk']))


class CreateSurveyView(View):
    def get(self, request):
        print(request.user)
        return render(request, 'base/create_survey.html')


class EditSurveyView(View):
    # authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):

        survey_obj = get_object_or_404(Survey, pk=kwargs['pk'])
        return render(request, 'base/edit_survey.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'base/login.html')