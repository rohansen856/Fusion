from rest_framework import permissions
from applications.globals.models import HoldsDesignation

class IsStudent(permissions.BasePermission):
    """
    Allows access only to students.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return hasattr(request.user, 'extrainfo') and request.user.extrainfo.user_type == 'student'

class IsTPO(permissions.BasePermission):
    """
    Allows access only to Placement Officers (TPO).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return HoldsDesignation.objects.filter(
            working=request.user,
            designation__name__icontains='placement officer'
        ).exists()

class IsChairman(permissions.BasePermission):
    """
    Allows access only to Placement Chairman.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return HoldsDesignation.objects.filter(
            working=request.user,
            designation__name__icontains='placement chairman'
        ).exists()

class IsRecruiter(permissions.BasePermission):
    """
    Allows access only to registered Recruiters.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.recruitercompanyaccess_set.exists()
