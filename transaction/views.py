from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import TransferForm, SubdivisionForm
from accounts.models import Account
from django.shortcuts import render
from parcels.models import Parcels

IMAGE_FILE_TYPES = ['txt', 'pdf', 'docx']


def file_upload(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            file = request.FILES['file_upload']
            fs = FileSystemStorage()

            file_type = fs.url(file).split('.')[-1]
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'transaction/error.html')
            else:
                uploaded_file_url = fs.url(file)
                user_pr.save()
                send_mail('Parcel Transfer',
                          f'''Hello {request.user}, This is to inform you that we have have received your email on the
                          land transfer of parcel, We will notify once the processing is complete.''',
                          settings.DEFAULT_FROM_EMAIL, [Account.objects.get(id=request.user.id).email],
                          fail_silently=False, )
                return render(request, 'transaction/details.html', {'uploaded_file_url': uploaded_file_url})
        return render(request, 'transaction/error.html')
    else:
        form = TransferForm()
        parcels = Parcels.objects.filter(owner_id=request.user.id).values_list('lr_no', flat=True)
    return render(request, 'transaction/model_form_upload.html', {'form': form, 'parcels': parcels})


# def create_profile(request):
#     form = TransferForm()
#     if request.method == 'POST' and request.FILES['file_upload']:
#         if form.is_valid():
#             # data = form.save(commit=False)
#             email = form.cleaned_data.get('email')
#             parcel_no = form.cleaned_data.get('parcel_no')
#             amount = form.cleaned_data.get('amount')
#
#             transfer = Transfer(seller=request.user.id, buyer_id=2, email=email,
#                                 parcel_no=parcel_no, amount=amount, file_upload='sasa')
#             transfer.save()
#
#             myfile = request.FILES['file_upload']
#             fs = FileSystemStorage()
#             filename = fs.save(myfile.name, myfile)
#             uploaded_file_url = fs.url(filename)
#
#             return render(request, 'transaction/simple_upload.html', {
#                 'uploaded_file_url': uploaded_file_url
#             })
#     return render(request, 'transaction/simple_upload.html')


# IMAGE_FILE_TYPES = ['txt', 'pdf', 'docx']


# def create_profile(request):
#     form = TransferForm()
#     if request.method == 'POST':
#         form = TransferForm(request.POST, request.FILES)
#         if form.is_valid():
#             user_pr = form.save(commit=False)
#             email = form.cleaned_data.get('email')
#             parcel_no = form.cleaned_data.get('parcel_no')
#             amount = form.cleaned_data.get('amount')
#
#             file = request.FILES['file_upload']
#             fs = FileSystemStorage()
#             uploaded_file_url = fs.url(file)
#
#             print('url file', uploaded_file_url)
#             print('data', email, parcel_no, amount)
#             file_type = fs.url(file).split('.')[-1]
#
#             if file_type not in IMAGE_FILE_TYPES:
#                 return render(request, 'transaction/error.html')
#
#             buyer = Account.objects.get(email=email)
#             user_pr.save()
#             form.save()
#             transfer = Transfer(seller=request.user.id, buyer_id=buyer.id, email=email,
#                                 parcel_no=parcel_no, amount=amount, file_upload=uploaded_file_url)
#             transfer.save()
#
#             # return render(request, 'transaction/details.html', {'uploaded_file_url': uploaded_file_url})
#             return redirect('home')
#     context = {"form": form}
#     return render(request, 'transaction/create.html', context)

def subdivision(request):
    context = {}
    if request.method == 'POST':
        form = SubdivisionForm(request.POST)
        if form.is_valid():
            form.save()

            send_mail('Ardhi Parcel subdivision',
                      f'''Hello {request.user}, This is to inform you that we have have received your email on\n
                             land subdivision, We'll you know when you cant commence your process.''',
                      settings.DEFAULT_FROM_EMAIL,
                      [Account.objects.get(id=request.user.id).email],
                      fail_silently=False,
                      )
            return redirect('home')
    else:
        form = SubdivisionForm()
        parcels = Parcels.objects.filter(owner_id=request.user.id).values_list('lr_no', flat=True)
    return render(request, 'transaction/subdivision.html', {'form': form, 'parcels': parcels})

