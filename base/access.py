from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
        Verify that the current user has the required role.
        This mixin ensures that the user is logged in and has the specified role.
    """

    required_role = None

    def test_func(self):
        """
            Check if the user has the required role.
            Raises a ValueError if required_role is not set.
        """

        if self.required_role is None:
            raise ValueError("required_role must be specified in the view")
        return (self.request.user.is_authenticated and
                hasattr(self.request.user, 'role') and
                self.request.user.role.name == self.required_role)

    def handle_no_permission(self):
        raise PermissionDenied