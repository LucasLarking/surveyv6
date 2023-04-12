from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    # Read permissions are allowed to any request
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print('aa')
        print(obj.customer_id.id, request.user.id)
        return obj.customer_id.user == request.user