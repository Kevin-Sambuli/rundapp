from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View

from django.core.mail import EmailMessage, send_mail

from django.conf import settings
from .forms import EmailForm, OwnershipForm
from .models import Ownership
from parcels.models import Parcels, ParcelDetails
from parcels.map import my_map
from django.core.serializers import serialize
from accounts.models import Account


class EmailAttachementView(View):
    form_class = EmailForm
    template_name = 'ownership/email_attachment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():

            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Sent email to %s' % email})
            except:
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name,
                      {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})

    # Single File Attachment
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.FILES)

    #     if form.is_valid():

    #         subject = form.cleaned_data['subject']
    #         message = form.cleaned_data['message']
    #         email = form.cleaned_data['email']
    #         attach = request.FILES['attach']

    #         try:
    #             mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
    #             mail.attach(attach.name, attach.read(), attach.content_type)
    #             mail.send()
    #             return render(request, self.template_name, {'email_form': form, 'error_message': 'Sent email to %s'%email})
    #         except:
    #             return render(request, self.template_name, {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

    #     return render(request, self.template_name, {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})


def ownership_view(request):
    context = {}
    if request.POST:
        form = OwnershipForm(request.POST)
        if form.is_valid():
            form.save()
            owner_id = form.cleaned_data.get('owner_id')
            parcel_id = form.cleaned_data.get('parcel_id')

            # authenticate the user if information is correct and valid
            tri = Ownership(owner=owner_id, parcel=parcel_id)
            tri.save()

        else:
            context['ownership_form'] = form
    else:
        form = OwnershipForm()
        context['ownership_form'] = form
    return render(request, 'ownership/ownership.html', context)


def search(request):
    context = {}
    if request.GET:
        # datas = list(Ownership.objects.all().values_list('parcel_id', flat=True))
        try:
            parcel = request.GET['parcel']
            parc = Ownership.objects.get(parcel=parcel)
            pd = ParcelDetails.objects.get(parcel=parcel)
            # print(pd.tenure)
            # print(pd.land_use)
            # print(pd.improvements)
            # print(pd.encumbrances)

            parcel_as_geojson = serialize('geojson', Parcels.objects.all())
            parcel_data = serialize('geojson', Parcels.objects.filter(id=parcel))

            map2 = my_map(parcel=parcel_data, land_parcels=parcel_as_geojson)
            map2.save('templates/ownership/parcel_search.html')

            context['details'] = pd

            own = Parcels.objects.get(id=parcel)
            # print('owner name from parcels', own.owner_id)
            # email = Account.objects.get(id=own.owner_id)
            # context['email'] = email
            # print('owner email', email.email)
            # print('owner email', Account.objects.get(id=own.owner_id).email)

            send_mail(
                'Ardhi Parcel Search',
                f'''Hey, {Ownership.objects.get(parcel=parcel).owner}, {request.user} has requested to view your\n 
                 land details, are you willing to allow him to view your land details.''',
                settings.DEFAULT_FROM_EMAIL,
                [Account.objects.get(id=own.owner_id).email],
                fail_silently=False,
            )
            # context['full_names'] = parc.owner
            context['full_names'] = Ownership.objects.get(parcel=parcel).owner
            context['email'] = Account.objects.get(id=own.owner_id)
        except:
            return HttpResponse('that parcel land you are searching doesnt exist')

        return render(request, 'ownership/search.html', context)


def my_property(request):
    # owner = Account.objects.get(id=request.user.id)
    parcels = Parcels.objects.filter(owner_id=request.user.id)  # accessing parcels of the logged user
    # print('parcels', parcels)

    # accessing each parcel detail and returning each parcel id
    parcel_id = list(Parcels.objects.filter(owner_id=request.user.id).values_list('id', flat=True))
    details = [det for det in list(Parcels.objects.filter(owner_id=request.user.id).values_list('id', flat=True))]

    # for det in parcels:
    #     print('det', det.id)
    #     details = ParcelDetails.objects.get(parcel=det.id)
    #     print('details', details)
    #     print('tenure', details.tenure)
    #     print('land use', details.land_use)
    #     print('encumbrances', details.encumbrances)
    #     print('improvements', details.improvements)
    #     print('')
    data = [ParcelDetails.objects.get(parcel=det) for det in parcels]
    print('data', data)

    points_as_geojson = serialize('geojson', Parcels.objects.all())
    parcel = serialize('geojson', Parcels.objects.filter(owner_id=request.user.id))
    map2 = my_map(parcel=parcel, land_parcels=points_as_geojson)
    map2.save('templates/ownership/parcel_map.html')

    context = {
        # 'owner': request,
        'parcels': parcels,
        'details': data,
    }
    return render(request, 'ownership/property.html', context)
