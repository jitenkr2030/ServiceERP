from django.contrib import admin
from . import models
for name in dir(models):
 obj=getattr(models,name)
 if isinstance(obj,type) and issubclass(obj,models.models.Model) and obj is not models.models.Model:
  try: admin.site.register(obj)
  except admin.sites.AlreadyRegistered: pass
admin.site.site_header='Services Management ERP'
admin.site.site_title='Services ERP Admin'
