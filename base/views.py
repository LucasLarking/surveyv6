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
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .pagination import DefaultPagination
from .serializers import (
    SurveySerializer,
    EditSurveySerializer,
    QuestionSerializer,
    EditQuestionSerializer
    )
from .models import (
    Survey,
    Question,
    User,
    Customer)

from .permissions import (IsOwnerOrReadOnly, IsOwnerOfSurveyOrReadOnly)

# Create your views here.


class SurveyViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'option', 'post']
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticatedOrReadOnly()]
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    def get_serializer_context(self):
        if self.request.method in permissions.SAFE_METHODS or self.request.method == 'POST':
            return {'customer_id': self.request.user.id, 'request': self.request}
        
        return {'customer_id': self.request.user.id, 'request': self.request, 'survey': self.kwargs['pk']}

    

    # def partial_update(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
        
    #     # Save the new instance
    #     self.perform_create(serializer)
    #     data = {
    #         "id": serializer.instance.id,
    #         "data": serializer.data,
    #         'csrf_token': csrf.get_token(request)
    #     }
        
    #     return Response(data, status=status.HTTP_201_CREATED)
    

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return SurveySerializer
        elif self.request.method == 'PATCH':
            return EditSurveySerializer



class QuestionViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', 'head', 'option', 'post', 'patch']
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticatedOrReadOnly()]
        if self.request.method == 'POST':
            return [IsOwnerOfSurveyOrReadOnly()]
        return [IsOwnerOfSurveyOrReadOnly()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionSerializer
        elif self.request.method == 'PATCH':
            return EditQuestionSerializer
        return QuestionSerializer

    def get_serializer_context(self):
        return {'customer_id': self.request.user.id, 'request': self.request, 'survey': self.kwargs['survey_pk']}




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