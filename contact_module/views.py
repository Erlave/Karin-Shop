from django.shortcuts import render, get_object_or_404
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from .form import ContactForm
from .models import contact_model

# Create your views here.
# def contact(request):
#     return render(request , 'contact_module/contact_page.html')



def contact_view(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contacts=contact_model(
                subject=contact_form.cleaned_data.get('subject'),
                phone_number=contact_form.cleaned_data.get('phone'),
                message=contact_form.cleaned_data.get('message')
            )

            contacts.save()
            return redirect(reverse('home'))
    else:
        contact_form = ContactForm()

    return render(request,'contact_module/contact_page.html',
                  {'contact_form': contact_form})