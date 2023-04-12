from rest_framework import serializers
from .models import Survey, Question, Option, Customer, User
from django.http import HttpResponseRedirect



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
                customer_id=Customer.objects.get(id=self.context['customer_id'])
            )
            return self.instance
        elif request.method == 'PATCH':
            self.instance = Survey.objects.get(id=self.context['survey'])
            self.instance.survey =self.validated_data['survey']
            self.instance.description =self.validated_data['description']
            self.instance.save()
        
        