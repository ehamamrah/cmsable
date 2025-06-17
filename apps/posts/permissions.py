from rest_framework import permissions

class IsEditorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsContentManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ['admin', 'content_manager']

class CanCreatePost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.content_moderator()

class CanUpdatePost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.content_moderator()
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_editor():
            return obj.user == request.user
        elif request.user.is_super_updater():
            return True
        else:
            return False

class CanDeletePost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.content_moderator()