from django import forms

from users.enum import UserRole


class UserCreateForm(forms.Form):
    account = forms.CharField(max_length=42, required=True)

    role = forms.ChoiceField(
        choices=[(UserRole.USER.value, "User"), (UserRole.ADMIN.value, "Admin")],
        required=True,
    )

    private_key = forms.CharField(max_length=66, required=True)

    def clean_account(self):
        """
        Check if account is a valid Ethereum address.

        Check that the account address starts with "0x" and has a length of 42 characters.
        If the check fails, raise a forms.ValidationError with message "Невірний формат Ethereum адреси".
        """
        account = self.cleaned_data.get("account")
        if not account.startswith("0x") or len(account) != 42:
            raise forms.ValidationError("Невірний формат Ethereum адреси")
        return account

    def clean_role(self):
        """
        Check if role is a valid UserRole.

        Check that the role is a valid UserRole. If the check fails, raise a forms.ValidationError with message "Невірна роль".
        """
        role = int(self.cleaned_data.get("role"))
        if role not in [role.value for role in UserRole]:
            raise forms.ValidationError("Невірна роль")
        return role
