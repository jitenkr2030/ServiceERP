# Services Management ERP — Django full-stack starter

A runnable Django ERP foundation based on the supplied Services Management ERP specification. It includes a responsive Bootstrap dashboard, authenticated CRUD screens, a REST API, PostgreSQL/SQLite configuration, core service-business data models, CSV exports, Django admin, audit events, sample data, and tested financial calculation helpers.

## 1. Requirements
- Python 3.10+
- PostgreSQL 14+ for shared/production use (SQLite is enabled by default for quick local setup)
- Internet connection for Bootstrap and Chart.js CDN assets, or vendor those assets locally for offline deployment

## 2. Run locally (Windows)
```powershell
cd services_management_erp
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
py manage.py makemigrations erp
py manage.py migrate
py manage.py seed_demo
py manage.py runserver
```
Open http://127.0.0.1:8000/

Demo login: `admin` / `Admin@12345` — change this password immediately after first login.

## 3. Run locally (macOS/Linux)
```bash
cd services_management_erp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations erp
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## 4. PostgreSQL setup
Create a database and user, then edit `.env`:
```dotenv
DB_ENGINE=postgres
DB_NAME=services_erp
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=127.0.0.1
DB_PORT=5432
```
Run `python manage.py makemigrations erp` and then `python manage.py migrate` after saving the configuration.

## 5. Main URLs
- `/` — Business dashboard
- `/accounts/login/` — Login
- `/admin/` — Django administration
- `/records/clients/`, `/records/projects/`, `/records/invoices/` etc. — CRUD modules
- `/reports/` — Management snapshot
- `/api/` — REST API root (authenticated)
- `/api/clients/`, `/api/projects/`, `/api/invoices/` etc. — REST endpoints

## 6. Included modules
Organization (company, branch, department), CRM (leads, clients, activities), service catalog, employees/consultants, projects, milestones, tasks, time entries, contracts/SLA fields, invoices and lines, expenses, payments and allocations, tickets, service visits, leave, resource allocations, documents, approvals, notifications, audit log, dashboard, reports and exports.

## 7. Important implementation notes
This is a functional, extensible first release, not a claim that every enterprise feature in the 26-module specification is production-complete. The screens provide generic authenticated create/read/update/delete flows for the included models. The API uses Django REST Framework and session/basic authentication. Role-specific menu/data restrictions, client portal isolation, full approval orchestration, automated recurring invoice scheduler, GST-compliant accounting, revenue recognition, bank reconciliation, TallyPrime synchronization, SMS/WhatsApp, payment gateway and hardened backup/restore are integration or phase-2 work and must be configured and security-tested before production.

The model foundation uses DecimalField for money. The `erp.calculations` service contains reusable financial calculations and `python manage.py test erp` tests the calculation helpers. The current CSV export is a raw module export; date-filtered analytics, PDF packs and advanced drill-down reports can be added on top.

## 8. Production checklist
- Replace `SECRET_KEY`; set `DEBUG=False`; configure `ALLOWED_HOSTS` and HTTPS.
- Use PostgreSQL and automated encrypted backups; test restore procedures.
- Configure email delivery, object storage and background jobs as required.
- Add role/group permissions and tenant/branch scoping to every queryset/API endpoint.
- Validate GST/tax logic with an accountant before issuing live tax invoices.
- Add workflow-specific audit trails and immutable posted financial transactions.
- Run security review, load testing and data migration rehearsal before go-live.

## 9. Suggested next development increments
1. Enforce company/branch tenant scoping and role matrix.
2. Add invoice line editor, tax/discount calculation, payment allocation workflow and PDF invoice.
3. Implement approval state transitions and recurring invoice jobs (Celery/Beat).
4. Build client portal with strict client-level isolation.
5. Add TallyPrime connector after confirming the customer's Tally version, company configuration and permitted interface.
