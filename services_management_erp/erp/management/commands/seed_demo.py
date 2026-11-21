from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from erp.models import Company,Client,ServiceCategory,Service,Project,Employee,Task
class Command(BaseCommand):
 help='Create demo ERP records and an admin login if none exists.'
 def handle(self,*args,**opts):
  User=get_user_model()
  if not User.objects.filter(is_superuser=True).exists(): User.objects.create_superuser('admin','admin@example.com','Admin@12345')
  company,_=Company.objects.get_or_create(name='Demo Services Pvt. Ltd.')
  client,_=Client.objects.get_or_create(name='ABC Technologies',defaults={'company':company,'email':'accounts@example.com','phone':'9876543210'})
  cat,_=ServiceCategory.objects.get_or_create(name='IT Support')
  Service.objects.get_or_create(code='SUP-001',name='On-site IT Support',defaults={'category':cat,'selling_rate':750,'cost_rate':350})
  project,_=Project.objects.get_or_create(code='PRJ-001',name='ABC Support Setup',defaults={'client':client,'status':'active','contract_value':50000,'budget':25000})
  employee,_=Employee.objects.get_or_create(employee_code='EMP-001',name='Demo Engineer',defaults={'hourly_cost_rate':350,'hourly_billing_rate':750})
  Task.objects.get_or_create(title='Initial site assessment',defaults={'project':project,'assigned_to':employee})
  self.stdout.write(self.style.SUCCESS('Demo data created. Login: admin / Admin@12345 (change immediately).'))
