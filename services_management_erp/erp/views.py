import csv
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .sections import SECTIONS, MENU
from .forms import form_for
from . import models

class LoginView(DjangoLoginView):
 template_name='registration/login.html'
 redirect_authenticated_user=True
 def form_valid(self,form):
  messages.success(self.request,'Welcome back.')
  return super().form_valid(form)

def logout_view(request):
 if request.method=='POST': logout(request)
 return redirect('login')

@login_required
def dashboard(request):
 today=timezone.localdate()
 context={'menu':MENU,'client_count':models.Client.objects.count(),'active_projects':models.Project.objects.filter(status='active').count(),'open_tasks':models.Task.objects.exclude(status__in=['completed','cancelled']).count(),'open_tickets':models.Ticket.objects.exclude(status__in=['resolved','closed']).count(),'invoice_total':models.Invoice.objects.exclude(status='cancelled').aggregate(v=Sum('total'))['v'] or 0,'expense_total':models.Expense.objects.filter(status='approved').aggregate(v=Sum('amount'))['v'] or 0,'outstanding':sum((i.outstanding for i in models.Invoice.objects.exclude(status='cancelled')), start=0),'recent_projects':models.Project.objects.select_related('client').order_by('-created_at')[:6],'recent_invoices':models.Invoice.objects.select_related('client').order_by('-created_at')[:6],'pending_approvals':models.Approval.objects.filter(status='pending').count(),'today':today}
 return render(request,'erp/dashboard.html',context)

def get_section(section):
 try: return SECTIONS[section]
 except KeyError: raise Http404('Unknown ERP module')

@login_required
def record_list(request,section):
 label,model=get_section(section)
 qs=model.objects.all().order_by('-id')
 query=request.GET.get('q','').strip()
 if query:
  from django.db.models import Q
  fields=[f.name for f in model._meta.fields if getattr(f,'get_internal_type',lambda: '')() in ('CharField','TextField','EmailField')]
  cond=Q()
  for field in fields: cond |= Q(**{f'{field}__icontains':query})
  if fields: qs=qs.filter(cond)
 page=Paginator(qs,20).get_page(request.GET.get('page'))
 return render(request,'erp/record_list.html',{'menu':MENU,'label':label,'section':section,'page_obj':page,'query':query,'display_fields':[f for f in model._meta.fields if f.name not in ('id','created_at','updated_at')]})

@login_required
def record_create(request,section):
 label,model=get_section(section); Form=form_for(model)
 if request.method=='POST':
  form=Form(request.POST,request.FILES)
  if form.is_valid():
   obj=form.save(); messages.success(request,f'{label.rstrip("s")} created successfully.'); return redirect('record_detail',section=section,pk=obj.pk)
 else: form=Form()
 return render(request,'erp/record_form.html',{'menu':MENU,'label':label,'section':section,'form':form,'heading':f'New {label.rstrip("s")}'})

@login_required
def record_detail(request,section,pk):
 label,model=get_section(section); obj=get_object_or_404(model,pk=pk)
 return render(request,'erp/record_detail.html',{'menu':MENU,'label':label,'section':section,'object':obj,'fields':[(f.verbose_name,getattr(obj,f.name)) for f in model._meta.fields if f.name not in ('id',)]})

@login_required
def record_update(request,section,pk):
 label,model=get_section(section); obj=get_object_or_404(model,pk=pk); Form=form_for(model)
 if request.method=='POST':
  form=Form(request.POST,request.FILES,instance=obj)
  if form.is_valid(): form.save(); messages.success(request,'Record updated.'); return redirect('record_detail',section=section,pk=obj.pk)
 else: form=Form(instance=obj)
 return render(request,'erp/record_form.html',{'menu':MENU,'label':label,'section':section,'form':form,'heading':f'Edit {label.rstrip("s")}'})

@login_required
def record_delete(request,section,pk):
 label,model=get_section(section); obj=get_object_or_404(model,pk=pk)
 if request.method=='POST':
  obj.delete(); messages.success(request,'Record deleted.'); return redirect('record_list',section=section)
 return render(request,'erp/confirm_delete.html',{'menu':MENU,'label':label,'section':section,'object':obj})

@login_required
def reports(request):
 return render(request,'erp/reports.html',{'menu':MENU,'projects':models.Project.objects.count(),'clients':models.Client.objects.count(),'hours':models.TimeEntry.objects.aggregate(v=Sum('hours'))['v'] or 0,'billable':models.TimeEntry.objects.filter(billable=True).aggregate(v=Sum('hours'))['v'] or 0,'revenue':models.Invoice.objects.exclude(status='cancelled').aggregate(v=Sum('total'))['v'] or 0,'expenses':models.Expense.objects.filter(status='approved').aggregate(v=Sum('amount'))['v'] or 0})

@login_required
def export_csv(request,section):
 label,model=get_section(section); response=HttpResponse(content_type='text/csv'); response['Content-Disposition']=f'attachment; filename="{section}.csv"'
 writer=csv.writer(response); fields=[f for f in model._meta.fields if f.name!='id']; writer.writerow([f.verbose_name for f in fields])
 for obj in model.objects.all().iterator(): writer.writerow([getattr(obj,f.name) for f in fields])
 return response
