from django.forms import ModelForm
from customers.models import Client

# Create the form class.
class ClientForm(ModelForm):
     class Meta:
         model = Client
         fields = ['name']