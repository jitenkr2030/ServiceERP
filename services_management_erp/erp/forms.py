from django import forms
from .sections import SECTIONS
class StyledModelForm(forms.ModelForm):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs)
  for field in self.fields.values():
   field.widget.attrs['class']=('form-check-input' if isinstance(field.widget,forms.CheckboxInput) else 'form-control')
   if isinstance(field.widget,forms.Textarea): field.widget.attrs['rows']=3
   if isinstance(field.widget,forms.DateInput): field.widget.attrs['type']='date'
   if isinstance(field.widget,forms.DateTimeInput): field.widget.attrs['type']='datetime-local'

def form_for(model):
 return type(f'{model.__name__}Form',(StyledModelForm,),{'Meta':type('Meta',(),{'model':model,'fields':'__all__'})})
