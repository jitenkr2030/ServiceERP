from rest_framework import serializers, viewsets
from . import models
class DynamicSerializer(serializers.ModelSerializer):
 class Meta:
  model=None
  fields='__all__'

def serializer_for(model):
 return type(f'{model.__name__}Serializer',(serializers.ModelSerializer,),{'Meta':type('Meta',(),{'model':model,'fields':'__all__'})})
def viewset_for(model):
 serializer=serializer_for(model)
 return type(f'{model.__name__}ViewSet',(viewsets.ModelViewSet,),{'queryset':model.objects.all(),'serializer_class':serializer})
