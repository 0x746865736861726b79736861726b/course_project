from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from loguru import logger

from users.forms import UserCreateForm
from users.factory import get_user_manager
from users.factory import get_auth_service
from users.exceptions.user_exceptions import UserNotRegisteredError
from users.exceptions.signature_exeptions import InvalidSignatureError


@method_decorator(csrf_exempt, name="dispatch")
class AuthenticateUserView(View):
    def post(self, request):
        user_address = request.POST.get("user_address")
        signature = request.POST.get("signature")
        message = request.POST.get("message")
        logger.info(
            f"Authenticating user {user_address} with signature {signature} and message {message}"
        )

        if not user_address or not signature or not message:
            return JsonResponse({"error": "Missing parameters"}, status=400)

        auth_service = get_auth_service()

        try:
            role = auth_service.authenticate_user(user_address, signature, message)
            return JsonResponse({"role": role}, status=200)
        except InvalidSignatureError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except UserNotRegisteredError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)


class UserCreateView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, "users/create_user.html", {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data["account"]
            role = int(form.cleaned_data["role"])
            private_key = form.cleaned_data["private_key"]

            user_manager = get_user_manager()

            try:
                receipt = user_manager.create_user(account, role, private_key)
                return JsonResponse({"status": "success", "receipt": receipt})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        return JsonResponse({"status": "error", "message": "Invalid form"}, status=400)


class UserListView(View):
    def get(self, request):
        """
        GET request handler.

        Returns a rendered page with a list of all users in the UsersContract.
        """
        user_manager = get_user_manager()
        users = user_manager.get_all_users()

        return render(request, "users/list.html", {"users": users})
