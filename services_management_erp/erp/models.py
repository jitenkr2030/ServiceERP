from django.conf import settings
from django.db import models
from django.utils import timezone

class TimeStamped(models.Model):
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta: abstract=True

class Company(TimeStamped):
 name=models.CharField(max_length=180)
 legal_name=models.CharField(max_length=180,blank=True)
 gstin=models.CharField(max_length=20,blank=True)
 pan=models.CharField(max_length=20,blank=True)
 email=models.EmailField(blank=True)
 phone=models.CharField(max_length=30,blank=True)
 address=models.TextField(blank=True)
 currency=models.CharField(max_length=3,default='INR')
 def __str__(self): return self.name

class Branch(TimeStamped):
 company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='branches')
 name=models.CharField(max_length=120)
 address=models.TextField(blank=True)
 phone=models.CharField(max_length=30,blank=True)
 def __str__(self): return f'{self.company} - {self.name}'

class Department(TimeStamped):
 company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='departments')
 name=models.CharField(max_length=120)
 def __str__(self): return self.name

class Client(TimeStamped):
 TYPES=[('company','Company'),('individual','Individual'),('government','Government'),('other','Other')]
 STATUS=[('active','Active'),('inactive','Inactive'),('prospect','Prospect')]
 company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='clients',null=True,blank=True)
 name=models.CharField(max_length=180)
 client_code=models.CharField(max_length=40,blank=True)
 client_type=models.CharField(max_length=20,choices=TYPES,default='company')
 industry=models.CharField(max_length=100,blank=True)
 gstin=models.CharField(max_length=20,blank=True)
 pan=models.CharField(max_length=20,blank=True)
 website=models.URLField(blank=True)
 email=models.EmailField(blank=True)
 phone=models.CharField(max_length=30,blank=True)
 contact_person=models.CharField(max_length=120,blank=True)
 billing_address=models.TextField(blank=True)
 service_address=models.TextField(blank=True)
 credit_limit=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 payment_terms_days=models.PositiveIntegerField(default=30)
 opening_balance=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 relationship_manager=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
 status=models.CharField(max_length=20,choices=STATUS,default='active')
 notes=models.TextField(blank=True)
 def __str__(self): return self.name

class Lead(TimeStamped):
 STAGES=[('new','New'),('qualified','Qualified'),('meeting','Meeting'),('proposal','Proposal'),('negotiation','Negotiation'),('won','Won'),('lost','Lost')]
 name=models.CharField(max_length=180)
 organization=models.CharField(max_length=180,blank=True)
 email=models.EmailField(blank=True)
 phone=models.CharField(max_length=30,blank=True)
 source=models.CharField(max_length=80,blank=True)
 stage=models.CharField(max_length=20,choices=STAGES,default='new')
 estimated_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 expected_close=models.DateField(null=True,blank=True)
 assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
 notes=models.TextField(blank=True)
 def __str__(self): return self.name

class ServiceCategory(TimeStamped):
 name=models.CharField(max_length=120,unique=True)
 description=models.TextField(blank=True)
 def __str__(self): return self.name

class Service(TimeStamped):
 BILLING=[('hourly','Hourly'),('daily','Daily'),('fixed','Fixed fee'),('unit','Per unit'),('visit','Per visit'),('retainer','Retainer'),('milestone','Milestone')]
 code=models.CharField(max_length=40,blank=True)
 name=models.CharField(max_length=160)
 category=models.ForeignKey(ServiceCategory,null=True,blank=True,on_delete=models.SET_NULL)
 description=models.TextField(blank=True)
 billing_method=models.CharField(max_length=20,choices=BILLING,default='hourly')
 unit=models.CharField(max_length=40,default='Hour')
 selling_rate=models.DecimalField(max_digits=12,decimal_places=2,default=0)
 cost_rate=models.DecimalField(max_digits=12,decimal_places=2,default=0)
 tax_rate=models.DecimalField(max_digits=5,decimal_places=2,default=18)
 active=models.BooleanField(default=True)
 def __str__(self): return self.name

