from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    # Read permissions are allowed to any request
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print('Checking if user is owner')
            return True
        print('aa')
        print('Checking if user is owner')
        print(obj.customer_id.id, request.user.id, 'RESULT:', obj.customer_id.user == request.user)

        return obj.customer_id.user == request.user


class IsOwnerOfSurveyOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('asdsdasd')
        if request.method in permissions.SAFE_METHODS:
            return True
        print('aa')
        print('USERS CUSTOMER ID: ', obj.survey.customer_id)
        print('USERS CUSTOMER ID USER:', obj.survey.customer_id.user, request.user)
        print('IS IT SAME? ', obj.survey.customer_id.user == request.user)
        return obj.survey.customer_id.user == request.user
