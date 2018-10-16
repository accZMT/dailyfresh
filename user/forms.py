from django import forms
from user.models import UserModel


# class UserRegisterForm(forms.Form):
#
#     username = forms.CharField(max_length=10, required=True)
#     password = forms.CharField(max_length=10, required=True)
#     email = forms.EmailField(required=True, )
class UserRegisterForm(forms.Form):
    class Meta:
        model = UserModel
        fields = "__all__"


class UserLoginForm(forms.Form):
    class Meta:
        model = UserModel
        fields = ['username', 'password']
