from rest_framework import permissions


class GlobalPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        model_permission_name = self.__get_model_permission_name(method=request.method, view=view,)

        if not model_permission_name:
            return False

        print(model_permission_name)
        return request.user.has_perm(model_permission_name)

    def __get_model_permission_name(self, method, view):
        try:
            app_name = view.queryset.model._meta.app_label
            model_name = view.queryset.model._meta.model_name
            action_name = self.__get_action_sufix(method)

            return f'{app_name}.{action_name}_{model_name}'
        except AttributeError:
            return None

    def __get_action_sufix(self, method):
        method_actions = {
            'GET': 'view',
            'OPTIONS': 'view',
            'HEAD': 'view',
            'POST': 'add',
            'DELETE': 'delete',
            'PUT': 'change',
            'PATCH': 'change',
        }
        return method_actions.get(method, '')
