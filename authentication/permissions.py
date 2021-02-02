from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == 'Admin' or request.user.role == 'Mentor' or request.user.role == 'Student'
        else:
            return request.user.role == 'Admin'


class IsMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == 'Admin' or request.user.role == 'Mentor'
        else:
            return request.user.role == 'Admin'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == 'Admin' or request.user.role == 'Mentor' or request.user.role == 'Student'
        else:
            return request.user.role == 'Student'

        