class Employee(TimeStamped):
 TYPES=[('full_time','Full time'),('part_time','Part time'),('contract','Contract'),('consultant','Consultant'),('freelancer','Freelancer'),('intern','Intern')]
 user=models.OneToOneField(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
 employee_code=models.CharField(max_length=40,blank=True)
 name=models.CharField(max_length=160)
 email=models.EmailField(blank=True)
 phone=models.CharField(max_length=30,blank=True)
 department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.SET_NULL)
 designation=models.CharField(max_length=100,blank=True)
 employment_type=models.CharField(max_length=20,choices=TYPES,default='full_time')
 joining_date=models.DateField(null=True,blank=True)
 hourly_cost_rate=models.DecimalField(max_digits=10,decimal_places=2,default=0)
 hourly_billing_rate=models.DecimalField(max_digits=10,decimal_places=2,default=0)
 skills=models.TextField(blank=True)
 active=models.BooleanField(default=True)
 def __str__(self): return self.name

class Project(TimeStamped):
 STATUS=[('draft','Draft'),('planning','Planning'),('approved','Approved'),('active','Active'),('on_hold','On hold'),('completed','Completed'),('closed','Closed'),('cancelled','Cancelled')]
 BILLING=[('fixed','Fixed price'),('time_material','Time & material'),('hourly','Hourly'),('milestone','Milestone'),('retainer','Retainer'),('internal','Internal')]
 code=models.CharField(max_length=40,blank=True)
 name=models.CharField(max_length=180)
 client=models.ForeignKey(Client,null=True,blank=True,on_delete=models.SET_NULL,related_name='projects')
 manager=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
 department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.SET_NULL)
 description=models.TextField(blank=True)
 start_date=models.DateField(null=True,blank=True)
 planned_end_date=models.DateField(null=True,blank=True)
 actual_end_date=models.DateField(null=True,blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default='planning')
 priority=models.CharField(max_length=20,default='medium')
 billing_method=models.CharField(max_length=20,choices=BILLING,default='time_material')
 contract_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 budget=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 estimated_hours=models.DecimalField(max_digits=10,decimal_places=2,default=0)
 overhead_budget=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 def __str__(self): return self.name

class Milestone(TimeStamped):
 project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='milestones')
 name=models.CharField(max_length=160)
 description=models.TextField(blank=True)
 due_date=models.DateField(null=True,blank=True)
 value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 completion_percent=models.PositiveSmallIntegerField(default=0)
 approved=models.BooleanField(default=False)
 def __str__(self): return self.name

class Task(TimeStamped):
 STATUS=[('new','New'),('todo','To do'),('in_progress','In progress'),('review','Review'),('waiting','Waiting'),('blocked','Blocked'),('completed','Completed'),('cancelled','Cancelled')]
 project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE,related_name='tasks')
 title=models.CharField(max_length=200)
 description=models.TextField(blank=True)
 assigned_to=models.ForeignKey(Employee,null=True,blank=True,on_delete=models.SET_NULL)
 owner=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='owned_tasks')
 priority=models.CharField(max_length=20,default='medium')
 status=models.CharField(max_length=20,choices=STATUS,default='todo')
 start_date=models.DateField(null=True,blank=True)
 due_date=models.DateField(null=True,blank=True)
 estimated_hours=models.DecimalField(max_digits=8,decimal_places=2,default=0)
 completion_percent=models.PositiveSmallIntegerField(default=0)
 def __str__(self): return self.title

class TimeEntry(TimeStamped):
 employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='time_entries')
 project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='time_entries')
 task=models.ForeignKey(Task,null=True,blank=True,on_delete=models.SET_NULL)
 work_date=models.DateField(default=timezone.localdate)
 hours=models.DecimalField(max_digits=7,decimal_places=2)
 billable=models.BooleanField(default=True)
 billing_rate=models.DecimalField(max_digits=10,decimal_places=2,default=0)
 cost_rate=models.DecimalField(max_digits=10,decimal_places=2,default=0)
 description=models.TextField()
 submitted=models.BooleanField(default=False)
 approved=models.BooleanField(default=False)
 @property
 def billable_amount(self): return self.hours*self.billing_rate if self.billable else 0
 @property
 def labour_cost(self): return self.hours*self.cost_rate
 def __str__(self): return f'{self.employee} - {self.work_date}'

class Contract(TimeStamped):
 TYPES=[('amc','AMC'),('retainer','Monthly retainer'),('service','Service agreement'),('consulting','Consulting'),('support','Support'),('fixed','Fixed term')]
 STATUS=[('draft','Draft'),('active','Active'),('expired','Expired'),('renewed','Renewed'),('cancelled','Cancelled')]
 number=models.CharField(max_length=50,unique=True)
 client=models.ForeignKey(Client,on_delete=models.CASCADE,related_name='contracts')
 project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.SET_NULL)
 contract_type=models.CharField(max_length=20,choices=TYPES,default='service')
 start_date=models.DateField()
 end_date=models.DateField()
 value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 billing_frequency=models.CharField(max_length=20,default='monthly')
 renewal_notice_days=models.PositiveIntegerField(default=30)
 response_hours=models.DecimalField(max_digits=7,decimal_places=2,default=0)
 resolution_hours=models.DecimalField(max_digits=7,decimal_places=2,default=0)
 terms=models.TextField(blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default='draft')
 def __str__(self): return self.number

