from rest_framework import permissions

class CanCreatePost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.content_moderator()

class CanUpdatePost(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.content_moderator():
            return False

        post = view.get_object()

        if request.user.is_super_updater():
            return True

        if request.user.is_editor():
            return post.user == request.user
        
        return False

class CanDeletePost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_super_updater():
            return True

        return False