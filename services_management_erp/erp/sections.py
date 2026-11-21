from . import models
SECTIONS={
 'clients':('Clients',models.Client), 'leads':('Leads',models.Lead), 'services':('Service catalog',models.Service),
 'projects':('Projects',models.Project), 'milestones':('Milestones',models.Milestone), 'tasks':('Tasks',models.Task),
 'employees':('Employees & consultants',models.Employee), 'time-entries':('Time entries',models.TimeEntry),
 'contracts':('Contracts & SLA',models.Contract), 'invoices':('Invoices',models.Invoice), 'invoice-lines':('Invoice lines',models.InvoiceLine),
 'expenses':('Expenses & claims',models.Expense), 'payments':('Payments & receipts',models.Payment), 'tickets':('Support tickets',models.Ticket),
 'service-visits':('Service visits',models.ServiceVisit), 'leave':('Leave requests',models.LeaveRequest),
 'resource-allocations':('Resource allocations',models.ResourceAllocation), 'activities':('CRM activities',models.Activity),
 'documents':('Documents',models.Document), 'approvals':('Approvals',models.Approval),
 'branches':('Branches',models.Branch), 'departments':('Departments',models.Department),
}
MENU=[('Overview',[('Dashboard','dashboard')]),('CRM & Sales',[('Leads','leads'),('Clients','clients'),('Activities & follow-ups','activities'),('Services','services')]),('Projects & Work',[('Projects','projects'),('Milestones','milestones'),('Tasks','tasks'),('Time entries','time-entries')]),('Team',[('Employees','employees'),('Resource allocations','resource-allocations'),('Leave requests','leave')]),('Contracts & Billing',[('Contracts & SLA','contracts'),('Invoices','invoices'),('Expenses','expenses'),('Payments','payments')]),('Service & Support',[('Support tickets','tickets'),('Service visits','service-visits')]),('Administration',[('Documents','documents'),('Approvals','approvals'),('Branches','branches'),('Departments','departments')])]
