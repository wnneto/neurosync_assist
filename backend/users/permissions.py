from rest_framework.permissions import BasePermission


class IsMedico(BasePermission):
    """Permite acesso apenas a usuários com perfil de médico."""
    def has_permission(self, request, view):
        return hasattr(request.user, 'medico')


class IsPaciente(BasePermission):
    """Permite acesso apenas a usuários com perfil de paciente."""
    def has_permission(self, request, view):
        return hasattr(request.user, 'paciente')


class IsColaborador(BasePermission):
    """Permite acesso apenas a usuários com perfil de colaborador."""
    def has_permission(self, request, view):
        return hasattr(request.user, 'colaborador')


class IsAdminUser(BasePermission):
    """Permite acesso apenas a usuários com superusuário ativo."""
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsMedicoOrAdmin(BasePermission):
    """
    Permite acesso se o usuário for médico ou superusuário (admin).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, 'grupo', None) == 'medico' or request.user.is_superuser
        )
    


class IsMedicoOrColaborador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, 'grupo', None) in ['medico', 'colaborador']
        )