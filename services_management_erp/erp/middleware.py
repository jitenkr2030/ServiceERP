from .models import AuditLog
class AuditMiddleware:
 def __init__(self,get_response): self.get_response=get_response
 def __call__(self,request):
  response=self.get_response(request)
  if request.user.is_authenticated and request.method in ('POST','PUT','PATCH','DELETE') and not request.path.startswith('/accounts/'):
   # Business object changes are also available through Django admin; this records request-level activity.
   AuditLog.objects.create(user=request.user,action=request.method,model_name='HTTP',object_id='',detail=request.path,ip_address=request.META.get('REMOTE_ADDR'))
  return response