class Invoice(TimeStamped):
 STATUS=[('draft','Draft'),('approved','Approved'),('issued','Issued'),('part_paid','Partially paid'),('paid','Paid'),('overdue','Overdue'),('cancelled','Cancelled'),('disputed','Disputed')]
 number=models.CharField(max_length=50,unique=True)
 client=models.ForeignKey(Client,on_delete=models.PROTECT,related_name='invoices')
 project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.SET_NULL)
 contract=models.ForeignKey(Contract,null=True,blank=True,on_delete=models.SET_NULL)
 invoice_date=models.DateField(default=timezone.localdate)
 due_date=models.DateField()
 subtotal=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 discount=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 tax_amount=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 total=models.DecimalField(max_digits=14,decimal_places=2,default=0)
 status=models.CharField(max_length=20,choices=STATUS,default='draft')
 notes=models.TextField(blank=True)
 @property
 def outstanding(self): return self.total-self.allocations.aggregate(v=models.Sum('amount'))['v'] if self.allocations.exists() else self.total
 def __str__(self): return self.number

class InvoiceLine(TimeStamped):
 invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='lines')
 description=models.CharField(max_length=240)
 quantity=models.DecimalField(max_digits=10,decimal_places=2,default=1)
 rate=models.DecimalField(max_digits=12,decimal_places=2,default=0)
 tax_rate=models.DecimalField(max_digits=5,decimal_places=2,default=0)
 @property
 def amount(self): return self.quantity*self.rate
 def __str__(self): return self.description

class Expense(TimeStamped):
 CATEGORIES=[('travel','Travel'),('accommodation','Accommodation'),('meals','Meals'),('transport','Transportation'),('fuel','Fuel'),('office','Office'),('software','Software'),('hardware','Hardware'),('contractor','Contractor'),('materials','Project materials'),('other','Other')]
 STATUS=[('draft','Draft'),('submitted','Submitted'),('approved','Approved'),('rejected','Rejected'),('reimbursed','Reimbursed')]
 expense_date=models.DateField(default=timezone.localdate)
 employee=models.ForeignKey(Employee,null=True,blank=True,on_delete=models.SET_NULL)
 client=models.ForeignKey(Client,null=True,blank=True,on_delete=models.SET_NULL)
 project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.SET_NULL)
 category=models.CharField(max_length=20,choices=CATEGORIES,default='other')
 vendor=models.CharField(max_length=160,blank=True)
 amount=models.DecimalField(max_digits=12,decimal_places=2)
 tax_amount=models.DecimalField(max_digits=12,decimal_places=2,default=0)
 billable=models.BooleanField(default=False)
 reimbursable=models.BooleanField(default=True)
 receipt=models.FileField(upload_to='expense_receipts/',blank=True)
 description=models.TextField(blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default='draft')
 def __str__(self): return f'{self.category} - {self.amount}'

class Payment(TimeStamped):
 METHODS=[('cash','Cash'),('bank','Bank transfer'),('upi','UPI'),('cheque','Cheque'),('online','Online')]
 client=models.ForeignKey(Client,on_delete=models.PROTECT,related_name='payments')
 invoice=models.ForeignKey(Invoice,null=True,blank=True,on_delete=models.SET_NULL,related_name='payments')
 payment_date=models.DateField(default=timezone.localdate)
 amount=models.DecimalField(max_digits=14,decimal_places=2)
 method=models.CharField(max_length=20,choices=METHODS,default='bank')
 reference=models.CharField(max_length=100,blank=True)
 notes=models.TextField(blank=True)
 def __str__(self): return f'{self.client} - {self.amount}'

class PaymentAllocation(TimeStamped):
 payment=models.ForeignKey(Payment,on_delete=models.CASCADE,related_name='allocations')
 invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='allocations')
 amount=models.DecimalField(max_digits=14,decimal_places=2)

