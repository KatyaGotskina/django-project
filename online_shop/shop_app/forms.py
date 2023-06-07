from django.forms import EmailField, CharField
from django.contrib.auth.forms import UserCreationForm
from . models import Users

class RegistrationForm(UserCreationForm):

    first_name = CharField(max_length=40, required=True)
    surname = CharField(max_length=40)
    last_name = CharField(max_length=40, required=True)
    email = EmailField(required=True)

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'surname', 'last_name', 'email', 'password1', 'password2']
