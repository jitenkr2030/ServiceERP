from rest_framework.routers import DefaultRouter
from .api import viewset_for
from .sections import SECTIONS
router=DefaultRouter()
for slug,(label,model) in SECTIONS.items(): router.register(slug,viewset_for(model),basename=slug)
urlpatterns=router.urls
