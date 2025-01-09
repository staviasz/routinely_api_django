from .docs.customer_docs import (
    RegisterCustomerDoc,
    LoginCustomerDoc,
    NewPasswordDoc,
    ConfirmCodeToResetPasswordCustomerDoc,
    ForgetPasswordDoc,
    RefreshLoginDoc,
)
from .customer_views import (
    RegisterCustomerView,
    NewPasswordView,
    RefreshLoginView,
    LoginCustomerView,
    ForgetPasswordView,
    ConfirmCodeToResetPasswordView,
)

from .docs.task_docs import (
    CreateTaskDoc,
    ListTaskDoc,
    UpdateTaskDoc,
    DeleteTaskDoc,
)
from .task_views import TaskViews
