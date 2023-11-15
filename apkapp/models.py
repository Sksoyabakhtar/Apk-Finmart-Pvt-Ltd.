from django.db import models
from datetime import date, datetime
from django.utils import timezone

class AdminUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to='admin_images/', null=True, blank=True)
    active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, default='admin')

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_type = models.CharField(max_length=100)
    trading_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=15, default='GST1234567')
    date_added = models.DateField(default=date.today)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    location = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/', max_length=255, null=True, blank=True)


    def __str__(self):
        return self.company_name


class Department(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    head = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    location = models.CharField(max_length=255)
    location_head = models.CharField(max_length=255)
    address_line1 = models.TextField()
    address_line2 = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)


class CompanyPolicy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%b-%d-%Y, %I:%M %p')}"

class Designation(models.Model):
    designation_name = models.CharField(max_length=100)
    company_type = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True, choices=((True, 'Activate'), (False, 'Deactivate')))
    created_at = models.DateTimeField(auto_now_add=True)

  


from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    website = models.URLField()
    password = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=100)
    img = models.ImageField(upload_to='client_images/')





#employee_cretion Page
#___________________________________________________________________________________________

class Employee(models.Model):
    full_name = models.CharField(max_length=255, default="John Doe")
    email = models.EmailField(default="example@example.com")
    phone = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(default="2000-01-01", null=True, blank=True)
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    
    company = models.ForeignKey(Company, on_delete=models.SET_DEFAULT, default=1)
    department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=1)
    designation = models.ForeignKey(Designation, on_delete=models.SET_DEFAULT, default=1)
    
    OFFICE_SHIFT_CHOICES = (
        ('9-5', '9 AM to 5 PM'),
        ('6-2', '6 AM to 2 PM'),
        ('2-10', '2 PM to 10 PM'),
        ('10-6', '10 PM to 6 AM'),
    )
    office_shift = models.CharField(max_length=10, choices=OFFICE_SHIFT_CHOICES, default="9-5")
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=1)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    
    ATTENDANCE_TYPE_CHOICES = (
        ('general', 'General'),
        ('ip_based', 'IP Based'),
    )
    attendance_type = models.CharField(max_length=10, choices=ATTENDANCE_TYPE_CHOICES, default="general")
    
    password = models.CharField(max_length=128, null=True, blank=True)
    joining_date = models.DateField(default="2023-01-01", null=True, blank=True)
    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)


class EmployeeSalary(models.Model):
    employee_id = models.CharField(max_length=20)
    employee_ref = models.ForeignKey(Employee, on_delete=models.CASCADE, default=1) 
    month = models.CharField(max_length=20, default='January')  
    basic = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)
    conv = models.DecimalField(max_digits=10, decimal_places=2)
    m_epf = models.DecimalField(max_digits=10, decimal_places=2)
    m_esi = models.DecimalField(max_digits=10, decimal_places=2)
    lta = models.DecimalField(max_digits=10, decimal_places=2)
    medical = models.DecimalField(max_digits=10, decimal_places=2)
    r_allow = models.DecimalField(max_digits=10, decimal_places=2)
    g_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    n_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    e_epf = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    e_esi = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    er_epf = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    er_esi = models.DecimalField(max_digits=10, decimal_places=2, null=True)

   
    status = models.CharField(max_length=20, default="Active")
    wages_type = models.CharField(max_length=20, default="Monthly")
    billable_type = models.CharField(max_length=20, default="Billable")
    bonus = models.CharField(max_length=3, default="No")
    leave_encash = models.CharField(max_length=3, default="No")
    epf = models.CharField(max_length=3, default="Yes")
    esi = models.CharField(max_length=3, default="Yes")
    epf_pension = models.CharField(max_length=3, default="No")
    tds = models.CharField(max_length=3, default="No")
    hr_deduction = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = 'Employee Salary'
        verbose_name_plural = 'Employee Salaries'    

class Project(models.Model):
    title = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Highest', 'Highest'),
    ]

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium',
    )
    
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Complete', 'Complete'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Not Started'
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    assigned_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=1)
    summary = models.TextField()

    def __str__(self):
        return self.title


class Training(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    training_type = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2) 


class Task(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE) 
    start_date = models.DateField()
    end_date = models.DateField()
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    project_users = models.CharField(max_length=100)
    

    def __str__(self):
        return self.title
    
from django.db import models

class ItemCreation(models.Model):
    product_name = models.CharField(max_length=255) 
    quantity = models.PositiveIntegerField() 

    def __str__(self):
        return self.product_name
    

from django.db import models

class Supplier(models.Model):
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    gstin_number = models.CharField(max_length=15)
    address = models.TextField()

