"""apkproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apkapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage,name='signup'),
    path('login/', views.LoginPage,name='login'),
    path('admindashboard/', views.admindashboard,name='admindashboard'),
    path('logout/', views.LogoutPage,name='logout'),
    path('userdashboard/', views.userdashboard,name='userdashboard'),

    
    # MIS Module
    # =================================================================================================================
    path('investment_list/', views.investment_list, name='investment_list'),
    path('create_investment/', views.create_investment, name='create_investment'),
    path('investments/update/<int:investment_id>/', views.update_investment, name='update_investment'),
    path('investments/delete/<int:investment_id>/', views.delete_investment, name='delete_investment'),

    path('management_department/', views.management_department, name='management_department'),

    path('manage_staff/', views.manage_staff, name='manage_staff'),
    path('view_staff/<int:employee_id>/', views.view_staff, name='view_staff'),
    path('edit_staff/<int:employee_id>/', views.edit_staff, name='edit_staff'),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('delete_staff/<int:employee_id>/', views.delete_staff, name='delete_staff'),
    
    
    path('manage_salary/', views.manage_salary, name='manage_salary'),
    path('edit_manage_salary/<int:salary_id>/', views.edit_manage_salary, name='edit_manage_salary'),
    path('update_manage_salary/<int:salary_id>/', views.update_manage_salary, name='update_manage_salary'),
    path('delete_manage_salary/<int:salary_id>/', views.delete_manage_salary, name='delete_manage_salary'),
    
    path('download_invoice/', views.download_invoice, name='download_invoice'),


    path('manage_leave_mis/', views.manage_leave_mis, name='manage_leave_mis'),
    path('update_manage_leave/update/<int:pk>/', views.update_manage_leave, name='update_manage_leave'),
    path('delete_manage_leave/delete/<int:pk>/', views.delete_manage_leave, name='delete_manage_leave'),

    path('manage_task/', views.manage_task, name='manage_task'),
    path('edit_manage_task/<int:task_id>/', views.edit_manage_task, name='edit_manage_task'),
    path('update_manage_task/<int:task_id>/', views.update_manage_task, name='update_manage_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),

    path('manage_attendance/', views.manage_attendance, name='manage_attendance'),
    path('delete_manage_attendance/<int:attendance_id>/', views.delete_manage_attendance, name='delete_manage_attendance'),
    path('update_manage_attendance/<int:attendance_id>/', views.update_manage_attendance, name='update_manage_attendance'),
    
    path('add_courier_management/', views.add_courier_management, name='add_courier_management'),
    path('client_document_verified_process/', views.client_document_verified_process, name='client_document_verified_process'),



    path('query_management/', views.query_management, name='query_management'),
    path('add_query/', views.add_mutual_funds, name='add_query'),
    path('mutual_funds/', views.mutual_funds_page, name='mutual_funds_page'),
    
    path('add_fixed_deposit/', views.add_fixed_deposit, name='add_fixed_deposit'),
    path('add_life_insurance/', views.add_life_insurance, name='add_life_insurance'),
    path('add_health_insurance/', views.add_health_insurance, name='add_health_insurance'),
    path('add_general_insurance/', views.add_general_insurance, name='add_general_insurance'),
    path('add_bonds/', views.add_bonds, name='add_bonds'),
    path('add_nps/', views.add_nps, name='add_nps'),

    path('view_query_management/', views.view_query_management, name='view_query_management'),
    path('edit_query_management/', views.edit_query_management, name='edit_query_management'),
    
    path('business_mis/', views.business_mis, name='business_mis'),
    
    path('mis_employee_report/', views.mis_employee_report, name='mis_employee_report'),
    path('view_mis_employee_report/', views.view_mis_employee_report, name='view_mis_employee_report'),
    path('mis_attendance_report/', views.mis_attendance_report, name='mis_attendance_report'),
    path('mis_business_report/', views.mis_business_report, name='mis_business_report'),
    path('mis_dailysalestask_report/', views.mis_dailysalestask_report, name='mis_dailysalestask_report'),
    path('mis_dailysales_product_report/', views.mis_dailysales_product_report, name='mis_dailysales_product_report'),

    # HR Module
    # =================================================================================================================
    # Employee
    # ========
    # ========

    path('employee_creation/', views.employee_creation, name='employee_creation'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('get_employee_data/<int:employee_id>/', views.get_employee_data, name='get_employee_data'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    
    path('salary/', views.salary, name='salary'),
    path('add_salary/', views.add_salary, name='add_salary'),

    path('view_salary/', views.view_salary, name='view_salary'),
    path('edit_salary/<int:salary_id>/', views.edit_salary, name='edit_salary'),
    path('update_salary/<int:salary_id>/', views.update_salary, name='update_salary'),
    path('delete_salary/<int:salary_id>/', views.delete_salary, name='delete_salary'),

    # user management 
    # ===============

    path('user_creation/', views.user_creation, name='user_creation'),
    path('add_admin_user/', views.add_admin_user, name='add_admin_user'),

    path('user_list/', views.user_list, name='user_list'),
    path('delete_admin_user/<int:user_id>/', views.delete_admin_user, name='delete_admin_user'),

    path('assign_role/', views.assign_role, name='assign_role'),

    # Project task management 
    # =======================

    path('add_project/', views.add_project, name='add_project'),
    path('project/', views.project, name='project'),
    path('project/<int:project_id>/', views.project, name='edit_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('update_project/<int:project_id>/', views.update_project, name='update_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),

    path('add_task/', views.add_task, name='add_task'),
    path('task/', views.task, name='task'),
    path('api/companies/', views.get_companies, name='get_companies'),
    path('api/projects/', views.get_projects, name='get_projects'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),

  


    path('add-client/', views.add_client, name='add_client'),
    path('client/', views.client, name='client'),
    path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('update_client/<int:client_id>/', views.update_client, name='update_client'),

    
    path('invoice/', views.invoice, name='invoice'),
    # path('add_invoice/', views.add_invoice, name='add_invoice'),


    path('tax_type/', views.tax_type, name='tax_type'),
    path('add_tax_type/', views.add_tax_type, name='add_tax_type'),
    path('edit_tax_type/<int:tax_id>/', views.edit_tax_type, name='edit_tax_type'),
    path('update_tax_type/<int:tax_id>/', views.update_tax_type, name='update_tax_type'),
    path('delete_tax_type/<int:tax_id>/', views.delete_tax_type, name='delete_tax_type'),

    #organization 
    #============

    path('company_creation/', views.company_creation, name='company_creation'),
    path('add_company/', views.add_company, name='add_company'),
    path('edit_company/<int:company_id>/', views.edit_company, name='edit_company'),
    path('get_company_data/', views.get_company_data, name='get_company_data'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),

    # Department Page___
#___________________________________________________________________________________________

    path("department_creation/", views.department_creation, name="department_creation"),
    path('edit_department/', views.edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),

# Location Page___
#___________________________________________________________________________________________

    path('location/', views.location, name='location'),
    path('add_location/', views.add_location, name='add_location'),
    path('edit_location/<int:location_id>/', views.edit_location, name='edit_location'),
    path('get_location_data/', views.get_location_data, name='get_location_data'),
    path('delete_location/<int:location_id>/', views.delete_location, name='delete_location'),

# Company_policy Page___
#___________________________________________________________________________________________
    path('company_policy/', views.company_policy, name='company_policy'),
    path('add_policy/', views.add_policy, name='add_policy'),
    path('edit_policy/<int:policy_id>/', views.edit_policy, name='edit_policy'),
    path('get_policy_data/', views.get_policy_data, name='get_policy_data'),
    path('delete_policy/<int:policy_id>/', views.delete_policy, name='delete_policy'),

# Desigination Page___
#___________________________________________________________________________________________________

    path('designations/', views.designation_list, name='designation_list'),
    path('add_designation/', views.add_designation, name='add_designation'),
    path('delete_designation/<int:designation_id>/', views.delete_designation, name='delete_designation'),
    path('get_designation_data/<int:designation_id>/', views.get_designation_data, name='get_designation_data'),
    path('edit_designation/<int:designation_id>/', views.edit_designation, name='edit_designation'),

# add_role Page___
#______________________________________________________________________________________________________

    path('role/', views.role, name='role'),
    path('add_role/', views.add_role, name='add_role'),
    path('edit_role/<int:role_id>/', views.edit_role, name='edit_role'),
    path('get_role_data/', views.get_role_data, name='get_role_data'),
    path('delete_role/<int:role_id>/', views.delete_role, name='delete_role'),

#training Page
#_________________________________________________________________________________________________________

    path('training/', views.training_list, name='training_list'),
    path('add_training/', views.add_training, name='add_training'),
    path('get_training_data/<int:training_id>/', views.get_training_data, name='get_training_data'),
    path('edit_training/<int:training_id>/', views.edit_training, name='edit_training'),
    path('delete_training/<int:training_id>/', views.delete_training, name='delete_training'),


    path('branch_creation/', views.branch_creation, name='branch_creation'),
    path('add_branch/', views.add_branch, name='add_branch'),
    path('branch/edit/<int:branch_id>/', views.edit_branch, name='edit_branch'),
    path('branch/update/<int:branch_id>/', views.update_branch, name='update_branch'),
    path('delete_branch/<int:branch_id>/', views.delete_branch, name='delete_branch'), 

    # time sheets 
    # ===========
    path('hr_attendance_list/', views.hr_attendance_list, name='hr_attendance_list'),
    path('add_attendance/', views.add_attendance, name='add_attendance'),
    path('delete_attendance/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
    path('attendance/update/<int:attendance_id>/', views.update_attendance, name='update_attendance'),
    path('timesheet_update_attendance/', views.timesheet_update_attendance, name='timesheet_update_attendance'),
    path('attendance/', views.attendance, name='attendance'),

    path('day_wise_attendance/', views.day_wise_attendance, name='day_wise_attendance'),
    
    path('holiday_list/', views.holiday_list, name='holiday_list'),
    path('holiday_create/', views.holiday_create, name='holiday_create'),
    path('holiday_update/<int:holiday_id>/', views.holiday_update, name='holiday_update'),
    path('holiday_delete/<int:holiday_id>/', views.holiday_delete, name='holiday_delete'),
    path('manage_holiday/', views.manage_holiday, name='manage_holiday'),

    path('manage_leave/', views.manage_leave, name='manage_leave'),
    path('leave_type_list/', views.leave_type_list, name='leave_type_list'),
    path('add_leave_type/', views.add_leave_type, name='add_leave_type'),
    path('leave_types/update/<int:leave_type_id>/', views.update_leave_type, name='update_leave_type'),
    path('leave_types/delete/<int:leave_type_id>/', views.delete_leave_type, name='delete_leave_type'),

    path('leave_request_list/', views.leave_request_list, name='leave_request_list'),
    path('leave_request_create/', views.leave_request_create, name='leave_request_create'),
    path('leave_request/update/<int:pk>/', views.leave_request_update, name='leave_request_update'),
    path('leave_request/delete/<int:pk>/', views.leave_request_delete, name='leave_request_delete'),

    path('monthly_wise_attendance/', views.monthly_wise_attendance, name='monthly_wise_attendance'),


    path('create_office_shift/', views.create_office_shift, name='create_office_shift'),
    path('office_shift_list/', views.office_shift_list, name='office_shift_list'),
    path('update_office_shift/<int:shift_id>/', views.update_office_shift, name='update_office_shift'),
    path('delete_office_shift/<int:shift_id>/', views.delete_office_shift, name='delete_office_shift'),
    path('office_shift/', views.office_shift, name='office_shift'),

    # Hr reports
    # ========== 
    path('attendance_report/', views.attendance_report, name='attendance_report'),
    path('deposite_report/', views.deposite_report, name='deposite_report'),
    path('Employees_report/', views.Employees_report, name='Employees_report'),
    
    path('expenses_report/', views.expenses_report, name='expenses_report'),
    
    path('project_report/', views.project_report, name='project_report'),
    path('task_report/', views.task_report, name='task_report'),
    path('training_report/', views.training_report, name='training_report'),
    path('transaction_report/', views.transaction_report, name='transaction_report'),


    # Payroll
# ==================================================================================================================
# ==================================================================================================================
    path('employee_list/', views.employee_list, name='employee_list'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('attendance/<int:employee_id>/', views.view_attendance, name='view_attendance'),


    path('payroll_list/', views.payroll_list, name='payroll_list'),


    path('department_list/', views.department_list, name='department_list'),
    path('department/<int:department_id>/', views.view_department, name='view_department'),

    path('position_list/', views.position_list, name='position_list'),
    path('desigination/<int:desigination_id>/', views.view_desigination, name='view_desigination'),

    path('allowance_list/', views.allowance_list, name='allowance_list'),
    path('edit_allowance/<int:allowance_id>/', views.edit_allowance, name='edit_allowance'),
    path('delete_allowance/<int:allowance_id>/', views.delete_allowance, name='delete_allowance'),

    path('deduction_list/', views.deduction_list, name='deduction_list'),
    path('update-deduction/<int:deduction_id>/', views.update_deduction, name='update_deduction'),
    path('delete_deduction/<int:deduction_id>/', views.delete_deduction, name='delete_deduction'),

    path('new_payment/', views.new_payment, name='new_payment'),
    path('payment_history/', views.payment_history, name='payment_history'),


# Acounts 
# ===================================================================================================================
# ===================================================================================================================
# master
# ======
    path('add-item/', views.add_item, name='add_item'),
    path('item_creation/', views.item_creation, name='item_creation'), 
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),

    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('supplier_creation/', views.supplier_creation, name='supplier_creation'), 
    path('supplier/<int:supplier_id>/update/', views.update_supplier, name='update_supplier'),
    path('supplier/<int:supplier_id>/delete/', views.delete_supplier, name='delete_supplier'),


    path('new_purchase_return/', views.new_purchase_return, name='new_purchase_return'),
    path('purchase_return_success/', views.purchase_return_success, name='purchase_return_success'),
    path('get_available_quantity_purchase_return/', views.get_available_quantity, name='get_available_quantity_purchase_return'),
    path('purchase_return_list/', views.purchase_return_list, name='purchase_return_list'),
    path('purchase-return/<int:return_id>/', views.view_return_bill, name='view_return_bill'),
    path('purchase-return/<int:return_id>/delete/', views.delete_return, name='delete_return'),

# transaction 
# ===========
    path('purchase/', views.purchase_list, name='purchase_list'),
    path('purchase/new/', views.new_purchase, name='new_purchase'),
    path('purchase/<int:purchase_id>/', views.view_bill, name='view_bill'),
    path('purchase/<int:purchase_id>/delete/', views.delete_bill, name='delete_bill'),
    path('purchase/<int:purchase_id>/confirm-delete/', views.confirm_delete, name='confirm_delete'), 

    path('create_payment_voucher/', views.create_payment_voucher, name='create_payment_voucher'),
    path('view-payment-vouchers/', views.view_payment_vouchers, name='view_payment_vouchers'),

    path('payment_supplier/', views.payment_supplier, name='payment_supplier'), 

    path('add_expenses/', views.add_expenses, name='add_expenses'),
    path('expenses/<int:expense_id>/update/', views.update_expense, name='update-expense'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),

    path('purchase_ledger_report/', views.purchase_ledger_report, name='purchase_ledger_report'),
    path('stock_report/', views.stock_report, name='stock_report'),


    # user 
# ===========
   path('user_courier_management/', views.user_courier_management, name='user_courier_management'), 
   path('user_query_management/', views.user_query_management, name='user_query_management'), 
   path('user_business_mis/', views.user_business_mis, name='user_business_mis'), 
   path('user_travel_allowance/', views.user_travel_allowance, name='user_travel_allowance'), 
   path('user_view_salary/', views.user_view_salary, name='user_view_salary'), 
   path('user_apply_leave/', views.user_apply_leave, name='user_apply_leave'), 
   path('user_ctc_structure/', views.user_ctc_structure, name='user_ctc_structure'), 
   path('user_leave_balance/', views.user_leave_balance, name='user_leave_balance'), 
   path('user_courier_management_report/', views.user_courier_management_report, name='user_courier_management_report'), 
   path('user_query_management_report/', views.user_query_management_report, name='user_query_management_report'), 
   path('user_business_mis_report/', views.user_business_mis_report, name='user_business_mis_report'), 
   path('user_view_salary_report/', views.user_view_salary_report, name='user_view_salary_report'), 
   path('user_apply_leave_report/', views.user_apply_leave_report, name='user_apply_leave_report'), 
   path('user_ctc_structure_report/', views.user_ctc_structure_report, name='user_ctc_structure_report'), 
   path('user_leave_balance_report/', views.user_leave_balance_report, name='user_leave_balance_report'), 
   path('user_travel_allowance_report/', views.user_travel_allowance_report, name='user_travel_allowance_report'), 
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
