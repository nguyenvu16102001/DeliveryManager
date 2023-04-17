from rest_framework import permissions


class RatingOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, rating):
        return request.user == rating.user
