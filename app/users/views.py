from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

from users.forms import UserCreateForm
from users.factory import get_user_manager


class UserCreateView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(
            request,
            "users/create_user.html",
            {
                "form": form,
            },
        )

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            account = form.cleaned_data["account"]
            role = int(form.cleaned_data["role"])
            private_key = form.cleaned_data["private_key"]

            user_manager = get_user_manager()

            try:
                receipt = user_manager.create_user(account, role, private_key)
                return JsonResponse(
                    {
                        "status": "success",
                        "receipt": receipt,
                    }
                )
            except Exception as e:
                return JsonResponse(
                    {"status": "error", "message": str(e)},
                    status=400,
                )
        else:
            return JsonResponse(
                {"status": "error", "errors": form.errors},
                status=400,
            )
