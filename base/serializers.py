from rest_framework import serializers
from .models import Survey, Question, Option, Customer, User
from django.http import HttpResponseRedirect
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .permissions import (
    IsOwnerOfSurveyOrReadOnly,
    IsOwnerOrReadOnly)


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'membership']


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SurveySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'customer_id', 'survey', 'description']
        read_only_fields = ['customer_id', 'id']
        partial = False


    def validate(self, attrs):
        request = self.context['request']
        print('Validationg Question')
        if request.method in ['PATCH', 'DELETE']:
            if Survey.objects.get(id=self.context['survey']).customer_id.user != request.user:
                raise serializers.ValidationError('You dont own this survey.')
        return attrs



    def save(self, **kwargs):
        print('saving')
        request = self.context['request']

        if request.method == 'POST':
            self.instance = Survey.objects.create(
                survey=self.validated_data['survey'],
                description=self.validated_data['description'],
                customer_id=Customer.objects.get(
                    id=self.context['customer_id'])
            )
            return self.instance
        elif request.method == 'PATCH':
            print(self.context)
            self.instance = Survey.objects.get(id=self.context['survey'])
            self.instance.survey = self.validated_data['survey']
            self.instance.description = self.validated_data['description']
            self.instance.save()

            return self.instance




class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'survey', 'question']
        read_only_fields = ['survey', 'id']
        partial = False


    def validate(self, attrs):
        request = self.context['request']
        print('Validationg Question')
        if request.method not in permissions.SAFE_METHODS:
            if Survey.objects.get(id=self.context['survey']).customer_id.user != request.user:
                raise serializers.ValidationError('You dont own this survey')
        return attrs

    def save(self, **kwargs):
        print(',akitng')
        request = self.context['request']

        if request.method == 'POST':
            self.instance = Question.objects.create(
                survey=Survey.objects.get(id=self.context['survey']),
                question=self.validated_data['question'],
            )
            return self.instance
    
        if request.method == 'PATCH':
            print(self.context)
            self.instance = Question.objects.get(id=self.context['question'])
            self.instance.question = self.validated_data['question']
            self.instance.save()

            return self.instance

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)

        instance.save()
        return instance


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Option
        fields = ['id', 'option', 'question']
        read_only_fields = ['question', 'id']
        partial = False

    def validate(self, attrs):
        request = self.context['request']
        print('Validationg option')
        if request.method not in permissions.SAFE_METHODS:
            if Survey.objects.get(id=self.context['survey']).customer_id.user != request.user:
                raise serializers.ValidationError('You dont own this survey.')
        return attrs


    def save(self, **kwargs):

        request = self.context['request']

        if request.method == 'POST':
            self.instance = Option.objects.create(
                question=Question.objects.get(id=self.context['question']),
                option=self.validated_data['option'],
            )
            return self.instance

    def update(self, instance, validated_data):
        instance.option = validated_data.get('option', instance.option)

        instance.save()
        return instance
