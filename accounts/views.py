from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
# import django_tables2 as tables
# from django_tables2 import SingleTableView

from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Account


# Create your views here.
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            gender = form.cleaned_data.get('gender')
            kra_pin = form.cleaned_data.get('kra_pin')
            id_no = form.cleaned_data.get('id_no')
            dob = form.cleaned_data.get('dob')
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password1')

            # authenticate the user if information is correct and valid
            account = authenticate(first_name=first_name, last_name=last_name, email=email,
                                   username=username, gender=gender, kra_pin=kra_pin, id_no=id_no,
                                   dob=dob, phone=phone, password=password)
            if account:
                login(request, account)
                
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, "accounts/login.html", context)


# function for account view
def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"]
            }
            form.save()
            context["success_message"] = "Account successfully updated"
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, "accounts/account.html", context)


def must_authenticate_view(request):
    return render(request, 'accounts/must_authenticate.html', {})


def home_screen_view(request, *args, **kwargs):
    context = {}

    users = Account.objects.all()
    context['users'] = users

    return render(request, "index.html", context)



# # Create your views here.
# class ProjectListView(SingleTableView):
#     model = Project
#     table_class = ProjectTable
#     template_name = '/projects.html'


# class ProjectTable(tables.Table):
#     class Meta:
#         model = Account
#         template_name = "accounts/custom.html"

# # view to display all users
# def user_list_view(request):
#     # User = get_user_model()
#     # return render(request, 'users_list.html', {'users': User.objects.all()})
#     context = {}
#     users = Account.objects.all()
#     context['users'] = users

#     return render(request, "accounts/account-users.html", context)
