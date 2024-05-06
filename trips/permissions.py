from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class IsOwnerLocation(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.trip.created_by == request.user


class IsOwnerPlace(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.location.trip.created_by == request.user
