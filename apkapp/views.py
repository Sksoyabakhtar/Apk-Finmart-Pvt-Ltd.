from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,Http404
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from datetime import date
from apkapp.models import Company,Department,Location,CompanyPolicy,Designation,Role
from apkapp.models import AdminUser , Employee ,Training
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound,HttpResponseRedirect,HttpResponseServerError
from datetime import date
from apkapp.models import Company,Department,Location,CompanyPolicy,Designation,Role,Training,Branch
from apkapp.models import AdminUser,Employee,EmployeeSalary,TaxType,Invoice,InvoiceItem
from .models import Attendance
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.paginator import Paginator, Page

# Create your views here.
@login_required(login_url='login')
def admindashboard(request):
    return render(request, 'admin_dashboard.html')

from django.contrib import messages

def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Your password and confirm password do not match.")
            return render(request, 'signup.html')

        my_user = User.objects.create_user(username, email, password)
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html')


from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                # Redirect superusers to the admin dashboard
                return redirect('admindashboard')
            else:
                # Redirect regular users to the about page
                return redirect('userdashboard')
        else:
            # Handle invalid login credentials
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')



def LogoutPage(request):
    logout(request)
    return redirect('login')


def userdashboard(request):
    return render(request, 'user_dashboard.html')

# MIS Module
# ======================================================================================================================
from django.shortcuts import render, redirect
from .models import Investment

def investment_list(request):
    investments = Investment.objects.all()
    return render(request, 'mis/investment_list.html', {'investments': investments})

