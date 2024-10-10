from django.views import View
from django.shortcuts import render

from users.forms import UserCreateForm


class CreateUserView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(
            request,
            "users/create_user.html",
            context={
                "form": form,
            },
        )
