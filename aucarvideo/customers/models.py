from django.db import models

from tenant_schemas.models import TenantMixin

class Client(TenantMixin):
    """
    Tennat descrition
    A Client (tenant) for this application is
    conposed of domain_url and schema_name.
    """

    # The name of the client's enterprice
    name = models.CharField(max_length=100)
    # The date on which the tenant was created
    created_on = models.DateField(auto_now_add=True)
