from django.urls import path
from django_.view.customer_views import (
    RegisterCustomerView,
    LoginCustomerView,
    RefreshLoginView,
    NewPasswordView,
    ForgetPasswordView,
    ConfirmCodeToResetPasswordView,
    ConfirmEmailView,
)

urlpatterns = [
    path("", RegisterCustomerView.as_view(), name="register-customer"),
    path("auth/", LoginCustomerView.as_view(), name="auth-customer"),
    path("refresh-auth/", RefreshLoginView.as_view(), name="refresh-customer"),
    path("new-password/", NewPasswordView.as_view(), name="new-password-customer"),
    path(
        "forgot-password/",
        ForgetPasswordView.as_view(),
        name="forget-password-customer",
    ),
    path(
        "confirm-code/",
        ConfirmCodeToResetPasswordView.as_view(),
        name="confirm-code-customer",
    ),
    path("confirm-email/", ConfirmEmailView.as_view(), name="confirm-email-customer"),
]
