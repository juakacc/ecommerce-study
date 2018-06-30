from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from .forms import ContactForm

User = get_user_model()

class IndexView(TemplateView):
    template_name = 'index.html'

index = IndexView.as_view()

def contact(request):
    success = False
    form = ContactForm(request.POST or None)

    if form.is_valid():
        form.send_email()
        messages.success(request, 'Obrigado pelo contato')
    elif request.method == 'post':
        messages.error(request, 'Formulário inválido')
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    model = User
    success_url = reverse_lazy('login')

register = RegisterView.as_view()
