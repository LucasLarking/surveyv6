from rest_framework import serializers
from .models import Survey, Question, Option, Customer, User
from django.http import HttpResponseRedirect
from rest_framework.exceptions import PermissionDenied
from .permissions import (
    IsOwnerOfSurveyOrReadOnly,
    IsOwnerOrReadOnly)


class SurveySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'customer_id', 'survey', 'description']
        read_only_fields = ['customer_id', 'id']
        partial = False

    def validate_description(self, description):
        if description == 'desc':
            raise serializers.ValidationError('Description cannot be desc')
        return description

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
            print('context', self.context)
            print(request.user)
            request = self.context['request']
            if not request.user.has_perm(IsOwnerOrReadOnly):
                raise PermissionDenied('Yoi are not the owner')
            self.instance = Survey.objects.get(id=self.context['survey'])
            self.instance.survey = self.validated_data['survey']
            self.instance.description = self.validated_data['description']
            self.instance.save()


class EditSurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ['survey', 'description']

        partial = False

    def save(self, **kwargs):

        request = self.context['request']
        if not request.user.has_perm('base.IsOwnerOrReadOnly'):
            raise PermissionDenied(
                'ato perform this action.')

        if request.method == 'PATCH':
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

    def save(self, **kwargs):

        request = self.context['request']
        if not request.user.has_perm(IsOwnerOfSurveyOrReadOnly):
            raise PermissionDenied(
                'You do not have permission to perform this action.')

        if request.method == 'POST':
            self.instance = Question.objects.create(
                survey=Survey.objects.get(id=self.context['survey']),
                question=self.validated_data['question'],
            )
            return self.instance

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)

        instance.save()
        return instance


class EditQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['question']

        partial = False

    def save(self, **kwargs):

        request = self.context['request']
        if not request.user.has_perm(IsOwnerOfSurveyOrReadOnly):
            raise PermissionDenied(
                'You do not have permission to perform this action.')

        if request.method == 'PATCH':
            self.instance = Question.objects.get(survey=self.context['survey'])
            self.instance.question = self.validated_data['question']
            self.instance.save()

            return self.instance
