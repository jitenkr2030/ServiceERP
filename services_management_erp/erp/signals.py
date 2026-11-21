from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog
@receiver(post_save)
def audit_save(sender,instance,created,raw=False,**kwargs):
 if raw or sender.__name__ in ('AuditLog','Session','LogEntry','ContentType','Permission','Group'): return
 try:
  AuditLog.objects.create(action='CREATE' if created else 'UPDATE',model_name=sender.__name__,object_id=str(instance.pk),detail='Model saved')
 except Exception: pass
@receiver(post_delete)
def audit_delete(sender,instance,**kwargs):
 if sender.__name__ in ('AuditLog','Session','LogEntry','ContentType','Permission','Group'): return
 try: AuditLog.objects.create(action='DELETE',model_name=sender.__name__,object_id=str(instance.pk),detail='Model deleted')
 except Exception: pass
