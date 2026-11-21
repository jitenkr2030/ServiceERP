from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from erp import views
urlpatterns=[path('admin/',admin.site.urls),path('accounts/login/',views.LoginView.as_view(),name='login'),path('accounts/logout/',views.logout_view,name='logout'),path('',views.dashboard,name='dashboard'),path('records/<slug:section>/',views.record_list,name='record_list'),path('records/<slug:section>/new/',views.record_create,name='record_create'),path('records/<slug:section>/<int:pk>/',views.record_detail,name='record_detail'),path('records/<slug:section>/<int:pk>/edit/',views.record_update,name='record_update'),path('records/<slug:section>/<int:pk>/delete/',views.record_delete,name='record_delete'),path('reports/',views.reports,name='reports'),path('reports/export/<slug:section>.csv',views.export_csv,name='export_csv'),path('api/',include('erp.api_urls'))]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
