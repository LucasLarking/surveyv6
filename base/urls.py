from django.urls import path, include

from rest_framework_nested import routers
from .views import (
    SurveyViewSet,
    QuestionViewSet,
    OptionViewSet,
    LoginView,
    CreateSurveyView,
    EditSurveyView)


router = routers.DefaultRouter()
router.register('surveys', SurveyViewSet)
survey_router = routers.NestedDefaultRouter(router, 'surveys', lookup='survey')
survey_router.register('questions', QuestionViewSet, basename='survey-question')


question_router = routers.NestedDefaultRouter(survey_router, 'questions', lookup='question')
question_router.register('options', OptionViewSet, basename='survey-option')

# survey_router.register('options', OptionViewSet, basename='survey-option')

urlpatterns = router.urls + survey_router.urls + question_router.urls

urlpatterns += [path('create_survey', CreateSurveyView.as_view(), name='create_survey')]
urlpatterns += [path('edit_survey/<str:pk>', EditSurveyView.as_view(), name='edit_survey')]
urlpatterns += [path('login', LoginView.as_view(), name='login'),]