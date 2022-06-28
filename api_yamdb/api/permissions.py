from rest_framework import permissions


#Спросить Hastred45 про юзеров
class AnonReadOnlyAdminAll(permissions.BasePermission):
    pass
    '''def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser)'''