def create_investment(request):
    if request.method == 'POST':
        name = request.POST['name']
        investment_type = request.POST['type']
        description = request.POST['description']
        duration_of_years = request.POST['duration_of_years']

        Investment.objects.create(
            name=name,
            type=investment_type,
            description=description,
            duration_of_years=duration_of_years
        )
        return redirect('investment_list')

    return render(request, 'mis/create_investment.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Investment

def update_investment(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    if request.method == 'POST':
        investment.name = request.POST['name']
        investment.type = request.POST['type']
        investment.description = request.POST['description']
        investment.duration_of_years = request.POST['duration_of_years']
        investment.save()
        return redirect('investment_list')
    return render(request, 'mis/update_investment.html', {'investment': investment})

def delete_investment(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    if request.method == 'POST':
        investment.delete()
        return redirect('investment_list')
    return render(request, 'mis/delete_investment.html', {'investment': investment})




def management_department(request):
    departments = Department.objects.all()  # Fetch all departments from the database
    companies = Company.objects.all()
    return render(request, 'mis/management_department.html', {"companies": companies, 'departments': departments})


from django.db.models import F
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

def manage_staff(request):
    # Fetch the required data with annotations
    employees = Employee.objects.all().annotate(
        n_pay=F('employeesalary__n_pay')
    )

    # Number of items per page
    items_per_page = 10  # Modify this based on the number of items to display per page

    # Create a Paginator instance
    paginator = Paginator(employees, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the 'employees' for the current page
    current_page = paginator.get_page(page_number)

    return render(request, 'mis/manage_staff.html', {'employees': current_page})


def view_staff(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee_salary = EmployeeSalary.objects.filter(employee_ref=employee)
    return render(request, 'mis/view_staff.html', {'employee': employee, 'employee_salary': employee_salary})

def edit_staff(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee_salary = EmployeeSalary.objects.filter(employee_ref=employee)
    companies = Company.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    roles = Role.objects.all()
    
    return render(request, 'mis/edit_staff.html', {
        'employee': employee,
        'employee_salary': employee_salary,
        'companies': companies,
        'departments': departments,
        'designations': designations,
        'roles': roles
    })

def update_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        employee_salary = get_object_or_404(EmployeeSalary, employee_ref=employee)

        # Update Employee details
        employee.full_name = request.POST.get('full_name', employee.full_name)
        employee.email = request.POST.get('email', employee.email)
        employee.phone = request.POST.get('phone', employee.phone)
        employee.dob = request.POST.get('dob', employee.dob)
        employee.gender = request.POST.get('gender', employee.gender)
        employee.company_id = request.POST.get('company', employee.company_id)
        employee.department_id = request.POST.get('department', employee.department_id)
        employee.designation_id = request.POST.get('designation', employee.designation_id)
        employee.office_shift = request.POST.get('office_shift', employee.office_shift)
        employee.user_name = request.POST.get('username', employee.user_name)
        employee.role_id = request.POST.get('role', employee.role_id)
        employee.attendance_type = request.POST.get('attendance_type', employee.attendance_type)
        employee.joining_date = request.POST.get('joining_date', employee.joining_date)

        if 'user_image' in request.FILES:  # Check if a new image has been uploaded
            employee.user_image = request.FILES['user_image']  

        employee_salary.basic = request.POST.get('basic', employee_salary.basic)
        employee_salary.hra = request.POST.get('hra', employee_salary.hra)
        employee_salary.others = request.POST.get('others', employee_salary.others)
        employee_salary.conv = request.POST.get('conv', employee_salary.conv)
        employee_salary.m_epf = request.POST.get('m_epf', employee_salary.m_epf)
        employee_salary.m_esi = request.POST.get('m_esi', employee_salary.m_esi)
        employee_salary.lta = request.POST.get('lta', employee_salary.lta)
        employee_salary.medical = request.POST.get('medical', employee_salary.medical)
        employee_salary.r_allow = request.POST.get('r_allow', employee_salary.r_allow)
        employee_salary.status = request.POST.get('status', employee_salary.status)
        employee_salary.wages_type = request.POST.get('wages_type', employee_salary.wages_type)
        employee_salary.billable_type = request.POST.get('billable_type', employee_salary.billable_type)
        employee_salary.bonus = request.POST.get('bonus', employee_salary.bonus)
        employee_salary.leave_encash = request.POST.get('leave_encash', employee_salary.leave_encash)
        employee_salary.epf = request.POST.get('epf', employee_salary.epf)
        employee_salary.esi = request.POST.get('esi', employee_salary.esi)
        employee_salary.epf_pension = request.POST.get('epf_pension', employee_salary.epf_pension)
        employee_salary.tds = request.POST.get('tds', employee_salary.tds)
        employee_salary.hr_deduction = request.POST.get('hr_deduction', employee_salary.hr_deduction)
        employee_salary.g_salary = request.POST.get('g_salary', employee_salary.g_salary)
        employee_salary.n_pay = request.POST.get('n_pay', employee_salary.n_pay)
        employee_salary.ctc = request.POST.get('ctc', employee_salary.ctc)
        employee_salary.e_epf = request.POST.get('e_epf', employee_salary.e_epf)
        employee_salary.e_esi = request.POST.get('e_esi', employee_salary.e_esi)
        employee_salary.er_epf = request.POST.get('er_epf', employee_salary.er_epf)
        employee_salary.er_esi = request.POST.get('er_esi', employee_salary.er_esi)
        # Save the changes

        employee.save()
        employee_salary.save()
        return redirect('view_staff', employee_id=employee.id)  # Redirect back to the view_staff page

    return render(request, 'mis/edit_staff.html')


def delete_staff(request, employee_id):
    # Retrieve the employee object or return a 404 error if not found
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        # If the request method is POST, i.e., the delete confirmation form is submitted, proceed with deletion
        employee.delete()
        return redirect('manage_staff')  # Redirect to the staff list or any other appropriate URL after deletion

    # Render a confirmation page for the user to confirm the deletion
    return render(request, 'mis/delete_staff.html', {'employee': employee})



def manage_salary(request):
    salaries = EmployeeSalary.objects.all()
    return render(request, 'mis/manage_salary.html', {'salaries': salaries})

def edit_manage_salary(request, salary_id):
    try:
        salary = EmployeeSalary.objects.get(id=salary_id)
        # Perform actions related to editing salary
        return render(request, 'mis/edit_manage_salary.html', {'salary': salary})
    except EmployeeSalary.DoesNotExist:
        # Handle the case where the salary with the provided ID doesn't exist
        return render(request, 'error.html', {'error_message': 'Salary not found'})

def update_manage_salary(request, salary_id): 
    salary = get_object_or_404(EmployeeSalary, id=salary_id)

    if request.method == 'POST':
        employee_id = request.POST.get('employeeIdSelect')
        employee_name = request.POST.get('employeeNameSelect')
        month = request.POST.get('month')
        if employee_name:
            salary.employee_ref.full_name = employee_name  # Update the Employee Name
            salary.employee_ref.save()
        if month:
            salary.month = month
        # Update salary details from the form data
        salary.basic = request.POST.get('basic')
        salary.hra = request.POST.get('hra')
        salary.others = request.POST.get('others')
        salary.conv = request.POST.get('conv')
        salary.m_epf = request.POST.get('m_epf')
        salary.m_esi = request.POST.get('m_esi')
        # Update other salary fields in a similar manner

        # Newly added fields
        salary.employee_epf = request.POST.get('e_EPF')
        salary.employee_esi = request.POST.get('e_ESI')
        salary.employer_epf = request.POST.get('er_EPF')
        salary.employer_esi = request.POST.get('er_ESI')
        salary.lta = request.POST.get('lta')
        salary.medical = request.POST.get('medical')
        salary.r_allow = request.POST.get('r_allow')
        salary.gross_salary = request.POST.get('g_salary')
        salary.net_pay = request.POST.get('n_pay')
        salary.ctc = request.POST.get('ctc')

        salary.status = request.POST.get('status')
        salary.wages_type = request.POST.get('wagesType')
        salary.billable_type = request.POST.get('billableType')
        salary.bonus = request.POST.get('bonus')
        # Update other fields in a similar manner

        salary.leave_encash = request.POST.get('leaveEncash')
        salary.epf = request.POST.get('epf')
        salary.esi = request.POST.get('esi')
        salary.epf_pension = request.POST.get('epfPension')
        salary.tds = request.POST.get('tds')
        salary.hr_deduction = request.POST.get('hr_deduction')

        # Save the changes
        salary.save()

        # Redirect to a success URL or the salary detail page
        return redirect('manage_salary')  # Redirect to the salary detail page for the employee

    # If the form is not submitted via POST request, render the edit salary form
    return render(request, 'mis/edit_manage_salary.html', {'salary': salary})

def delete_manage_salary(request, salary_id):
    salary = get_object_or_404(EmployeeSalary, pk=salary_id)
    salary.delete()
    return redirect('manage_salary')



def download_invoice(request):
    return render(request, 'mis/download_invoice.html')

def manage_leave_mis(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'mis/manage_leave_mis.html', {'leave_requests': leave_requests})

from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest, Company, Department, Employee, LeaveType

def update_manage_leave(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    if request.method == 'POST':
        company_id = request.POST.get('company')
        department_id = request.POST.get('department')
        employee_id = request.POST.get('employee')
        leave_type_id = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        finish_date = request.POST.get('finish_date')
        status = request.POST.get('status')
        attachment = request.FILES.get('attachment')
        leave_reason = request.POST.get('leave_reason')

        # Fetch related objects
        company = get_object_or_404(Company, id=company_id)
        department = get_object_or_404(Department, id=department_id)
        employee = get_object_or_404(Employee, id=employee_id)
        leave_type = get_object_or_404(LeaveType, id=leave_type_id)

        # Update the LeaveRequest fields
        leave_request.company = company
        leave_request.department = department
        leave_request.employee = employee
        leave_request.leave_type = leave_type
        leave_request.start_date = start_date
        leave_request.finish_date = finish_date
        leave_request.status = status
        leave_request.attachment = attachment
        leave_request.leave_reason = leave_reason

        leave_request.save()

        return redirect('manage_leave_mis')

    companies = Company.objects.all()
    departments = Department.objects.all()
    employees = Employee.objects.all()
    leave_types = LeaveType.objects.all()

    context = {
        'leave_request': leave_request,
        'companies': companies,
        'departments': departments,
        'employees': employees,
        'leave_types': leave_types,
    }

    return render(request, 'mis/update_manage_leave.html', context)


def delete_manage_leave(request, pk):
    leave_request = LeaveRequest.objects.get(pk=pk)

    if request.method == 'POST':
        leave_request.delete()
        return redirect('manage_leave_mis')

    return render(request, 'mis/delete_manage_leave.html', {'leave_request': leave_request})



def manage_task(request):
    tasks = Task.objects.all()
    return render(request, 'mis/manage_task.html', {'tasks': tasks})

def edit_manage_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    companies = Company.objects.all()
    projects = Project.objects.all() 
    
    if request.method == 'POST':
        # Fetch the task instance, update its fields, and save it to the database
        task.title = request.POST.get('title')
        task.company = request.POST.get('company')
        task.start_date = request.POST.get('start_date')
        task.end_date = request.POST.get('end_date')
        task.project = request.POST.get('project')
        task.estimated_hours = request.POST.get('estimated_hours')
        task.project_users = request.POST.get('project_users')
        task.save()
        
        return redirect('manage_task')  # Redirect to the project or task list view
        
    # If the request is GET, render the edit task form
    return render(request, 'mis/edit_manage_task.html', {'task': task, 'companies': companies, 'projects': projects})

def update_manage_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        company_id = request.POST.get('company')  # Retrieve the company ID from the form
        company = Company.objects.get(pk=company_id)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        project_id = request.POST.get('project')
        project = Project.objects.get(pk=project_id)
        estimated_hours = request.POST.get('estimated_hours')
        project_users = request.POST.get('project_users')

        task.title = title
        task.company = company
        task.start_date = start_date
        task.end_date = end_date
        task.project = project
        task.estimated_hours = estimated_hours
        task.project_users = project_users

        task.save()

        return redirect('manage_task')  # Redirect to the task list page after successful update

    return render(request, 'mis/edit_manage_task.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('manage_task')  # Redirect to the task list page after deletion
    
    return HttpResponse("Invalid request method")

def manage_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, 'mis/manage_attendance.html', {'attendances': attendances})

# views.py
from django.shortcuts import redirect
from .models import Attendance

def delete_manage_attendance(request, attendance_id):
    if request.method == 'POST':
        attendance = get_object_or_404(Attendance, pk=attendance_id)
        attendance.delete()
        return redirect('manage_attendance')
    else:
        return HttpResponse(status=405)

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance, Employee, Company

def update_manage_attendance(request, attendance_id):
    # Get the attendance record to update or return a 404 if it doesn't exist
    attendance = get_object_or_404(Attendance, id=attendance_id)

    if request.method == 'POST':
        # Retrieve the updated data from the form
        employee_id = request.POST.get('employee')
        company_id = request.POST.get('company')
        date = request.POST.get('date')
        status = request.POST.get('status')
        clock_in = request.POST.get('clock_in')
        clock_out = request.POST.get('clock_out')

        # Update the existing Attendance instance
        attendance.employee_id = employee_id
        attendance.company_id = company_id
        attendance.date = date
        attendance.status = status
        attendance.clock_in = clock_in
        attendance.clock_out = clock_out

        # Save the updated attendance record
        attendance.save()

        return redirect('manage_attendance')

    # Retrieve employee and company data for the dropdowns
    employees = Employee.objects.all()
    companies = Company.objects.all()

    return render(request, 'mis/update_manage_attendance.html', {'attendance': attendance, 'employees': employees, 'companies': companies})


def add_courier_management(request):
    return render(request, 'mis/add_courier_management.html')

def client_document_verified_process(request):
    return render(request, 'mis/client_document_verified_process.html')



from .models import MutualFund, FixedDeposit,LifeInsurance,HealthInsurance,GeneralInsurance,Bonds,NPS,InsuranceCompany
from random import randint
from itertools import chain

def query_management(request):
    mutual_fund_data = MutualFund.objects.all()
    fixed_deposit_data = FixedDeposit.objects.all()
    life_insurance_data = LifeInsurance.objects.all()
    health_insurance_data = HealthInsurance.objects.all()
    general_insurance_data = GeneralInsurance.objects.all()
    bonds_data = Bonds.objects.all()
    nps_data = NPS.objects.all()

    # Combine all querysets into a single list
    all_data = list(chain(mutual_fund_data, fixed_deposit_data, life_insurance_data,
                          health_insurance_data, general_insurance_data, bonds_data, nps_data))
    
    return render(request, 'mis/query_management.html', {'all_data': all_data})


def mutual_funds_page(request):
    # Your view logic here
    return render(request, 'mis/mutual_funds_page.html')

def add_mutual_funds(request):
    if request.method == 'POST':
        # Get data from the form
        investor_name = request.POST.get('investor_name')
        pan_no = request.POST.get('pan_no')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        category = request.POST.get('category')
        scheme_name = request.POST.get('scheme_name')
        nominee_name = request.POST.get('nominee_name')
        amount = request.POST.get('amount')
        product_type = request.POST.get('product_type', 'Mutual Funds')

        # Generate a unique query_id
        prefix = 'APKQ_'
        unique_id = randint(1, 9999)
        query_id = f'{prefix}{unique_id}'

        # Create a new MutualFund object and save it to the database
        mutual_fund = MutualFund(
            query_id=query_id,
            product_type=product_type,
            investor_name=investor_name,
            pan_no=pan_no,
            date_of_birth=date_of_birth,
            email=email,
            mobile=mobile,
            category=category,
            scheme_name=scheme_name,
            nominee_name=nominee_name,
            amount=amount
        )
        mutual_fund.save()

        return redirect('query_management')

    return render(request, 'add_query.html')


def generate_unique_query_id(prefix='APKQ_'):
    unique_id = randint(1, 9999)
    return f'{prefix}{unique_id}'

def add_fixed_deposit(request):
    if request.method == 'POST':
        # Retrieve data from the form
        investor_name = request.POST.get('investor_name')
        investor_pan = request.POST.get('investor_pan')
        investor_dob = request.POST.get('investor_dob')
        investor_email = request.POST.get('investor_email')
        investor_mobile = request.POST.get('investor_mobile')
        company_name = request.POST.get('company_name')
        roi = request.POST.get('roi')
        tenure_type = request.POST.get('tenure_type')
        tenure_duration = request.POST.get('tenure_duration')
        nominee_name = request.POST.get('nominee_name')
        amount = request.POST.get('amount')
        product_type = request.POST.get('product_type', 'Fixed Deposit')

        # Generate a unique query_id
        query_id = generate_unique_query_id()

        # Save data to the database
        fixed_deposit = FixedDeposit(
            query_id=query_id,
            investor_name=investor_name,
            investor_pan=investor_pan,
            investor_dob=investor_dob,
            investor_email=investor_email,
            investor_mobile=investor_mobile,
            company_name=company_name,
            roi=roi,
            tenure_type=tenure_type,
            tenure_duration=tenure_duration,
            nominee_name=nominee_name,
            amount=amount,
            product_type=product_type,
        )
        fixed_deposit.save()

        return redirect('query_management')  # Redirect to a success page or any other URL

    return render(request, 'mis/add_fixed_deposit.html')


def add_life_insurance(request):
    if request.method == 'POST':
        # Retrieve data from the form
        proposer_name = request.POST.get('proposer_name')
        proposer_dob = request.POST.get('proposer_dob')
        proposer_pan = request.POST.get('proposer_pan')
        life_assured_name = request.POST.get('life_assured_name')
        life_assured_dob = request.POST.get('life_assured_dob')
        life_assured_pan = request.POST.get('life_assured_pan')
        life_assured_aadhar_no = request.POST.get('life_assured_aadhar_no')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        company_name = request.POST.get('company_name')
        plan_name = request.POST.get('plan_name')
        ppt = request.POST.get('ppt')
        pt = request.POST.get('pt')
        nominee_name = request.POST.get('nominee_name')
        amount = request.POST.get('amount')
        premium_frequency = request.POST.get('premium_frequency')
        product_type = request.POST.get('product_type', 'Life Insurance')

        # Generate a unique query_id
        query_id = generate_unique_query_id()

        # Create a new LifeInsurance object and save it to the database
        life_insurance = LifeInsurance(
            query_id=query_id,
            proposer_name=proposer_name,
            proposer_dob=proposer_dob,
            proposer_pan=proposer_pan,
            life_assured_name=life_assured_name,
            life_assured_dob=life_assured_dob,
            life_assured_pan=life_assured_pan,
            life_assured_aadhar_no=life_assured_aadhar_no,
            email=email,
            mobile_no=mobile_no,
            company_name=company_name,
            plan_name=plan_name,
            ppt=ppt,
            pt=pt,
            nominee_name=nominee_name,
            amount=amount,
            premium_frequency=premium_frequency,
            product_type=product_type,
        )
        life_insurance.save()

        return redirect('query_management')  # Redirect to a success page or any other URL

    return render(request, 'mis/add_life_insurance.html')


def add_health_insurance(request):
    if request.method == 'POST':
        # Retrieve data from the form
        policy_holder_name = request.POST.get('policy_holder_name')
        proposer_dob = request.POST.get('proposer_dob')
        proposer_pan = request.POST.get('proposer_pan')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        company_name = request.POST.get('company_name')
        plan = request.POST.get('plan')
        frequency = request.POST.get('frequency')
        nominee_name = request.POST.get('nominee_name')
        amount = request.POST.get('amount')
        product_type = request.POST.get('product_type', 'Health Insurance')

        # Generate a unique query_id
        query_id = generate_unique_query_id()

        # Create a new HealthInsurance object and save it to the database
        health_insurance = HealthInsurance(
            query_id=query_id,
            policy_holder_name=policy_holder_name,
            proposer_dob=proposer_dob,
            proposer_pan=proposer_pan,
            email=email,
            mobile=mobile,
            company_name=company_name,
            plan=plan,
            frequency=frequency,
            nominee_name=nominee_name,
            amount=amount,
            product_type=product_type,
        )
        health_insurance.save()

        return redirect('query_management')

    return render(request, 'mis/add_health_insurance.html')


def add_general_insurance(request):
    if request.method == 'POST':
        # Retrieve data from the form
        investor_name = request.POST.get('investor_name')
        pan_number = request.POST.get('pan_number')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        category = request.POST.get('category')
        company_name = request.POST.get('company_name')
        frequency = request.POST.get('frequency')
        nominee = request.POST.get('nominee')
        amount = request.POST.get('amount')
        product_type = request.POST.get('product_type', 'General Insurance')

        # Create a new GeneralInsurance object
        general_insurance = GeneralInsurance(
            investor_name=investor_name,
            pan_number=pan_number,
            date_of_birth=date_of_birth,
            email=email,
            mobile=mobile,
            category=category,
            company_name=company_name,
            frequency=frequency,
            nominee=nominee,
            amount=amount,
            product_type=product_type,
        )
        general_insurance.save()

        return redirect('query_management')  # Redirect to a success page or any other URL

    return render(request, 'mis/add_general_insurance.html')


def add_bonds(request):
    if request.method == 'POST':
        # Retrieve data from the form
        investor_name = request.POST.get('investor_name')
        pan_number = request.POST.get('pan_number')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        company_name = request.POST.get('company_name')
        scheme_name = request.POST.get('scheme_name')
        nominee_name = request.POST.get('nominee_name')
        roi = request.POST.get('roi')
        frequency = request.POST.get('frequency')
        amount = request.POST.get('amount')
        product_type = request.POST.get('product_type', 'Bonds')

        # Generate a unique query_id
        query_id = generate_unique_query_id()

        # Create a new Bonds object and save it to the database
        bonds = Bonds(
            query_id=query_id,
            investor_name=investor_name,
            pan_number=pan_number,
            date_of_birth=date_of_birth,
            email=email,
            mobile=mobile,
            company_name=company_name,
            scheme_name=scheme_name,
            nominee_name=nominee_name,
            roi=roi,
            frequency=frequency,
            amount=amount,
            product_type=product_type,
        )
        bonds.save()

        return redirect('query_management')  # Redirect to a success page or any other URL

    return render(request, 'mis/add_bond.html')


def add_nps(request):
    if request.method == 'POST':
        investor_name = request.POST.get('investor_name')
        pan_number = request.POST.get('pan_number')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        asp_name = request.POST.get('asp_name')
        nominee_name = request.POST.get('nominee_name')
        amount = request.POST.get('amount')
        product_type = request.POST.get('product_type', 'NPS')

        query_id = generate_unique_query_id()
        # Create a new NPS object and save it to the database
        nps = NPS(
            investor_name=investor_name,
            pan_number=pan_number,
            date_of_birth=date_of_birth,
            email=email,
            mobile=mobile,
            asp_name=asp_name,
            nominee_name=nominee_name,
            amount=amount,
            query_id=query_id,
            product_type=product_type
        )
        nps.save()

        selected_companies = request.POST.getlist('insurance_companies')

        # Add the selected insurance companies to the NPS object
        for company_name in selected_companies:
            company, created = InsuranceCompany.objects.get_or_create(name=company_name)
            nps.insurance_companies.add(company)

        return redirect('query_management')  

    return render(request, 'mis/add_nps.html')

def view_query_management(request):
    return render(request, 'mis/view_query_management.html')

def edit_query_management(request):
    return render(request, 'mis/edit_query_management.html')


def business_mis(request):
    return render(request, 'mis/business_mis.html')

# MIS Reports
def mis_employee_report(request):
    employees = Employee.objects.all()

    # Fetch EmployeeSalary records for each employee
    employee_salaries = EmployeeSalary.objects.filter(employee_ref__in=employees).values('employee_ref', 'n_pay')
    
    return render(request, 'mis/mis_employee_report.html', {'employees': employees, 'employee_salaries': employee_salaries})

def view_mis_employee_report(request):
    return render(request, 'mis/view_mis_employee_report.html')

def mis_attendance_report(request):
    attendances = Attendance.objects.all()
    return render(request, 'mis/mis_attendance_report.html', {'attendances': attendances})

def mis_business_report(request):
    return render(request, 'mis/mis_business_report.html')

def mis_dailysalestask_report(request):
    return render(request, 'mis/mis_dailysalestask_report.html')

def mis_dailysales_product_report(request):
    return render(request, 'mis/mis_dailysales_product_report.html')

# HR Module
# ======================================================================================================================
#employee_creation Page
#_____________________________________________________________________

from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.db.models import Q
from datetime import datetime

def employee_creation(request):
    employees = Employee.objects.all()
    companies = Company.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    roles = Role.objects.all()

    # Define the number of items to display per page
    items_per_page = 10  # You can change this to your desired number

    # Create a Paginator instance for each queryset
    employee_paginator = Paginator(employees, items_per_page)
    company_paginator = Paginator(companies, items_per_page)
    department_paginator = Paginator(departments, items_per_page)
    designation_paginator = Paginator(designations, items_per_page)
    role_paginator = Paginator(roles, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page objects for each queryset based on the page number
    employees = employee_paginator.get_page(page_number)
    companies = company_paginator.get_page(page_number)
    departments = department_paginator.get_page(page_number)
    designations = designation_paginator.get_page(page_number)
    roles = role_paginator.get_page(page_number)

    if request.method == "POST":
        print(request.POST)

        post_data = request.POST

        # Start with an empty filter condition
        filter_condition = Q()

        if 'company' in post_data:
            company = request.POST['company']
            filter_condition &= Q(company=company)

        if 'department' in post_data:
            department = request.POST['department']
            filter_condition &= Q(department=department)

        if 'designation' in post_data:
            designation = request.POST['designation']
            filter_condition &= Q(designation=designation)

        if 'officeShift' in post_data:
            office_shift = request.POST['officeShift']
            filter_condition &= Q(office_shift=office_shift)

        # Apply the filter condition to the employees queryset
        employees = Employee.objects.filter(filter_condition)


        if 'editEmployeeId' in  post_data:
            
            editEmployeeId = request.POST['editEmployeeId']
            
            employee = get_object_or_404(Employee , id= editEmployeeId)

            
            employee.full_name = request.POST.get('full_name')
            employee.email = request.POST.get('email')
            employee.phone = request.POST.get('phone')
            employee.dob = request.POST.get('dob')
            employee.gender = request.POST.get('gender')
            employee.company_id = request.POST.get('company')
            employee.department_id = request.POST.get('department')
            employee.designation_id = request.POST.get('desigination')
            employee.office_shift = request.POST.get('office_shift')
            employee.role_id = request.POST.get('role')
            employee.user_name = request.POST.get('user_name')
            employee.attendance_type = request.POST.get('attendance_type')
            date_of_joining = request.POST.get('date_of_joining')
            if date_of_joining:
                employee.joining_date = date_of_joining
            
            if 'user_image' in request.FILES:
                employee.user_image = request.FILES['user_image']

            employee.save()
        return redirect('employee_creation')

    return render(request, 'hr/employee_creation.html', {
        'employees': employees,
        'companies': companies,
        'departments': departments,
        'designations': designations,
        'roles': roles
    })



def add_employee(request):
    if request.method == 'POST':
        # Get the submitted data from the request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        company_id = request.POST.get('company')
        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')
        office_shift = request.POST.get('officeShift')
        role_id = request.POST.get('role')
        user_name = request.POST.get('userName')
        attendance_type = request.POST.get('attendanceType')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')  # Add this line

        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'your_template.html')

        joining_date = request.POST.get('joiningDate')

        # Handle the file upload
        user_image = request.FILES['userImage']

        # Ensure user_image is not empty before saving
        if user_image:
            # Create an Employee object and save it to the database
            employee = Employee(
                full_name=full_name,
                email=email,
                phone=phone,
                dob=dob,
                gender=gender,
                company_id=company_id,
                department_id=department_id,
                designation_id=designation_id,
                office_shift=office_shift,
                role_id=role_id,
                user_name=user_name,
                attendance_type=attendance_type,
                password=password,
                joining_date=joining_date,
                user_image=user_image,
            )
            employee.save()

            messages.success(request, 'Employee added successfully!')
            return JsonResponse({'success': True})  # Redirect to a success page or another page

        else:
            # Handle the case where no image was provided
            messages.error(request, 'Please upload an image for the employee.')

    # Render the template with an empty form
    return render(request, 'employee_creation')


from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_employee_data(request, employee_id):
    if request.method == 'GET':
        try:
            employee = Employee.objects.get(id=employee_id)
            data = {
                "id":employee.id, 
                "full_name": employee.full_name,
                "email": employee.email,
                "phone": employee.phone,
                "dob": str(employee.dob),
                "gender": employee.gender,
                "company": employee.company.id if employee.company else '',  # Use ID here
                "department": employee.department.id if employee.department else '',  # Use ID here
                "designation": employee.designation.id if employee.designation else '',  # Use ID here
                "office_shift": employee.office_shift,
                "user_name": employee.user_name,
                "role": employee.role.id if employee.role else '',  # Use ID here
                "attendance_type": employee.attendance_type,
                "date_of_joining": str(employee.joining_date),
                "user_image": employee.user_image.url if employee.user_image else ''
            }
            return JsonResponse(data)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully.'})
    else:
        return JsonResponse({'message': 'Method not allowed.'}, status=405)

def salary(request):
    employees = Employee.objects.all()
    return render(request, 'hr/add_salary.html', {'employees': employees})


def add_salary(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        employee_id = request.POST.get('employeeIdSelect')
        selected_employee = Employee.objects.get(id=employee_id)
        selected_employee_name = selected_employee.full_name
        month = request.POST.get('month')
        basic = request.POST.get('basic')
        hra = request.POST.get('hra')
        others = request.POST.get('others')
        conv = request.POST.get('conv')
        m_epf = request.POST.get('m_epf')
        m_esi = request.POST.get('m_esi')
        lta = request.POST.get('lta')
        medical = request.POST.get('medical')
        r_allow = request.POST.get('r_allow')
        status = request.POST.get('status')
        wages_type = request.POST.get('wagesType')
        billable_type = request.POST.get('billableType')
        bonus = request.POST.get('bonus')
        leave_encash = request.POST.get('leaveEncash')
        epf = request.POST.get('epf')
        esi = request.POST.get('esi')
        epf_pension = request.POST.get('epfPension')
        tds = request.POST.get('tds')
        hr_deduction = request.POST.get('hr_deduction')
        

        # Perform calculations
        gross_salary = float(basic or 0) + float(hra or 0) + float(others or 0) + float(conv or 0) + float(lta or 0) + float(medical or 0) + float(r_allow or 0)
        employee_epf = float(basic or 0) * 0.12
        employee_esi = gross_salary * 0.0075
        employer_epf = float(basic or 0) * 0.13
        employer_esi = gross_salary * 0.0325
        net_pay = gross_salary - (employee_epf + employee_esi)
        ctc = gross_salary + employee_epf + employee_esi + employer_epf + employer_esi

        # Save the data to the database
        salary = EmployeeSalary(
            employee_id=employee_id,
            employee_ref=selected_employee,
            month=month,
            basic=basic,
            hra=hra,
            others=others,
            conv=conv,
            m_epf=m_epf,
            m_esi=m_esi,
            lta=lta,
            medical=medical,
            r_allow=r_allow,
            status=status,
            wages_type=wages_type,
            billable_type=billable_type,
            bonus=bonus,
            leave_encash=leave_encash,
            epf=epf,
            esi=esi,
            epf_pension=epf_pension,
            tds=tds,
            hr_deduction=hr_deduction,
            g_salary=gross_salary,
            n_pay=net_pay,
            ctc=ctc,
            e_epf=employee_epf,
            e_esi=employee_esi,
            er_epf=employer_epf,
            er_esi=employer_esi
            
            # Include other fields and their values as needed
        )
        salary.save()

        # Redirect to a success page after saving
        return redirect('view_salary')  # Redirect to a success page

    return render(request, 'hr/add_salary.html', {'employees': employees})

def view_salary(request):
    salaries = EmployeeSalary.objects.all()

    # Define the number of items to display per page
    items_per_page = 10  # You can adjust this number as needed

    # Create a Paginator object for the salaries
    paginator = Paginator(salaries, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    salaries = paginator.get_page(page_number)

    return render(request, 'hr/view_salary.html', {'salaries': salaries})

def edit_salary(request, salary_id):
    try:
        salary = EmployeeSalary.objects.get(id=salary_id)
        # Perform actions related to editing salary
        return render(request, 'hr/edit_salary.html', {'salary': salary})
    except EmployeeSalary.DoesNotExist:
        # Handle the case where the salary with the provided ID doesn't exist
        return render(request, 'error.html', {'error_message': 'Salary not found'})

def update_salary(request, salary_id): 
    salary = get_object_or_404(EmployeeSalary, id=salary_id)

    if request.method == 'POST':
        employee_id = request.POST.get('employeeIdSelect')
        employee_name = request.POST.get('employeeNameSelect')
        month = request.POST.get('month')
        if employee_name:
            salary.employee_ref.full_name = employee_name  # Update the Employee Name
            salary.employee_ref.save()
        if month:
            salary.month = month
        # Update salary details from the form data
        salary.basic = request.POST.get('basic')
        salary.hra = request.POST.get('hra')
        salary.others = request.POST.get('others')
        salary.conv = request.POST.get('conv')
        salary.m_epf = request.POST.get('m_epf')
        salary.m_esi = request.POST.get('m_esi')
        # Update other salary fields in a similar manner

        # Newly added fields
        salary.employee_epf = request.POST.get('e_EPF')
        salary.employee_esi = request.POST.get('e_ESI')
        salary.employer_epf = request.POST.get('er_EPF')
        salary.employer_esi = request.POST.get('er_ESI')
        salary.lta = request.POST.get('lta')
        salary.medical = request.POST.get('medical')
        salary.r_allow = request.POST.get('r_allow')
        salary.gross_salary = request.POST.get('g_salary')
        salary.net_pay = request.POST.get('n_pay')
        salary.ctc = request.POST.get('ctc')

        salary.status = request.POST.get('status')
        salary.wages_type = request.POST.get('wagesType')
        salary.billable_type = request.POST.get('billableType')
        salary.bonus = request.POST.get('bonus')
        # Update other fields in a similar manner

        salary.leave_encash = request.POST.get('leaveEncash')
        salary.epf = request.POST.get('epf')
        salary.esi = request.POST.get('esi')
        salary.epf_pension = request.POST.get('epfPension')
        salary.tds = request.POST.get('tds')
        salary.hr_deduction = request.POST.get('hr_deduction')

        # Save the changes
        salary.save()

        # Redirect to a success URL or the salary detail page
        return redirect('view_salary')  # Redirect to the salary detail page for the employee

    # If the form is not submitted via POST request, render the edit salary form
    return render(request, 'hr/edit_salary.html', {'salary': salary})

def delete_salary(request, salary_id):
    salary = get_object_or_404(EmployeeSalary, pk=salary_id)
    salary.delete()
    return redirect('view_salary')


# user management
# ===============

def user_creation(request):
    admin_users = AdminUser.objects.all()  # Fetch all user creation data
    items_per_page = 10  # You can adjust this number as needed

    # Create a Paginator object for the admin users
    admin_user_paginator = Paginator(admin_users, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    admin_users = admin_user_paginator.get_page(page_number)
    return render(request, 'hr/user_creation.html', {'admin_users': admin_users})

def add_admin_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        active = request.POST.get('active', False)

        if password == confirm_password:
            admin_user = AdminUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone=phone,
                password=password,
                image=image,
                active=active,
                role="admin"
            )
            admin_user.save()
            return redirect('user_creation')
        else:
            return JsonResponse({'message': 'Passwords do not match'})

    return render(request, 'user_creation')



def user_list(request):
    employees = Employee.objects.all()
    admin_users = AdminUser.objects.all()
    companies = Company.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    roles = Role.objects.all()
    
    if request.method == "POST":
        print(request.POST)
        
        post_data = request.POST
    
        if 'editEmployeeId' in  post_data:
                
                editEmployeeId = request.POST['editEmployeeId']
                
                employee = get_object_or_404(Employee , id= editEmployeeId)

                
                employee.full_name = request.POST.get('full_name')
                employee.email = request.POST.get('email')
                employee.phone = request.POST.get('phone')
                employee.dob = request.POST.get('dob')
                employee.gender = request.POST.get('gender')
                employee.company_id = request.POST.get('company')
                employee.department_id = request.POST.get('department')
                employee.designation_id = request.POST.get('desigination')
                employee.office_shift = request.POST.get('office_shift')
                employee.role_id = request.POST.get('role')
                employee.user_name = request.POST.get('user_name')
                employee.attendance_type = request.POST.get('attendance_type')
                employee.date_of_joining = request.POST['date_of_joining']
                
                if 'user_image' in request.FILES:
                    employee.user_image = request.FILES['user_image']

                employee.save()
        return redirect('user_list')

    return render(request, 'hr/user_list.html', {
        'employees': employees,
        'admin_users': admin_users,
        'companies': companies,
        'departments': departments,
        'designations': designations,
        'roles': roles,
    })


def delete_admin_user(request, user_id):
    if request.method == 'POST':
        try:
            user_to_delete = AdminUser.objects.get(pk=user_id)
            user_to_delete.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except AdminUser.DoesNotExist:
            return JsonResponse({'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'message': 'An error occurred while deleting the user'})
    return JsonResponse({'message': 'Invalid request method'})


def assign_role(request):
    role_names = Role.objects.values_list('name', flat=True)
    items_per_page = 10  # You can adjust this number as needed

    # Create a Paginator object for the roles
    role_paginator = Paginator(role_names, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    roles = role_paginator.get_page(page_number)
    return render(request, 'hr/asign_role.html', {'role_names': role_names})



# Project task management 
# =======================
from django.shortcuts import render, redirect
from apkapp.models import Project

def add_project(request):
    if request.method == 'POST':
        title = request.POST['title']
        client_id = request.POST['client']  # Directly get the client input
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        priority = request.POST['priority']
        status = request.POST.get('status')
        company_id = request.POST['company']  # Directly get the company input
        assigned_employee_id = request.POST['assigned_employee']
        summary = request.POST['summary']

        client = Client.objects.get(pk=client_id)
        company = Company.objects.get(pk=company_id)
        assigned_employee = Employee.objects.get(pk=assigned_employee_id)
        
        project = Project(
            title=title,
            client=client,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            status=status,
            company=company,
            assigned_employee=assigned_employee,
            summary=summary
        )
        project.save()
        return redirect('project')  # Redirect to a project list view

    return render(request, 'hr/project.html')



from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Project

def project(request):
    project_list = Project.objects.all()  # Retrieve all projects from the database
    companies = Company.objects.all()
    employees = Employee.objects.all()
    clients = Client.objects.all()

    # Number of projects to display per page
    items_per_page = 10  # You can adjust this as needed

    paginator = Paginator(project_list, items_per_page)
    page = request.GET.get('page')

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        projects = paginator.page(paginator.num_pages)

    context = {
        'projects': projects,
        'companies': companies,
        'employees': employees,
        'clients': clients
    }
    return render(request, 'hr/project.html', context)


def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    companies = Company.objects.all()  # Fetch all companies
    employees = Employee.objects.all()
    clients = Client.objects.all()

    if request.method == 'POST':
        # Update the project details based on the form data
        project.title = request.POST.get('title')
        project.client = request.POST.get('client')  # Update client as per your model structure
        project.start_date = request.POST.get('start_date')
        project.end_date = request.POST.get('end_date')
        project.priority = request.POST.get('priority')
        project.status = request.POST.get('status')
        project.company = request.POST.get('company')  # Update company as per your model structure
        project.assigned_employee = request.POST.get('assigned_employee')  # Update employee as per your model structure
        project.summary = request.POST.get('summary')
        project.save()
        return redirect('project')  # Redirect to the project list view
    
    context = {
        'project': project,
        'companies': companies,
        'employees': employees,
        'clients': clients
    }

    # If the request is GET, render the edit project form
    return render(request, 'hr/edit_project.html', context)

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    companies = Company.objects.all()  # Retrieve all companies
    employees = Employee.objects.all()  # Retrieve all employees
    clients = Client.objects.all()  # Retrieve all clients

    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        # Retrieve client and assigned_employee using their IDs
        client_id = request.POST.get('client')
        client = get_object_or_404(Client, pk=client_id)
        assigned_employee_id = request.POST.get('assigned_employee')
        assigned_employee = get_object_or_404(Employee, pk=assigned_employee_id)

        summary = request.POST.get('summary')

        # Update the project instance
        project.title = title
        project.start_date = start_date
        project.end_date = end_date
        project.priority = priority
        project.status = status
        project.client = client
        project.assigned_employee = assigned_employee
        project.summary = summary

        # Update the Company field if required
        company_id = request.POST.get('company')
        if company_id:
            company = get_object_or_404(Company, pk=company_id)
            project.company = company

        project.save()
        return redirect('project')  # Redirect to the project list view

    context = {
        'project': project,
        'companies': companies,
        'employees': employees,
        'clients': clients
    }
    return render(request, 'hr/edit_project.html', context)


from django.shortcuts import get_object_or_404, redirect
from .models import Project

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect('project')


from django.shortcuts import render, redirect
from .models import Task, Company, Project  # Import the Project model

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company_id = request.POST.get('company')  # Get the company ID as a string
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        project_id = request.POST.get('project')  # Get the project ID as a string
        estimated_hours = request.POST.get('estimated_hours')
        project_users = request.POST.get('project_users')

        # Convert the company_id and project_id to integers
        company_id = int(company_id)
        project_id = int(project_id)

        # Get the Company and Project instances associated with the selected IDs
        company = Company.objects.get(pk=company_id)
        project = Project.objects.get(pk=project_id)  # Fetch the Project instance

        # Create a new task with the selected Company and Project
        task = Task(
            title=title,
            company=company,  # Assign the Company instance
            start_date=start_date,
            end_date=end_date,
            project=project,  # Assign the Project instance
            estimated_hours=estimated_hours,
            project_users=project_users
        )
        task.save()
        return redirect('task')

    return render(request, 'hr/task.html')


def task(request):
    tasks = Task.objects.all()

    # Define the number of items to display per page
    items_per_page = 10  # You can adjust this number as needed

    # Create a Paginator object for the tasks
    task_paginator = Paginator(tasks, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    tasks = task_paginator.get_page(page_number)

    return render(request, 'hr/task.html', {'tasks': tasks})

from django.http import JsonResponse
from .models import Company, Project

def get_companies(request):
    companies = Company.objects.all()
    data = [{'id': company.id, 'company_name': company.company_name} for company in companies]
    return JsonResponse(data, safe=False)

def get_projects(request):
    projects = Project.objects.all()
    data = [{'id': project.id, 'title': project.title} for project in projects]
    return JsonResponse(data, safe=False)

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    companies = Company.objects.all()
    projects = Project.objects.all() 
    
    if request.method == 'POST':
        # Fetch the task instance, update its fields, and save it to the database
        task.title = request.POST.get('title')
        task.company = request.POST.get('company')
        task.start_date = request.POST.get('start_date')
        task.end_date = request.POST.get('end_date')
        task.project = request.POST.get('project')
        task.estimated_hours = request.POST.get('estimated_hours')
        task.project_users = request.POST.get('project_users')
        task.save()
        
        return redirect('project')  # Redirect to the project or task list view
        
    # If the request is GET, render the edit task form
    return render(request, 'hr/edit_task.html', {'task': task, 'companies': companies, 'projects': projects})

def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        company_id = request.POST.get('company')  # Retrieve the company ID from the form
        company = Company.objects.get(pk=company_id)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        project_id = request.POST.get('project')
        project = Project.objects.get(pk=project_id)
        estimated_hours = request.POST.get('estimated_hours')
        project_users = request.POST.get('project_users')

        task.title = title
        task.company = company
        task.start_date = start_date
        task.end_date = end_date
        task.project = project
        task.estimated_hours = estimated_hours
        task.project_users = project_users

        task.save()

        return redirect('task')  # Redirect to the task list page after successful update

    return render(request, 'edit_task.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task')  # Redirect to the task list page after deletion
    
    return HttpResponse("Invalid request method")



from django.shortcuts import render, redirect
from .models import Client

def add_client(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        password = request.POST.get('password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')

        img = request.FILES.get('img')

        client = Client(
            first_name=first_name,
            last_name=last_name,
            company=company,
            user_name=user_name,
            email=email,
            phone=phone,
            website=website,
            password=password,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            img=img
        )
        client.save()
        return redirect('client')  

    return render(request, 'client.html' )


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Client

def client(request):
    client_list = Client.objects.all()

    per_page = 10

    paginator = Paginator(client_list, per_page)

    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return render(request, 'hr/client.html', {'clients': clients})



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Client

def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        client.first_name = request.POST.get('first_name')
        client.last_name = request.POST.get('last_name')
        client.company = request.POST.get('company')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.website = request.POST.get('website')
        client.address = request.POST.get('address')
        client.city = request.POST.get('city')
        client.state = request.POST.get('state')
        client.zip_code = request.POST.get('zip_code')
        client.country = request.POST.get('country')
        if 'img' in request.FILES:
            client.img = request.FILES['img']
        client.save()
        return redirect('client')

    return render(request, 'hr/edit_client.html', {'client': client})

def update_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, pk=client_id)
        client.first_name = request.POST.get('first_name')
        client.last_name = request.POST.get('last_name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.website = request.POST.get('website')
        client.company = request.POST.get('company')
        client.address = request.POST.get('address')
        client.city = request.POST.get('city')
        client.state = request.POST.get('state')
        client.zip_code = request.POST.get('zip_code')
        client.country = request.POST.get('country')
        
        if request.FILES.get('img'):
            client.img = request.FILES['img']

        client.save()


        return redirect('client')
    else:
        client = get_object_or_404(Client, pk=client_id)
        return render(request, 'hr/edit_client.html', {'client': client})

from django.shortcuts import render, redirect
from apkapp.models import Client  
from django.contrib import messages

def delete_client(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
        client.delete()
        messages.success(request, 'Client deleted successfully.')
    except Client.DoesNotExist:
        messages.error(request, 'Client not found.')
    return redirect('client')


def invoice(request):
    invoices = Invoice.objects.all()
    projects = Project.objects.all()
    tax_types = TaxType.objects.all()
    return render(request, 'hr/invoice.html', {'invoices': invoices, 'projects': projects, 'tax_types': tax_types})

# def add_invoice(request):
#     if request.method == 'POST':
#         last_invoice = Invoice.objects.order_by('-id').first()
#         if last_invoice:
#             last_invoice_number = last_invoice.invoice_number
#             invoice_number = str(int(last_invoice_number) + 1)
#         else:
#             invoice_number = '1000'

#         project_id = request.POST['project_id']
#         invoice_date = request.POST['invoice_date']
#         due_date = request.POST['due_date']

#         project = Project.objects.get(id=project_id)
#         invoice = Invoice.objects.create(invoice_number=invoice_number, project=project, invoice_date=invoice_date, due_date=due_date)

#         items = request.POST.getlist('item')
#         qtys = request.POST.getlist('qty')
#         unit_prices = request.POST.getlist('unitPrice')
#         tax_types = request.POST.getlist('tax_type')
#         tax_rates = request.POST.getlist('taxRate')
#         sub_totals = request.POST.getlist('subTotal')

#         for i in range(len(items)):
#             tax = TaxType.objects.get(id=tax_types[i])
#             InvoiceItem.objects.create(
#                 invoice=invoice,
#                 item=items[i],
#                 quantity=qtys[i],
#                 unit_price=unit_prices[i],
#                 tax_type=tax,
#                 tax_rate=tax_rates[i],
#                 sub_total=sub_totals[i]
#             )

#         discount_type = request.POST['discountType']
#         discount = request.POST['discount']
#         discount_amount = request.POST['discountAmount']
#         grand_total = request.POST['grandTotal']

#         Discount.objects.create(invoice=invoice, discount_type=discount_type, discount=discount, discount_amount=discount_amount)
#         GrandTotal.objects.create(invoice=invoice, grand_total=grand_total)

#         return redirect('invoice')

#     else:
#         last_invoice = Invoice.objects.order_by('-id').first()
#         if last_invoice:
#             last_invoice_number = last_invoice.invoice_number
#             invoice_number = str(int(last_invoice_number) + 1)
#         else:
#             invoice_number = '1000'

#         invoices = Invoice.objects.all()
#         projects = Project.objects.all()
#         tax_types = TaxType.objects.all()
#         return render(request, 'hr/invoice.html', {'invoices': invoices, 'projects': projects, 'tax_types': tax_types, 'invoice_number': invoice_number})


def tax_type(request):
    tax_types = TaxType.objects.all()

    items_per_page = 10 

    paginator = Paginator(tax_types, items_per_page)

    page_number = request.GET.get('page')

    tax_types = paginator.get_page(page_number)

    return render(request, 'hr/tax_type.html', {'tax_types': tax_types})

def add_tax_type(request):
    if request.method == 'POST':
        tax_name = request.POST.get('tax_name')
        tax_rate = request.POST.get('tax_rate')
        description = request.POST.get('description')
        tax_type = request.POST.get('tax_type')

        if tax_name and tax_rate and description and tax_type:
            TaxType.objects.create(
                tax_name=tax_name,
                tax_rate=tax_rate,
                description=description,
                tax_type=tax_type
            )
            return redirect('tax_type') 

    return render(request, 'hr/tax_type.html')

def edit_tax_type(request, tax_id):
    tax_type = get_object_or_404(TaxType, pk=tax_id)
    return render(request, 'hr/edit_taxtype.html', {'tax_type': tax_type})

def update_tax_type(request, tax_id):
    if request.method == 'POST':
        tax_type = get_object_or_404(TaxType, pk=tax_id)
        tax_type.tax_name = request.POST['tax_name']
        tax_type.tax_rate = request.POST['tax_rate']
        tax_type.description = request.POST['description']
        tax_type.tax_type = request.POST['tax_type']
        
        tax_type.save() 

        return redirect('tax_type') 

    return HttpResponse("Invalid request method")

def delete_tax_type(request, tax_id):
    tax_type = get_object_or_404(TaxType, pk=tax_id)

    if request.method == 'POST':
        tax_type.delete()
        return redirect('tax_type') 

    return HttpResponse("Invalid request method")

#organization 
#============
from django.core.paginator import Paginator
from django.shortcuts import render

def company_creation(request):

    companies = Company.objects.all()

    items_per_page = 10 

    paginator = Paginator(companies, items_per_page)

    page_number = request.GET.get('page')

    companies_page = paginator.get_page(page_number)

    return render(request, 'hr/company_creation.html', {'companies': companies_page})


def add_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_type = request.POST.get('company_type')
        trading_name = request.POST.get('trading_name')
        registration_number = request.POST.get('registration_number')
        gst_number = request.POST.get('gst_number')
        date_added = request.POST.get('date_added')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        website = request.POST.get('website')
        location = request.POST.get('location')
        company_logo = request.FILES.get('company_logo')
        

        new_company = Company(
            company_name=company_name,
            company_type=company_type,
            trading_name=trading_name,
            registration_number=registration_number,
            gst_number=gst_number,
            date_added=date_added,
            phone=phone,
            email=email,
            website=website,
            location=location,
            company_logo=request.FILES['company_logo']
            
        )
        new_company.save()

        return redirect('company_creation')
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def edit_company(request, company_id):
    if request.method == 'POST':
        try:
            company = Company.objects.get(pk=company_id)

            company.company_name = request.POST.get('company_name')
            company.company_type = request.POST.get('company_type')
            company.trading_name = request.POST.get('trading_name')
            company.registration_number = request.POST.get('registration_number')
            company.gst_number = request.POST.get('gst_number')
            company.date_added = request.POST.get('date_added')
            company.phone = request.POST.get('phone')
            company.email = request.POST.get('email')
            company.website = request.POST.get('website')
            company.location = request.POST.get('location')
            

            new_company_logo = request.FILES.get('company_logo')
            if new_company_logo:
                company.company_logo = new_company_logo

            company.save()

            return redirect('company_creation')
        except Company.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Company not found with ID {}'.format(company_id)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_company_data(request):
    if request.method == 'GET':
        company_id = request.GET.get('company_id')
        try:
            company = Company.objects.get(pk=company_id)
            data = {
                'company_name': company.company_name,
                'company_type': company.company_type,
                'trading_name': company.trading_name,
                'registration_number': company.registration_number,
                'gst_number': company.gst_number,
                'date_added': company.date_added,
                'phone': company.phone,
                'email': company.email,
                'website': company.website,
                'location': company.location,
                'image_url': company.company_logo.url, 
            }
            return JsonResponse(data)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def delete_company(request, company_id):
    if request.method == 'POST':
        try:

            company = Company.objects.get(id=company_id)
            company.delete()
            return JsonResponse({'message': 'Company deleted successfully.'})
        except Company.DoesNotExist:
            return JsonResponse({'message': 'Company not found.'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed.'}, status=405)

# Department Page___
#___________________________________________________________________________________________


def department_creation(request):
    companies = Company.objects.all()
    departments = Department.objects.all()
    items_per_page = 10 
    department_paginator = Paginator(departments, items_per_page)

    page_number = request.GET.get('page')

    departments = department_paginator.get_page(page_number)

    if request.method == "POST":
        department_name = request.POST.get("department_name")
        department_head = request.POST.get("department_head")
        company_id = request.POST.get("company")

        company = Company.objects.get(id=company_id)
        department = Department(name=department_name, head=department_head, company=company)
        department.save()

        return redirect("department_creation")

    return render(request, "hr/department_creation.html", {"companies": companies, "departments": departments})



def edit_department(request):

    if request.method == "POST":

        department_id = request.POST.get('department_id')
        department_name = request.POST.get("department_name")
        department_head = request.POST.get("department_head")
        company_id = request.POST.get("company_id")

       
        department = get_object_or_404(Department, pk=department_id)
        company = Company.objects.get(id=company_id)

        department.name =  department_name
        department.company =  company
        department.head =  department_head

        department.save()
        

        return redirect("department_creation")


    department_id = request.GET.get('department_id')
    department = get_object_or_404(Department, pk=department_id)

    data = {
        'name': department.name,
        'head': department.head,
        'company_id': department.company.id,
    }
    return JsonResponse(data)

def delete_department(request, department_id):
    if request.method == 'POST':
        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            return JsonResponse({'message': 'Department deleted successfully.'})
        except Department.DoesNotExist:
            return JsonResponse({'message': 'Department does not exist.'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)

# Location Page___
#___________________________________________________________________________________________


def location(request):
    locations = Location.objects.all()
    items_per_page = 10  

    location_paginator = Paginator(locations, items_per_page)

    page_number = request.GET.get('page')

    locations = location_paginator.get_page(page_number)
    return render(request, 'hr/location.html', {'locations': locations})


def add_location(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        location_head = request.POST.get('location_head')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        new_location = Location(
            location=location,
            location_head=location_head,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            country=country,
            zip=zip,
        )
        new_location.save()
        return redirect('location')
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def edit_location(request, location_id):
    if request.method == 'POST':
        try:
            location = Location.objects.get(pk=location_id)

            location.location = request.POST.get('location')
            location.location_head = request.POST.get('location_head')
            location.address_line1 = request.POST.get('address_line1')
            location.address_line2 = request.POST.get('address_line2')
            location.city = request.POST.get('city')
            location.state = request.POST.get('state')
            location.country = request.POST.get('country')
            location.zip = request.POST.get('zip')

            location.save()

            return redirect('location')
        except Location.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Location not found with ID {}'.format(location_id)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_location_data(request):
    if request.method == 'GET':
        location_id = request.GET.get('location_id')
        try:
            location = Location.objects.get(pk=location_id)
            data = {
                'location': location.location,
                'location_head': location.location_head,
                'address_line1': location.address_line1,
                'address_line2': location.address_line2,
                'city': location.city,
                'state': location.state,
                'country': location.country,
                'zip': location.zip,
            }
            return JsonResponse(data)
        except Location.DoesNotExist:
            return JsonResponse({'error': 'Location not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def delete_location(request, location_id):
    if request.method == 'POST':
        try:
            location = Location.objects.get(pk=location_id)
            location.delete()
            return JsonResponse({'success': True})
        except Location.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Location not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Company_policy Page___
#___________________________________________________________________________________________

def company_policy(request):
    policies = CompanyPolicy.objects.all()
    companies = Company.objects.all()
    items_per_page = 10 

    policy_paginator = Paginator(policies, items_per_page)

    page_number = request.GET.get('page')

    policies = policy_paginator.get_page(page_number)
    return render(request, 'hr/company_policy.html', {'policies': policies, 'companies': companies})

def add_policy(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        company_id = request.POST.get('company') 


        company = Company.objects.get(pk=company_id)


        policy = CompanyPolicy(title=title, description=description, company=company)
        policy.save()

        return redirect('company_policy') 

    companies = Company.objects.all()
    return render(request, 'add_policy.html', {'companies': companies})

def edit_policy(request, policy_id):

    policy = get_object_or_404(CompanyPolicy, pk=policy_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        company_id = request.POST.get('company')  

        policy.title = title
        policy.description = description

        company = Company.objects.get(pk=company_id)
        policy.company = company

        policy.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_policy_data(request):
    if request.method == 'GET':
        policy_id = request.GET.get('policy_id')
        try:
            policy = CompanyPolicy.objects.get(pk=policy_id) 
            data = {
                'title': policy.title,
                'description': policy.description,
                'company_id': policy.company.id,  
            }
            return JsonResponse(data)
        except CompanyPolicy.DoesNotExist: 
            return JsonResponse({'error': 'Policy not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def delete_policy(request, policy_id):
    if request.method == 'POST':
        try:
            policy = CompanyPolicy.objects.get(pk=policy_id)
            policy.delete()
            return JsonResponse({'success': True})
        except CompanyPolicy.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Policy not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Desigination Page___
#___________________________________________________________________________________________

def designation_list(request):
    designations = Designation.objects.all()
    companies = Company.objects.all()
    departments = Department.objects.all()
    items_per_page = 10 


    designation_paginator = Paginator(designations, items_per_page)

    page_number = request.GET.get('page')

    
    designations = designation_paginator.get_page(page_number)
    return render(request, 'hr/desigination.html', {'designations': designations, 'companies': companies, 'departments': departments})


def add_designation(request):
    if request.method == 'POST':
        name = request.POST.get('name')  
        company_id = request.POST.get('company')  
        department_id = request.POST.get('department')

        designation = Designation(
            designation_name=name,
            company_type_id=company_id,
            department_id=department_id
        )
        designation.save()

        return redirect('designation_list')

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_designation_data(request, designation_id):
    designation = get_object_or_404(Designation, id=designation_id)

    
    data = {
        'id': designation.id,
        'designation_name': designation.designation_name,
        'company_type': designation.company_type.id,
        'department': designation.department.id
        
    }

    return JsonResponse(data)

def edit_designation(request, designation_id):
    if request.method == 'POST':
       
        designation = Designation.objects.get(pk=designation_id)

       
        designation.designation_name = request.POST.get('designation_name')
        designation.company_type_id = request.POST.get('company_type') 
        designation.department_id = request.POST.get('department')  

        
        designation.save()

        return redirect('designation_list')  

    return render(request, 'edit_designation.html') 

def delete_designation(request, designation_id):
    try:
        designation = Designation.objects.get(pk=designation_id)
        designation.delete()
        return JsonResponse({'success': True, 'message': 'Designation deleted successfully'})
    except Designation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Designation not found'})


#add_role Page
#_____________________________________________________________________

def role(request):
    roles = Role.objects.all()
    items_per_page = 10  
    role_paginator = Paginator(roles, items_per_page)
    page_number = request.GET.get('page')
    roles = role_paginator.get_page(page_number)
    return render(request, 'hr/add_role.html', {'roles': roles})
    
def add_role(request):
    if request.method == "POST":
        name = request.POST.get('role_name')
        description = request.POST.get('role_description')
        active = request.POST.get('role_active') == 'Active'
        role = Role.objects.create(name=name, description=description, active=active)
       
        return redirect('role')  

    return render(request, 'hr/add_role.html')

def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status') 

       
        role.name = name
        role.description = description
        role.active = status == 'Activate'  

        role.save()  

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_role_data(request):
    if request.method == 'GET':
        role_id = request.GET.get('role_id')
        try:
            role = Role.objects.get(pk=role_id)  
            data = {
                "id": role.id,
                'name': role.name,
                'description': role.description,
                'status': 'Activate' if role.active else 'Deactivate',
                
            }
            return JsonResponse(data)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def delete_role(request, role_id):
    if request.method == 'POST':
        try:
           
            role = Role.objects.get(id=role_id)
            role.delete()
            return JsonResponse({'message': 'Role deleted successfully.'})
        except Role.DoesNotExist:
            return JsonResponse({'message': 'Role not found.'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed.'}, status=405)


#training Page
#_____________________________________________________________________

def training_list(request):
    companies = Company.objects.all()
    employees = Employee.objects.all()
    trainings = Training.objects.all()
    items_per_page = 10  

    
    training_paginator = Paginator(trainings, items_per_page)

    
    page_number = request.GET.get('page')

    
    trainings = training_paginator.get_page(page_number)
    return render(request, 'hr/training.html', {'companies': companies, 'employees': employees, 'trainings': trainings})


def add_training(request):
    if request.method == 'POST':
        company_id = request.POST.get('company', None)
        employee_id = request.POST.get('employee', None) 
        training_type = request.POST['training_type']
        trainer = request.POST['trainer']
        duration = request.POST['duration']
        cost = request.POST['cost']

       
        if company_id is not None:
            
            company = Company.objects.get(pk=company_id)
        else:
           
            company = None

        
        if employee_id is not None:
           
            employee = Employee.objects.get(pk=employee_id)
        else:
            
            employee = None

        
        training = Training(
            company=company,
            employee=employee,
            training_type=training_type,
            trainer=trainer,
            duration=duration,
            cost=cost
        )
        training.save()

        return redirect('training_list') 

    
    employees = Employee.objects.all()
    
    return render(request, 'hr/add_training.html', {'employees': employees}) 


def edit_training(request, training_id):
    if request.method == 'POST':
        try:
            training = Training.objects.get(pk=training_id)

            
            training.training_type = request.POST.get('training_type')
            training.trainer = request.POST.get('trainer')
            training.duration = request.POST.get('duration')
            training.cost = request.POST.get('cost')

           
            employee_id = request.POST.get('employee')
            employee = get_object_or_404(Employee, pk=employee_id)
            training.employee = employee

           
            company_id = request.POST.get('company')
            company = get_object_or_404(Company, pk=company_id)
            training.company = company

            training.save()

            return redirect('training_list')  
        except Training.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Training not found with ID {}'.format(training_id)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_training_data(request, training_id):
    try:
        training = Training.objects.get(pk=training_id)

        
        data = {
            'training_type': training.training_type,
            'trainer': training.trainer,
            'duration': training.duration,
            'cost': training.cost,
            'company_id': training.company.id,  
            'company_name': training.company.company_name,  
            'employee_id': training.employee.id, 
            'employee_name': training.employee.full_name,
        }
        return JsonResponse(data)
    except Training.DoesNotExist:
        return JsonResponse({'error': 'Training not found'}, status=404)


def delete_training(request, training_id):
    if request.method == 'POST':
        training = get_object_or_404(Training, pk=training_id)
        training.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def branch_creation(request):
    branches = Branch.objects.all()

   
    items_per_page = 10 

    
    paginator = Paginator(branches, items_per_page)

    
    page_number = request.GET.get('page')

    
    branches = paginator.get_page(page_number)

    return render(request, 'hr/branch_creation.html', {'branches': branches})

def add_branch(request):
    if request.method == 'POST':
        branch_id = request.POST.get('branch_id')
        branch_name = request.POST.get('branch_name')
        district = request.POST.get('district')
        pin_code = request.POST.get('pin_code')
        location = request.POST.get('location')

        
        new_branch = Branch(branch_id=branch_id, branch_name=branch_name, district=district, pin_code=pin_code, location=location)
        new_branch.save()

        
        return redirect('branch_creation') 

    return render(request, 'hr/branch_creation.html')

def edit_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    return render(request, 'hr/edit_branch.html', {'branch': branch})

def update_branch(request, branch_id):
    if request.method == 'POST':
        branch = get_object_or_404(Branch, id=branch_id)

        branch.branch_id = request.POST.get('branch_id')
        branch.branch_name = request.POST.get('branch_name')
        branch.district = request.POST.get('district')
        branch.pin_code = request.POST.get('pin_code')
        branch.location = request.POST.get('location')

        branch.save()

        return redirect('branch_creation')
    else:
        return HttpResponse('Invalid request method.')

def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    branch.delete()
    return redirect('branch_creation')

# time sheets 
# ===========
from django.shortcuts import render, redirect
from .models import Attendance, Employee, Company

def add_attendance(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        company_id = request.POST.get('company')
        date = request.POST.get('date')
        status = request.POST.get('status')
        clock_in = request.POST.get('clock_in')
        clock_out = request.POST.get('clock_out')
        
        Attendance.objects.create(
            employee_id=employee_id,
            company_id=company_id,
            date=date,
            status=status,
            clock_in=clock_in,
            clock_out=clock_out,
        )
        
        return redirect('hr_attendance_list')
    
    
    employees = Employee.objects.all()
    companies = Company.objects.all()
    
    return render(request, 'hr/add_attendance.html', {'employees': employees, 'companies': companies})

def hr_attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'hr/attendance_list.html', {'attendances': attendances})


from django.shortcuts import redirect
from .models import Attendance

def delete_attendance(request, attendance_id):
    if request.method == 'POST':
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            attendance.delete()
        except Attendance.DoesNotExist:
            pass
    return redirect('hr_attendance_list')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance, Employee, Company

def update_attendance(request, attendance_id):
   
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        
        employee_id = request.POST.get('employee')
        company_id = request.POST.get('company')
        date = request.POST.get('date')
        status = request.POST.get('status')
        clock_in = request.POST.get('clock_in')
        clock_out = request.POST.get('clock_out')

        
        attendance.employee_id = employee_id
        attendance.company_id = company_id
        attendance.date = date
        attendance.status = status
        attendance.clock_in = clock_in
        attendance.clock_out = clock_out

        
        attendance.save()

        return redirect('hr_attendance_list')

   
    employees = Employee.objects.all()
    companies = Company.objects.all()

    return render(request, 'hr/update_attendance.html', {'attendance': attendance, 'employees': employees, 'companies': companies})



def attendance(request):
    return render(request, 'hr/attendance.html')

from django.db.models import Q
from datetime import datetime
from .models import Company, Employee, Attendance

def day_wise_attendance(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    company_id = request.GET.get('company')
    employee_id = request.GET.get('employee')

    attendances = Attendance.objects.all()

    
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        attendances = attendances.filter(date__lte=end_date)
    if company_id:
        attendances = attendances.filter(company_id=company_id)
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)

    companies = Company.objects.all()
    employees = Employee.objects.all()

    return render(request, 'hr/day_wise_attendance.html', {'attendances': attendances, 'companies': companies, 'employees': employees})

def timesheet_update_attendance(request):
    search_criteria = request.GET.get('search')
    
    
    if search_criteria:
        attendances = Attendance.objects.filter(
            Q(employee__full_name__icontains=search_criteria) |
            Q(company__company_name__icontains=search_criteria) |
            Q(date__icontains=search_criteria) |
            Q(status__icontains=search_criteria)
        )
    else:
        attendances = Attendance.objects.all()

    return render(request, 'hr/timesheet_update_attendance.html', {'attendances': attendances})


def manage_holiday(request):
    return render(request, 'hr/manage_holiday.html')

from django.shortcuts import render, redirect
from .models import Holiday

def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'hr/holiday_list.html', {'holidays': holidays})

def holiday_create(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        company_id = request.POST['company']
        title = request.POST['title']
        start_date = request.POST['start_date']
        finish_date = request.POST['finish_date']

        Holiday.objects.create(company_id=company_id, title=title, start_date=start_date, finish_date=finish_date)
        return redirect('holiday_list')

    return render(request, 'hr/holiday_form.html', {'companies': companies})

from .models import Holiday, Company
from django.shortcuts import render, get_object_or_404, redirect

def holiday_update(request, holiday_id):
    holiday = get_object_or_404(Holiday, pk=holiday_id)
    companies = Company.objects.all()

    if request.method == 'POST':
        holiday.title = request.POST['title']
        holiday.start_date = request.POST['start_date']
        holiday.finish_date = request.POST['finish_date']
        
       
        company_id = request.POST['company']
        holiday.company_id = company_id
        
        holiday.save()
        return redirect('holiday_list')

    context = {
        'holiday': holiday,
        'companies': companies,
    }
    
    return render(request, 'hr/holiday_update.html', context)



from django.shortcuts import get_object_or_404, render, redirect
from .models import Holiday

def holiday_delete(request, holiday_id):
    holiday = get_object_or_404(Holiday, pk=holiday_id)
    
    if request.method == 'POST':
        holiday.delete()
        return redirect('holiday_list')
    
    context = {
        'holiday': holiday,
    }
    
    return render(request, 'hr/holiday_confirm_delete.html', context)

def manage_leave(request):
    return render(request, 'hr/manage_leave.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveType

def leave_type_list(request):
    leave_types = LeaveType.objects.all()
    context = {'leave_types': leave_types}
    return render(request, 'hr/leave_type_list.html', context)

from django.shortcuts import render, redirect
from .models import LeaveType

def add_leave_type(request):
    if request.method == 'POST':
        leave_type_name = request.POST.get('leave_type_name')
        year = request.POST.get('year')
        quantity = request.POST.get('quantity')

        LeaveType.objects.create(
            leave_type_name=leave_type_name,
            year=year,
            quantity=quantity
        )

        return redirect('leave_type_list')

    return render(request, 'hr/add_leave_type.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveType

def update_leave_type(request, leave_type_id):
    leave_type = get_object_or_404(LeaveType, id=leave_type_id)

    if request.method == 'POST':
        leave_type.leave_type_name = request.POST.get('leave_type_name')
        leave_type.year = request.POST.get('year')
        leave_type.quantity = request.POST.get('quantity')
        leave_type.save()
        return redirect('leave_type_list')

    context = {'leave_type': leave_type}
    return render(request, 'hr/update_leave_type.html', context)


def delete_leave_type(request, leave_type_id):
    leave_type = get_object_or_404(LeaveType, id=leave_type_id)

    if request.method == 'POST':
        leave_type.delete()
        return redirect('leave_type_list')

    context = {'leave_type': leave_type}
    return render(request, 'hr/delete_leave_type.html', context)

from django.shortcuts import render, redirect
from .models import LeaveRequest

def leave_request_list(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'hr/leave_request_list.html', {'leave_requests': leave_requests})

from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest, Company, Department, Employee, LeaveType

def leave_request_create(request):
    if request.method == 'POST':
        company_id = request.POST.get('company')
        department_id = request.POST.get('department')
        employee_id = request.POST.get('employee')
        leave_type_id = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        finish_date = request.POST.get('finish_date')
        status = request.POST.get('status')
        attachment = request.FILES.get('attachment')
        leave_reason = request.POST.get('leave_reason')

        company = get_object_or_404(Company, id=company_id)
        department = get_object_or_404(Department, id=department_id)
        employee = get_object_or_404(Employee, id=employee_id)
        leave_type = get_object_or_404(LeaveType, id=leave_type_id)

        LeaveRequest.objects.create(
            company=company,
            department=department,
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            finish_date=finish_date,
            status=status,
            attachment=attachment,
            leave_reason=leave_reason
        )

        return redirect('leave_request_list')

    companies = Company.objects.all()
    departments = Department.objects.all()
    employees = Employee.objects.all()
    leave_types = LeaveType.objects.all()

    context = {
        'companies': companies,
        'departments': departments,
        'employees': employees,
        'leave_types': leave_types,
    }

    return render(request, 'hr/leave_request_form.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest, Company, Department, Employee, LeaveType

def leave_request_update(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    if request.method == 'POST':
        company_id = request.POST.get('company')
        department_id = request.POST.get('department')
        employee_id = request.POST.get('employee')
        leave_type_id = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        finish_date = request.POST.get('finish_date')
        status = request.POST.get('status')
        attachment = request.FILES.get('attachment')
        leave_reason = request.POST.get('leave_reason')

        
        company = get_object_or_404(Company, id=company_id)
        department = get_object_or_404(Department, id=department_id)
        employee = get_object_or_404(Employee, id=employee_id)
        leave_type = get_object_or_404(LeaveType, id=leave_type_id)

        
        leave_request.company = company
        leave_request.department = department
        leave_request.employee = employee
        leave_request.leave_type = leave_type
        leave_request.start_date = start_date
        leave_request.finish_date = finish_date
        leave_request.status = status
        leave_request.attachment = attachment
        leave_request.leave_reason = leave_reason

        leave_request.save()

        return redirect('leave_request_list')

    companies = Company.objects.all()
    departments = Department.objects.all()
    employees = Employee.objects.all()
    leave_types = LeaveType.objects.all()

    context = {
        'leave_request': leave_request,
        'companies': companies,
        'departments': departments,
        'employees': employees,
        'leave_types': leave_types,
    }

    return render(request, 'hr/leave_request_update.html', context)



def leave_request_delete(request, pk):
    leave_request = LeaveRequest.objects.get(pk=pk)

    if request.method == 'POST':
        leave_request.delete()
        return redirect('leave_request_list')

    return render(request, 'hr/leave_request_confirm_delete.html', {'leave_request': leave_request})

from django.db.models import Q
from datetime import datetime
from .models import Company, Employee, Attendance

def monthly_wise_attendance(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    company_id = request.GET.get('company')
    employee_id = request.GET.get('employee')

    attendances = Attendance.objects.all()

    
    if year:
        attendances = attendances.filter(date__year=year)
    if month:
        attendances = attendances.filter(date__month=month)
    if company_id:
        attendances = attendances.filter(company_id=company_id)
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)

    companies = Company.objects.all()
    employees = Employee.objects.all()

    return render(request, 'hr/monthly_wise_attendance.html', {'attendances': attendances, 'companies': companies, 'employees': employees})


from django.shortcuts import render, get_object_or_404, redirect
from .models import OfficeShift, Company

def create_office_shift(request):
    companies = Company.objects.all()

    if request.method == 'POST':
        shift_name = request.POST['shift_name']
        company_id = request.POST['company']
        monday_in = request.POST['monday_in']
        monday_out = request.POST['monday_out']
        tuesday_in = request.POST['tuesday_in']
        tuesday_out = request.POST['tuesday_out']
        wednesday_in = request.POST['wednesday_in']
        wednesday_out = request.POST['wednesday_out']
        thursday_in = request.POST['thursday_in']
        thursday_out = request.POST['thursday_out']
        friday_in = request.POST['friday_in']
        friday_out = request.POST['friday_out']
        saturday_in = request.POST['saturday_in']
        saturday_out = request.POST['saturday_out']
        sunday_in = request.POST['sunday_in']
        sunday_out = request.POST['sunday_out']
        
        
        company = get_object_or_404(Company, id=company_id)

        OfficeShift.objects.create(
            shift_name=shift_name,
            company=company,
            monday_in=monday_in,
            monday_out=monday_out,
            tuesday_in=tuesday_in,
            tuesday_out=tuesday_out,
            wednesday_in=wednesday_in,
            wednesday_out=wednesday_out,
            thursday_in=thursday_in,
            thursday_out=thursday_out,
            friday_in=friday_in,
            friday_out=friday_out,
            saturday_in=saturday_in,
            saturday_out=saturday_out,
            sunday_in=sunday_in,
            sunday_out=sunday_out,
            
        )

        return redirect('office_shift_list')

    context = {'companies': companies}
    return render(request, 'hr/create_office_shift.html', context)

def office_shift_list(request):
    office_shifts = OfficeShift.objects.all()
    return render(request, 'hr/office_shift_list.html', {'office_shifts': office_shifts})

def update_office_shift(request, shift_id):
    office_shift = get_object_or_404(OfficeShift, id=shift_id)
    companies = Company.objects.all()

    if request.method == 'POST':
        shift_name = request.POST['shift_name']
        company_id = request.POST['company']
        monday_in = request.POST['monday_in']
        monday_out = request.POST['monday_out']
        tuesday_in = request.POST['tuesday_in']
        tuesday_out = request.POST['tuesday_out']
        wednesday_in = request.POST['wednesday_in']
        wednesday_out = request.POST['wednesday_out']
        thursday_in = request.POST['thursday_in']
        thursday_out = request.POST['thursday_out']
        friday_in = request.POST['friday_in']
        friday_out = request.POST['friday_out']
        saturday_in = request.POST['saturday_in']
        saturday_out = request.POST['saturday_out']
        sunday_in = request.POST['sunday_in']
        sunday_out = request.POST['sunday_out']
        
        company = get_object_or_404(Company, id=company_id)

        office_shift.shift_name = shift_name
        office_shift.company = company
        office_shift.monday_in = monday_in
        office_shift.monday_out = monday_out
        office_shift.tuesday_in = tuesday_in
        office_shift.tuesday_out = tuesday_out
        office_shift.wednesday_in=wednesday_in
        office_shift.wednesday_out=wednesday_out
        office_shift.thursday_in=thursday_in
        office_shift.thursday_out=thursday_out
        office_shift.friday_in=friday_in
        office_shift.friday_out=friday_out
        office_shift.saturday_in=saturday_in
        office_shift.saturday_out=saturday_out
        office_shift.sunday_in=sunday_in
        office_shift.sunday_out=sunday_out
        
        office_shift.save()

        return redirect('office_shift_list')

    context = {'office_shift': office_shift, 'companies': companies}
    return render(request, 'hr/update_office_shift.html', context)

def delete_office_shift(request, shift_id):
    office_shift = get_object_or_404(OfficeShift, id=shift_id)

    if request.method == 'POST':
        office_shift.delete()
        return redirect('office_shift_list')

    return render(request, 'hr/delete_office_shift.html', {'office_shift': office_shift})

def office_shift(request):
    return render(request, 'hr/office_shift.html')


# Hr reports
# ========== 
from datetime import datetime, time

def calculate_total_work_hours(clock_in, clock_out):
    if clock_in and clock_out:
        
        time_difference = datetime.combine(datetime.min, clock_out) - datetime.combine(datetime.min, clock_in)

       
        total_hours = time_difference.seconds // 3600
        total_minutes = (time_difference.seconds % 3600) // 60

        return f"{total_hours} hours {total_minutes} minutes"
    else:
        return "N/A"



def attendance_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    company_id = request.GET.get('company')
    employee_id = request.GET.get('employee')

    attendances = Attendance.objects.all()

   
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        attendances = attendances.filter(date__lte=end_date)
    if company_id:
        attendances = attendances.filter(company_id=company_id)
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)

    # Calculate and add total work hours for each attendance entry
    for attendance in attendances:
        attendance.total_work = calculate_total_work_hours(attendance.clock_in, attendance.clock_out)

    companies = Company.objects.all()
    employees = Employee.objects.all()
    return render(request, 'hr/attendance_report.html', {'attendances': attendances, 'companies': companies, 'employees': employees})


def deposite_report(request):
    return render(request, 'hr/deposit_report.html')

def Employees_report(request):
    employees = Employee.objects.all()
    companies = Company.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    return render(request, 'hr/Employees_report.html', {
        'employees': employees,
        'companies': companies,
        'departments': departments,
        'designations': designations,
    })

from datetime import datetime,timedelta
from django.db.models import Q

def expenses_report(request):
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    expenses = Expense.objects.all()

    # Filter by category if it is specified
    if category and category != 'all':
        expenses = expenses.filter(category=category)
        
        # Apply date filtering if both start_date and end_date are provided
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)
            
            # Filter the date range
            expenses = expenses.filter(created_date__gte=start_date_obj, created_date__lt=end_date_obj)

            start_date = start_date_obj.strftime('%Y-%m-%d')
            end_date = (end_date_obj - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        # Show all data when 'For All' is selected
        start_date = ''
        end_date = ''

    context = {
        'expenses': expenses,
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'hr/expenses_report.html', context)

def project_report(request):
    return render(request, 'hr/project_report.html')

def task_report(request):
    tasks = Task.objects.all() 
    status_filter = request.GET.get('status_filter')
    if status_filter and status_filter != 'All':
        tasks = tasks.filter(status=status_filter)
    return render(request, 'hr/task_report.html', {'tasks': tasks})

def training_report(request):
    companies = Company.objects.all()
    employees = Employee.objects.all()
    trainings = Training.objects.all()
    return render(request, 'hr/training_report.html', {'companies': companies, 'employees': employees, 'trainings': trainings})

def transaction_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    company_id = request.GET.get('company')
    employee_id = request.GET.get('employee')

    attendances = Attendance.objects.all()

    # Apply filters if provided
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        attendances = attendances.filter(date__lte=end_date)
    if company_id:
        attendances = attendances.filter(company_id=company_id)
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)

    # Calculate and add total work hours for each attendance entry
    for attendance in attendances:
        attendance.total_work = calculate_total_work_hours(attendance.clock_in, attendance.clock_out)

    companies = Company.objects.all()
    employees = Employee.objects.all()
    return render(request, 'hr/transaction_report.html', {'attendances': attendances, 'companies': companies, 'employees': employees})




# Payroll
# ==================================================================================================================
# ==================================================================================================================

from django.shortcuts import render
from .models import Employee, EmployeeSalary

def employee_list(request):
    # Fetch employees
    employees = Employee.objects.all()

    # Fetch EmployeeSalary records for each employee
    employee_salaries = EmployeeSalary.objects.filter(employee_ref__in=employees).values('employee_ref', 'n_pay')

    return render(request, 'payroll/employee_list.html', {'employees': employees, 'employee_salaries': employee_salaries})

def employee_detail(request, employee_id):
    # Fetch the employee data from the database using the employee_id
    employee = Employee.objects.get(id=employee_id)  # Assuming Employee model has an 'id' field

    context = {
        'employee': employee,
    }
    return render(request, 'payroll/employee_detail.html', context)



from django.shortcuts import render
from .models import Attendance  # Import your Attendance model

def attendance_list(request):
    # Fetch all attendance records from the database
    attendances = Attendance.objects.all()

    return render(request, 'payroll/attendance_list.html', {'attendances': attendances})

def view_attendance(request, employee_id):
    attendances = Attendance.objects.filter(employee_id=employee_id)
    context = {
        'attendances': attendances,
    }
    return render(request, 'payroll/view_attendance.html', context)




def payroll_list(request):
    return render(request, 'payroll/payroll_list.html')

from django.shortcuts import render
from .models import Department  # Import your Department model

def department_list(request):
    # Fetch all department records from the database
    departments = Department.objects.all()

    return render(request, 'payroll/department_list.html', {'departments': departments})

def view_department(request, department_id):
    # Get the specific department based on the ID
    department = Department.objects.get(id=department_id)

    # Render a template to display department details
    return render(request, 'payroll/view_department.html', {'department': department})


from django.shortcuts import render
from .models import Designation  # Import your Designation model

def position_list(request):
    # Fetch all designation records from the database
    designations = Designation.objects.all()

    return render(request, 'payroll/position_list.html', {'designations': designations})

def view_desigination(request, desigination_id):
    designation = get_object_or_404(Designation, id=desigination_id)
    return render(request, 'payroll/view_desigination.html', {'designation': designation})



from django.shortcuts import render, redirect
from .models import Allowance 

def allowance_list(request):
    if request.method == "POST":
        # Check if the request method is POST
        allowance = request.POST.get("allowance")
        description = request.POST.get("description")

        new_allowance = Allowance(allowance=allowance, description=description)
        new_allowance.save()

        return redirect("allowance_list")  # Redirect to the same view after form submission

    # Fetch all existing allowances from the database
    allowances = Allowance.objects.all()

    return render(request, 'payroll/allowance_list.html', {'allowances': allowances})


from django.shortcuts import render, redirect
from .models import Allowance 

def edit_allowance(request, allowance_id):
    if request.method == "POST":
        # Check if the request method is POST
        allowance = Allowance.objects.get(pk=allowance_id)  # Retrieve the allowance by its ID
        allowance.allowance = request.POST.get("allowance")
        allowance.description = request.POST.get("description")
        allowance.save()
        
        return redirect("allowance_list")  # Redirect to the list of allowances after editing

    # If the request method is GET, retrieve the allowance for editing
    allowance = Allowance.objects.get(pk=allowance_id)

    return render(request, 'payroll/edit_allowance.html', {'allowance': allowance})


from django.shortcuts import get_object_or_404

def delete_allowance(request, allowance_id):
    if request.method == "POST":
        allowance = get_object_or_404(Allowance, pk=allowance_id)
        allowance.delete()
        return redirect("allowance_list")




from .models import Deduction
from django.shortcuts import render, redirect

def deduction_list(request):
    if request.method == "POST":
        deduction_name = request.POST.get("deduction_name")
        description = request.POST.get("description")

        Deduction.objects.create(deduction_name=deduction_name, description=description)
        return redirect("deduction_list")

    deductions = Deduction.objects.all()
    return render(request, 'payroll/deduction_list.html', {'deductions': deductions})

from .models import Deduction
from django.shortcuts import render, redirect, get_object_or_404

def update_deduction(request, deduction_id):
    deduction = get_object_or_404(Deduction, pk=deduction_id)

    if request.method == "POST":
        deduction_name = request.POST.get("deduction_name")
        description = request.POST.get("description")

        deduction.deduction_name = deduction_name
        deduction.description = description
        deduction.save()

        return redirect("deduction_list")

    return render(request, 'payroll/update_deduction.html', {'deduction': deduction})

def delete_deduction(request, deduction_id):
    deduction = Deduction.objects.get(pk=deduction_id)
    deduction.delete()
    return redirect("deduction_list")





def new_payment(request):
    return render(request, 'payroll/new_payment.html')

def payment_history(request):
    return render(request, 'payroll/payment_history.html')



# Acounts 
# ===================================================================================================================
# ===================================================================================================================
# master
# ======
from django.shortcuts import render, redirect
from .models import ItemCreation

def add_item(request):
    if request.method == "POST":
        # Get data from the form
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')

        # Create a new item in the database
        item = ItemCreation(product_name=product_name, quantity=quantity)
        item.save()

        return redirect('item_creation')

    return render(request, 'accounts/item_creation.html')

def item_creation(request):
    items = ItemCreation.objects.all()
    return render(request, 'accounts/item_creation.html', {'items': items})

from django.shortcuts import render, redirect, get_object_or_404
from .models import ItemCreation

def update_item(request, item_id):
    item = get_object_or_404(ItemCreation, pk=item_id)

    if request.method == "POST":
        # Get the updated data from the form
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')

        # Update the item in the database
        item.product_name = product_name
        item.quantity = quantity
        item.save()

        return redirect('item_creation')

    return render(request, 'accounts/update_item.html', {'item': item})

from django.shortcuts import render, redirect, get_object_or_404
from .models import ItemCreation

def delete_item(request, item_id):
    item = get_object_or_404(ItemCreation, pk=item_id)
    item.delete()
    return redirect('item_creation')

from django.shortcuts import render, redirect
from .models import Supplier
def add_supplier(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        gstin_number = request.POST.get('gstin_number')
        address = request.POST.get('address')

        Supplier.objects.create(
            company_name=company_name,
            phone_number=phone_number,
            email=email,
            gstin_number=gstin_number,
            address=address
        )
        return redirect('supplier_creation')

    return render(request, 'accounts/supplier_creation.html')

def supplier_creation(request):
    suppliers = Supplier.objects.all()
    return render(request, 'accounts/supplier_creation.html', {'suppliers': suppliers})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier

def update_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        # Get updated data from the request
        company_name = request.POST.get('company_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        gstin_number = request.POST.get('gstin_number')
        address = request.POST.get('address')

        # Update the supplier object
        supplier.company_name = company_name
        supplier.phone_number = phone_number
        supplier.email = email
        supplier.gstin_number = gstin_number
        supplier.address = address

        # Save the changes
        supplier.save()

        # Redirect to the supplier detail page
        return redirect('supplier_creation')

    return render(request, 'accounts/update_supplier.html', {'supplier': supplier})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier

def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.delete()
    return redirect('supplier_creation')





from django.shortcuts import render, redirect
from .models import PurchaseReturn, PurchaseReturnItem
from django.http import JsonResponse

def new_purchase_return(request):
    inventories = ItemCreation.objects.all()

    if request.method == 'POST':
        # Retrieve the form data from the request
        invoice_no = request.POST['invoice_no']
        purchase_date = request.POST['purchase_date']
        supplier_name = request.POST['supplier_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']
        gstin = request.POST['gstin']
        return_date = request.POST['return_date']
        selected_inventories = request.POST.getlist('inventory[]')
        prices = request.POST.getlist('price[]')
        quantities = request.POST.getlist('quantity[]')
        amounts = request.POST.getlist('amount[]')
        gsts = request.POST.getlist('gst[]')
        gstprices = request.POST.getlist('gstprice[]')
        igsts = request.POST.getlist('igst[]')
        igstprices = request.POST.getlist('igstprice[]')
        total_prices = request.POST.getlist('total_price[]')

        # Create a new PurchaseReturn object
        purchase_return = PurchaseReturn.objects.create(
            invoice_no=invoice_no,
            purchase_date=purchase_date,
            supplier_name=supplier_name,
            phone_number=phone_number,
            email=email,
            address=address,
            gstin_no=gstin,
            purchase_return_date=return_date
        )

        # Create PurchaseReturnItem objects for each selected inventory
        for i in range(len(selected_inventories)):
            inventory_id = selected_inventories[i]
            inventory = ItemCreation.objects.get(pk=inventory_id)
            price = prices[i]
            quantity = quantities[i]
            amount = amounts[i]
            gst = gsts[i]
            gstprice = gstprices[i]
            igst = igsts[i]
            igstprice = igstprices[i]
            total_price = total_prices[i]

            # Update the inventory quantity (since it's a return)
            inventory.quantity -= int(quantity)
            inventory.save()

            PurchaseReturnItem.objects.create(
                purchase_return=purchase_return,
                stock=inventory,
                price=price,
                quantity=quantity,
                amount=amount,
                gst=gst,
                gstprice=gstprice,
                igst=igst,
                igstprice=igstprice,
                total_price=total_price
            )

        return redirect('purchase_return_success')

    context = {
        'inventories': inventories
    }
    return render(request, 'accounts/new-purchase-return.html', context)


def purchase_return_success(request):
    return render(request, 'accounts/purchase-return-success.html')


from django.http import JsonResponse
from .models import ItemCreation  # Import the Inventory model

def get_available_quantity(request):
    stock_id = request.GET.get('stock_id')

    # Fetch the inventory object
    try:
        inventory = ItemCreation.objects.get(id=stock_id)
    except ItemCreation.DoesNotExist:
        return JsonResponse({'error': 'Invalid stock ID'})

    # Return the available quantity as JSON response
    return JsonResponse({'available_quantity': inventory.quantity})


from django.shortcuts import render
from .models import PurchaseReturn
from django.core.paginator import Paginator

def purchase_return_list(request):
    # Get all purchase returns
    purchase_returns = PurchaseReturn.objects.all()

    # Set the number of items to display per page
    items_per_page = 10  # You can adjust this number according to your preferences

    # Create a Paginator instance
    paginator = Paginator(purchase_returns, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    purchase_return_page = paginator.get_page(page_number)

    context = {
        'purchase_returns': purchase_return_page
    }

    return render(request, 'accounts/purchase-return-list.html', context)



from django.shortcuts import render, get_object_or_404
from .models import PurchaseReturn, PurchaseReturnItem  # Import the PurchaseReturn and PurchaseReturnItem models

def view_return_bill(request, return_id):
    purchase_return = get_object_or_404(PurchaseReturn, id=return_id)
    purchase_return_items = purchase_return.purchase_return_items.all()

    total_amount = sum(item.amount for item in purchase_return_items)
    total_gst = sum(item.amount * (item.gst / 100) for item in purchase_return_items)
    total_igst = sum(item.amount * (item.igst / 100) for item in purchase_return_items)
    total_price = total_amount + total_gst + total_igst

    context = {
        'purchase_return': purchase_return,
        'purchase_return_items': purchase_return_items,
        'total_amount': total_amount,
        'total_gst': total_gst,
        'total_igst': total_igst,
        'total_price': total_price,
    }

    return render(request, 'accounts/view_return_bill.html', context)


from django.shortcuts import get_object_or_404, redirect
from .models import PurchaseReturn  # Import the PurchaseReturn model

def delete_return(request, return_id):
    purchase_return = get_object_or_404(PurchaseReturn, id=return_id)
    
    # Add any additional logic here
    
    purchase_return.delete()
    
    # Redirect to the purchase return list page or any other appropriate page
    return redirect('purchase_return_list')


# transaction 
# ===========
from django.shortcuts import render, redirect
from .models import Supplier, ItemCreation, Purchase, PurchaseItem

import time
import random

def generate_purchase_id():
    timestamp = int(time.time())  # Get current timestamp
    random_num = random.randint(1000, 9999)  # Generate a random 4-digit number
    purchase_id = f'PUR-{timestamp}-{random_num}'  # Create the purchase ID
    return purchase_id

from decimal import Decimal

def new_purchase(request):
    suppliers = Supplier.objects.all()
    items = ItemCreation.objects.all()

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        stocks = request.POST.getlist('stock[]')
        prices = request.POST.getlist('price[]')
        quantities = request.POST.getlist('quantity[]')
        gsts = request.POST.getlist('gst[]')
        gstprices = request.POST.getlist('gstprice[]')
        igsts = request.POST.getlist('igst[]')
        igstprices = request.POST.getlist('igstprice[]')
        total_prices = request.POST.getlist('total_price[]')
        purchase_dates = request.POST.getlist('purchase_date[]')

        supplier = Supplier.objects.get(id=supplier_id)

        purchase = Purchase.objects.create(
            supplier=supplier,
            purchase_id=generate_purchase_id(),
            total_price=0,
            purchase_date=purchase_dates[0]  # Use the first purchase date from the list
        )

        for i in range(len(stocks)):
            stock_id = stocks[i]
            price = Decimal(prices[i])
            quantity = int(quantities[i])
            gst = Decimal(gsts[i])
            gstprice = Decimal(gstprices[i])
            igst = Decimal(igsts[i])
            igstprice = Decimal(igstprices[i])
            total_price = Decimal(total_prices[i])
            amount = price * quantity

            inventory = ItemCreation.objects.get(id=stock_id)

            purchase_item = PurchaseItem.objects.create(
                purchase=purchase,
                stock=inventory,
                price=price,
                quantity=quantity,
                amount=amount,
                gst=gst,
                gstprice=gstprice,
                igst=igst,
                igstprice=igstprice,
                total_price=total_price
            )

            # Update the product quantity in the inventory
            inventory.quantity += quantity
            inventory.save()

            purchase.total_price += total_price
            purchase.save()

        return redirect('purchase_list')

    context = {
        'suppliers': suppliers,
        'items': items
    }
    return render(request, 'accounts/new-purchase.html', context)




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Purchase

def purchase_list(request):
    purchases = Purchase.objects.select_related('supplier').all()

    # Paginate the purchases list
    paginator = Paginator(purchases, 10)  # Show 10 purchases per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'purchases': page_obj,
    }

    return render(request, 'accounts/purchase_list.html', context)
from django.shortcuts import render
from .models import Purchase

def view_bill(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    
    # Calculate the total amount, total GST, and total IGST
    total_amount = sum(item.amount for item in purchase.purchase_items.all())
    total_gst = sum((item.amount * item.gst / 100) for item in purchase.purchase_items.all())
    total_igst = sum(item.igst for item in purchase.purchase_items.all())
    
    context = {
        'purchase': purchase,
        'total_amount': total_amount,
        'total_gst': total_gst,
        'total_igst': total_igst,
    }
    return render(request, 'accounts/view_bill.html', context)


    
def delete_bill(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    if request.method == 'POST':
        # Perform the deletion
        purchase.delete()
        return redirect('purchase_list')
    
    return render(request, 'accounts/delete_purchase.html', {'purchase': purchase})

def confirm_delete(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    if request.method == 'POST':
        # Delete the purchase
        purchase.delete()
        return redirect('purchase_list')

    context = {'purchase': purchase}
    return render(request, 'accounts/confirm_delete.html', context)


from django.shortcuts import render, redirect
from .models import PaymentVoucher

def create_payment_voucher(request):
    if request.method == 'POST':
        voucher_number = request.POST['voucher_number']
        cash_or_bank = request.POST['cash_or_bank']
        customer_name = request.POST['customer_name']
        date = request.POST['date']
        narration = request.POST['narration']
        particular = request.POST['particular']
        bill_no = request.POST['bill_no']
        amount = request.POST['amount']
        account_no = request.POST['account_no']
        check_no = request.POST['check_no']

        payment_voucher = PaymentVoucher.objects.create(
            voucher_number=voucher_number,
            cash_or_bank=cash_or_bank,
            customer_name=customer_name,
            date=date,
            narration=narration,
            particular=particular,
            bill_no=bill_no,
            amount=amount,
            account_no=account_no,
            check_no=check_no
        )

        return redirect('view_payment_vouchers')
    else:
        return render(request, 'accounts/create_payment_voucher.html')



from django.shortcuts import render, redirect
from .models import PaymentVoucher

def view_payment_vouchers(request):
    vouchers = PaymentVoucher.objects.all()

    if request.method == 'POST' and 'delete_voucher' in request.POST:
        voucher_id = request.POST['voucher_id']
        PaymentVoucher.objects.filter(id=voucher_id).delete()
        return redirect('view_payment_vouchers')

    context = {
        'vouchers': vouchers,
    }
    return render(request, 'accounts/view_payment_vouchers.html', context)

def payment_supplier(request):
    return render(request, 'accounts/payment_supplier.html')


from django.shortcuts import render, redirect
from .models import Expense
from django.urls import reverse


def add_expenses(request):
    expenses = Expense.objects.all()
    suppliers = Supplier.objects.all()  # Fetch all suppliers for the dropdown in the form

    if request.method == 'POST':
        batch_number = request.POST.get('batch_number')
        supplier_name = request.POST.get('supplier_name')
        item = request.POST.get('item')
        company_name = request.POST.get('company')  # Align the form field name
        category = request.POST.get('category')
        expiry_date = request.POST.get('expiry_date')
        created_date = request.POST.get('created_date')
        amount = request.POST.get('amount')

        try:
            supplier = Supplier.objects.get(company_name=company_name)
        except Supplier.DoesNotExist:
            # If the supplier doesn't exist, create a new one
            supplier = Supplier(company_name=company_name)
            supplier.save()

        expense = Expense.objects.create(
            batch_number=batch_number,
            supplier=supplier,
            item=item,
            company=company_name,  # Align with the Expense model field name
            expiry_date=expiry_date,
            created_date=created_date,
            amount=amount,
            category=category
        )
        return redirect('add_expenses')

    return render(request, 'accounts/add_expenses.html', {'expenses': expenses, 'suppliers': suppliers})
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense

def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    
    if request.method == 'POST':
        try:
            # Update the expense based on form data
            expense.batch_number = request.POST['batch_number']
            supplier_id = request.POST['supplier_name']
            expense.supplier = Supplier.objects.get(pk=supplier_id)  # Fetch supplier using primary key
            expense.item = request.POST['item']
            expense.company = request.POST['company']
            expense.expiry_date = request.POST['expiry_date']
            expense.created_date = request.POST['created_date']
            expense.amount = request.POST['amount']
            expense.category = request.POST['category']
            
            expense.save()  # Save the updated expense
            
            # Redirect to the expense detail page or a success page
            return redirect('add_expenses')
        except Supplier.DoesNotExist:
            # Handle the case where the supplier is not found
            raise Http404("Supplier does not exist")
    
    context = {
        'suppliers': Supplier.objects.all(),
        'expense': expense,
    }
    return render(request, 'accounts/update_expense.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return JsonResponse({'message': 'Expense deleted successfully'})




from django.shortcuts import render
from datetime import datetime
from .models import Purchase, PaymentVoucher

def purchase_ledger_report(request):
    # Retrieve data from Purchase table
    purchases = Purchase.objects.all()

    # Retrieve data from PaymentVoucher table
    vouchers = PaymentVoucher.objects.all()

    # Get filter parameters from request
    name_filter = request.GET.get('name_filter', '')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')

    # Convert start_date and end_date strings to datetime.date objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    # Generate ledger entries from Purchase data
    ledger_entries = []
    total_debit = 0
    total_credit = 0
    for purchase in purchases:
        if name_filter.lower() in purchase.supplier.company_name.lower() and (not start_date or purchase.purchase_date >= start_date) and (not end_date or purchase.purchase_date <= end_date):
            entry = {
                'date': purchase.purchase_date,
                'particulars': f"Supplier: {purchase.supplier.company_name}, Stock Purchased",
                'vch_type': "Purchase",
                'debit': 0,
                'credit': purchase.total_price
            }
            ledger_entries.append(entry)
            total_credit += purchase.total_price

    # Generate ledger entries from PaymentVoucher data
    for voucher in vouchers:
        if name_filter.lower() in voucher.customer_name.lower() and (not start_date or voucher.date >= start_date) and (not end_date or voucher.date <= end_date):
            entry = {
                'date': voucher.date,
                'particulars': f"Supplier: {voucher.customer_name}, Bank: {voucher.cash_or_bank}, Particular: {voucher.particular}, Account No: {voucher.account_no}, Check No: {voucher.check_no}",
                'vch_type': "Payment",
                'debit': voucher.amount,
                'credit': 0
            }
            ledger_entries.append(entry)
            total_debit += voucher.amount

    # Calculate balance
    balance = total_debit - total_credit
     # Perform pagination on the ledger entries
    page_number = request.GET.get('page', 1)
    paginator = Paginator(ledger_entries, 10)  # Show 10 entries per page
    ledger_entries = paginator.get_page(page_number)
    context = {
        'ledger_entries': ledger_entries,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'balance': balance,
        'name_filter': name_filter,
        'start_date': start_date_str,
        'end_date': end_date_str
    }
    return render(request, 'accounts/purchase_ledger_report.html', context)


from django.shortcuts import render
from django.db.models import Sum, F
from datetime import datetime

def stock_report(request):
    inventory_items = []

    # Retrieve date filter values
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Convert date filter values to datetime objects
    from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date() if from_date else None
    to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date() if to_date else None

    if not from_date and not to_date:
        # If no date filters are applied, retrieve all inventory items and display in the table
        all_inventories = ItemCreation.objects.all()
        for inventory in all_inventories:
            purchased_quantity = PurchaseItem.objects.filter(stock=inventory).aggregate(Sum('quantity'))['quantity__sum'] or 0
            purchase_return_quantity = PurchaseReturnItem.objects.filter(stock=inventory).aggregate(Sum('quantity'))['quantity__sum'] or 0
            inventory_items.append({
                'name': inventory.product_name,
                'purchased_quantity': purchased_quantity,
                'purchase_return_quantity': purchase_return_quantity,
                'actual_stock': purchased_quantity - purchase_return_quantity,
            })
    else:
        # Retrieve inventory items based on the date filters
        inventories = ItemCreation.objects.all()
        for inventory in inventories:
            purchased_quantity = PurchaseItem.objects.filter(stock=inventory, purchase__purchase_date__range=(from_date_obj, to_date_obj)).aggregate(Sum('quantity'))['quantity__sum'] or 0
            purchase_return_quantity = PurchaseReturnItem.objects.filter(stock=inventory, purchase_return__purchase_return_date__range=(from_date_obj, to_date_obj)).aggregate(Sum('quantity'))['quantity__sum'] or 0
            inventory_items.append({
                'name': inventory.product_name,
                'purchased_quantity': purchased_quantity,
                'purchase_return_quantity': purchase_return_quantity,
                'actual_stock': purchased_quantity - purchase_return_quantity,
            })

    context = {
        'inventory_items': inventory_items,
        'from_date': from_date,
        'to_date': to_date
    }

    return render(request, 'accounts/stock_report.html', context)



# USER pannel 
# ===========
def user_courier_management(request):
    return render(request, 'user/user_courier_management.html')

def user_query_management(request):
    return render(request, 'user/user_query_management.html')

def user_business_mis(request):
    return render(request, 'user/user_business_mis.html')

def user_travel_allowance(request):
    return render(request, 'user/user_travel_allowance.html')

def user_view_salary(request):
    return render(request, 'user/user_view_salary.html')    

def user_apply_leave(request):
    return render(request, 'user/user_apply_leave.html')

def user_ctc_structure(request):
    return render(request, 'user/user_ctc_structure.html')

def user_leave_balance(request):
    return render(request, 'user/user_leave_balance.html')

def user_courier_management_report(request):
    return render(request, 'user/user_courier_management_report.html')

def user_query_management_report(request):
    return render(request, 'user/user_query_management_report.html')

def user_business_mis_report(request):
    return render(request, 'user/user_business_mis_report.html')

def user_view_salary_report(request):
    return render(request, 'user/user_view_salary_report.html')

def user_apply_leave_report(request):
    return render(request, 'user/user_apply_leave_report.html')

def user_ctc_structure_report(request):
    return render(request, 'user/user_ctc_structure_report.html')

def user_leave_balance_report(request):
    return render(request, 'user/user_leave_balance_report.html')

def user_travel_allowance_report(request):
    return render(request, 'user/user_travel_allowance_report.html')