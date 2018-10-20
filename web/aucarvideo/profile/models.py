from django.db import models
from django.contrib.auth.models import User

company_name = models.CharField(max_length=32)
company_name.contribute_to_class(User, 'company_name')