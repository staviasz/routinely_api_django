from django.urls import path
from view.customer_views import (
    RegisterCustomerView,
    LoginCustomerView,
    RefreshLoginView,
    NewPasswordView,
    ForgetPasswordView,
    ConfirmCodeToResetPasswordView,
)

urlpatterns = [
    path("register/", RegisterCustomerView.as_view(), name="register-customer"),
    path("auth/", LoginCustomerView.as_view(), name="auth-customer"),
    path("refresh-auth/", RefreshLoginView.as_view(), name="refresh-customer"),
    path("new-password/", NewPasswordView.as_view(), name="new-password-customer"),
    path(
        "forget-password/",
        ForgetPasswordView.as_view(),
        name="forget-password-customer",
    ),
    path(
        "confirm-code/",
        ConfirmCodeToResetPasswordView.as_view(),
        name="confirm-code-customer",
    ),
]