class TaxType(models.Model):
    tax_name = models.CharField(max_length=100)
    tax_rate = models.IntegerField()
    description = models.TextField()
    tax_type = models.CharField(max_length=20, default='Percentage')

    def __str__(self):
        return self.tax_name
    

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)  
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    invoice_date = models.DateField()
    due_date = models.DateField()

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_type = models.ForeignKey('TaxType', on_delete=models.CASCADE)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

class Discount(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)

class GrandTotal(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
        


class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_id = models.CharField(max_length=50, unique=True)  
    purchase_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchase_items', on_delete=models.CASCADE)
    stock = models.ForeignKey(ItemCreation, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    gst = models.DecimalField(max_digits=5, decimal_places=2)
    gstprice = models.DecimalField(max_digits=10, decimal_places=2)
    igst = models.DecimalField(max_digits=5, decimal_places=2)
    igstprice = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)    

 
    
from django.db import models

class PurchaseReturn(models.Model):
    invoice_no = models.CharField(max_length=20)
    purchase_date = models.DateField()
    supplier_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    gstin_no = models.CharField(max_length=20, blank=True)
    purchase_return_date = models.DateField()

    def __str__(self):
        return self.supplier_name

    def get_total_price(self):
        total_price = 0
        for item in self.purchase_return_items.all():
            total_price += item.total_price
        return total_price

class PurchaseReturnItem(models.Model):
    purchase_return = models.ForeignKey(PurchaseReturn, related_name='purchase_return_items', on_delete=models.CASCADE)
    stock = models.ForeignKey(ItemCreation, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=5, decimal_places=2)
    gstprice = models.DecimalField(max_digits=10, decimal_places=2)
    igst = models.DecimalField(max_digits=5, decimal_places=2)
    igstprice = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase Item {self.pk} - {self.stock.product_name}"



from django.db import models

class PaymentVoucher(models.Model):
    voucher_number = models.CharField(max_length=50)
    cash_or_bank = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)
    date = models.DateField()
    narration = models.CharField(max_length=50)
    particular = models.CharField(max_length=50)
    bill_no = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_no = models.CharField(max_length=50)
    check_no = models.CharField(max_length=50)


from django.db import models

class Expense(models.Model):
    batch_number = models.CharField(max_length=100, default=0)
    CATEGORY_CHOICES = (
        ('Stationary', 'Stationary'),
        ('Fuel', 'Fuel'),
        # Add other categories as needed
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=1)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Stationary')
    item = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    expiry_date = models.DateField()
    created_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)
    clock_in = models.TimeField()
    clock_out = models.TimeField(null=True, blank=True)    


from django.db import models


class OfficeShift(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    shift_name = models.CharField(max_length=100)
    monday_in = models.TimeField()
    monday_out = models.TimeField()
    tuesday_in = models.TimeField()
    tuesday_out = models.TimeField()
    wednesday_in = models.TimeField()
    wednesday_out = models.TimeField()
    thursday_in = models.TimeField()
    thursday_out = models.TimeField()
    friday_in = models.TimeField()
    friday_out = models.TimeField()
    saturday_in = models.TimeField()
    saturday_out = models.TimeField()
    sunday_in = models.TimeField()
    sunday_out = models.TimeField()

    def __str__(self):
        return self.shift_name
    


from django.db import models
from .models import Company

class Holiday(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    finish_date = models.DateField()

    def __str__(self):
        return self.title  

from django.db import models

class LeaveType(models.Model):
    leave_type_name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()  
    quantity = models.PositiveIntegerField() 

    def __str__(self):
        return self.leave_type_name
      


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)  
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    finish_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    attachment = models.FileField(upload_to='leave_attachments/', null=True, blank=True)
    leave_reason = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.finish_date} ({self.status})"


class Branch(models.Model):
    branch_id = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    location = models.TextField()



class Allowance(models.Model):
    allowance = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.allowance  


from django.db import models

class Deduction(models.Model):
    deduction_name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return self.deduction_name


from django.db import models

class Investment(models.Model):
    TYPE_CHOICES = [
        ('Fixed Deposit', 'Fixed Deposit'),
        ('Recurring Deposit', 'Recurring Deposit'),
        ('SIP', 'SIP'),
        ('Investment', 'Investment'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    duration_of_years = models.PositiveIntegerField()

    def __str__(self):
        return self.name



from django.utils.crypto import get_random_string
from random import randint

class MutualFund(models.Model):
    query_id = models.CharField(max_length=20, unique=True)
    product_type = models.CharField(max_length=50, null=True)
    investor_name = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    scheme_name = models.CharField(max_length=100, blank=True, null=True)
    nominee_name = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateField(default=date.today)
    product_type = models.CharField(max_length=255, null=True, blank=True)

    def _str_(self):
        return self.query_id

    def save(self, *args, **kwargs):

        if not self.query_id:
            # Generate a unique query_id
            prefix = 'APKQ_'
            unique_id = randint(1, 9999)
            self.query_id = f'{prefix}{unique_id}'

        super().save(*args, **kwargs)





def generate_unique_query_id(prefix='APKQ_'):
    unique_id = randint(1, 9999)
    return f'{prefix}{unique_id}'

class FixedDeposit(models.Model):
    query_id = models.CharField(max_length=100, unique=True)
    investor_name = models.CharField(max_length=255)
    investor_pan = models.CharField(max_length=10)
    investor_dob = models.DateField()
    investor_email = models.EmailField()
    investor_mobile = models.CharField(max_length=15)
    
    # Fixed Deposit fields
    company_name = models.CharField(max_length=255)
    roi = models.FloatField()
    tenure_type = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('half_yearly', 'Half-Yearly')])
    tenure_duration = models.CharField(max_length=20, choices=[('annually', 'Annually'), ('cumulative', 'Cumulative')])
    nominee_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(default=date.today)
    product_type = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.query_id:
            self.query_id = generate_unique_query_id()
        super().save(*args, **kwargs)