class Ticket(TimeStamped):
 STATUS=[('new','New'),('assigned','Assigned'),('in_progress','In progress'),('waiting','Waiting'),('resolved','Resolved'),('closed','Closed')]
 number=models.CharField(max_length=50,unique=True)
 client=models.ForeignKey(Client,on_delete=models.CASCADE,related_name='tickets')
 project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.SET_NULL)
 contract=models.ForeignKey(Contract,null=True,blank=True,on_delete=models.SET_NULL)
 title=models.CharField(max_length=200)
 description=models.TextField()
 category=models.CharField(max_length=80,default='Support')
 priority=models.CharField(max_length=20,default='medium')
 assigned_to=models.ForeignKey(Employee,null=True,blank=True,on_delete=models.SET_NULL)
 due_date=models.DateTimeField(null=True,blank=True)
 resolved_at=models.DateTimeField(null=True,blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default='new')
 resolution_notes=models.TextField(blank=True)
 def __str__(self): return self.number

class ServiceVisit(TimeStamped):
 ticket=models.ForeignKey(Ticket,null=True,blank=True,on_delete=models.SET_NULL)
 client=models.ForeignKey(Client,on_delete=models.CASCADE)
 engineer=models.ForeignKey(Employee,null=True,blank=True,on_delete=models.SET_NULL)
 scheduled_at=models.DateTimeField()
 check_in=models.DateTimeField(null=True,blank=True)
 check_out=models.DateTimeField(null=True,blank=True)
 location=models.TextField(blank=True)
 work_performed=models.TextField(blank=True)
 parts_used=models.TextField(blank=True)
 client_signature_name=models.CharField(max_length=120,blank=True)
 service_charges=models.DecimalField(max_digits=12,decimal_places=2,default=0)
 travel_expense=models.DecimalField(max_digits=12,decimal_places=2,default=0)

class LeaveRequest(TimeStamped):
 STATUS=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
 employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
 start_date=models.DateField()
 end_date=models.DateField()
 leave_type=models.CharField(max_length=40,default='casual')
 reason=models.TextField(blank=True)
 status=models.CharField(max_length=20,choices=STATUS,default='pending')
 approved_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)

class ResourceAllocation(TimeStamped):
 employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
 project=models.ForeignKey(Project,on_delete=models.CASCADE)
 start_date=models.DateField()
 end_date=models.DateField()
 allocation_percent=models.PositiveSmallIntegerField(default=100)
 planned_hours=models.DecimalField(max_digits=8,decimal_places=2,default=0)

class Activity(TimeStamped):
 TYPES=[('call','Call'),('meeting','Meeting'),('email','Email'),('followup','Follow-up'),('note','Note')]
 client=models.ForeignKey(Client,null=True,blank=True,on_delete=models.CASCADE)
 lead=models.ForeignKey(Lead,null=True,blank=True,on_delete=models.CASCADE)
 assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
 activity_type=models.CharField(max_length=20,choices=TYPES,default='note')
 subject=models.CharField(max_length=180)
 due_at=models.DateTimeField(null=True,blank=True)
 completed=models.BooleanField(default=False)
 notes=models.TextField(blank=True)

class Document(TimeStamped):
 title=models.CharField(max_length=180)
 category=models.CharField(max_length=80,default='General')
 client=models.ForeignKey(Client,null=True,blank=True,on_delete=models.CASCADE)
 project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE)
 file=models.FileField(upload_to='documents/')
 expiry_date=models.DateField(null=True,blank=True)
 uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)

class Approval(TimeStamped):
 STATUS=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
 title=models.CharField(max_length=180)
 module=models.CharField(max_length=80)
 object_reference=models.CharField(max_length=80,blank=True)
 requested_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='approval_requests')
 approver=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name='approvals_to_review')
 status=models.CharField(max_length=20,choices=STATUS,default='pending')
 comments=models.TextField(blank=True)
 decided_at=models.DateTimeField(null=True,blank=True)

class Notification(TimeStamped):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
 title=models.CharField(max_length=180)
 message=models.TextField(blank=True)
 read=models.BooleanField(default=False)
 link=models.CharField(max_length=240,blank=True)

class AuditLog(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
 action=models.CharField(max_length=30)
 model_name=models.CharField(max_length=100)
 object_id=models.CharField(max_length=80,blank=True)
 detail=models.TextField(blank=True)
 ip_address=models.GenericIPAddressField(null=True,blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=['-created_at']
 def __str__(self): return f'{self.action} {self.model_name} {self.object_id}'
