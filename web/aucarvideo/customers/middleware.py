from tenant_schemas.middleware import BaseTenantMiddleware
from tenant_schemas.utils import get_public_schema_name


class XHeaderTenantMiddleware(BaseTenantMiddleware):
    """
    Determines tenant by the value of the ``X-DTS-SCHEMA`` HTTP header.
    """
    def get_tenant(self, model, hostname, request):
        domain_url = request.META.get('HTTP_X_DTS_SCHEMA', get_public_schema_name())
        tenant = model.objects.get(domain_url=domain_url)
        return tenant