class LifeInsurance(models.Model):
    query_id = models.CharField(max_length=100, unique=True)
    proposer_name = models.CharField(max_length=255)
    proposer_dob = models.DateField()
    proposer_pan = models.CharField(max_length=20)
    life_assured_name = models.CharField(max_length=255)
    life_assured_dob = models.DateField()
    life_assured_pan = models.CharField(max_length=20)
    life_assured_aadhar_no = models.CharField(max_length=20)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    company_name = models.CharField(max_length=255)
    plan_name = models.CharField(max_length=255)
    ppt = models.CharField(max_length=10)
    pt = models.CharField(max_length=10)
    nominee_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    premium_frequency = models.CharField(max_length=50)
    created_at = models.DateField(default=date.today)
    product_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.proposer_name} - {self.plan_name}"

    def save(self, *args, **kwargs):
        if not self.query_id:
            self.query_id = generate_unique_query_id()
        super().save(*args, **kwargs)



class HealthInsurance(models.Model):
    query_id = models.CharField(max_length=100, unique=True)
    policy_holder_name = models.CharField(max_length=255)
    proposer_dob = models.DateField()
    proposer_pan = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    company_name = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    frequency = models.CharField(max_length=50)
    nominee_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateField(default=date.today)
    product_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.policy_holder_name} - {self.plan}"

    def save(self, *args, **kwargs):
        if not self.query_id:
            self.query_id = generate_unique_query_id()
        super().save(*args, **kwargs)


class GeneralInsurance(models.Model):
    query_id = models.CharField(max_length=100, unique=True)
    investor_name = models.CharField(max_length=255, verbose_name='Investor Name')
    pan_number = models.CharField(max_length=10, verbose_name='PAN Number')
    date_of_birth = models.DateField(verbose_name='Date of Birth')
    email = models.EmailField(verbose_name='Email')
    mobile = models.CharField(max_length=15, verbose_name='Mobile')
    category = models.CharField(max_length=255, verbose_name='Category')
    company_name = models.CharField(max_length=255, verbose_name='Company Name')
    frequency = models.CharField(max_length=255, verbose_name='Frequency')
    nominee = models.CharField(max_length=255, verbose_name='Nominee')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    created_at = models.DateField(default=date.today)
    product_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.investor_name} - {self.pan_number}"

    def save(self, *args, **kwargs):
        if not self.query_id:
            self.query_id = generate_unique_query_id()
        super().save(*args, **kwargs)


class Bonds(models.Model):
    query_id = models.CharField(max_length=100, unique=True)
    investor_name = models.CharField(max_length=255, verbose_name='Investor Name')
    pan_number = models.CharField(max_length=10, verbose_name='PAN Number')
    date_of_birth = models.DateField(verbose_name='Date of Birth')
    email = models.EmailField(verbose_name='Email')
    mobile = models.CharField(max_length=15, verbose_name='Mobile')
    company_name = models.CharField(max_length=255, verbose_name='Company Name')
    scheme_name = models.CharField(max_length=255, verbose_name='Scheme Name')
    nominee_name = models.CharField(max_length=255, verbose_name='Nominee Name')
    roi = models.CharField(max_length=255, verbose_name='ROI')
    frequency = models.CharField(max_length=255, verbose_name='Frequency')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    created_at = models.DateField(default=date.today)
    product_type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.investor_name} - {self.pan_number}"

    def save(self, *args, **kwargs):
        if not self.query_id:
            self.query_id = generate_unique_query_id()  # You need to implement or replace this function
        super().save(*args, **kwargs)


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=255)


class NPS(models.Model):
    investor_name = models.CharField(max_length=255)
    pan_number = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    asp_name = models.CharField(max_length=255)
    nominee_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_companies = models.ManyToManyField(InsuranceCompany)
    query_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateField(default=date.today)
    product_type = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.query_id:
            self.query_id = generate_unique_query_id()
        super().save(*args, **kwargs)



