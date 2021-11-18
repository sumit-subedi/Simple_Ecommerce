from django.shortcuts import render, redirect
from accounts.forms import UserAdminCreationForm, UserDetailForm


def register(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    return render(req, 'register.html', {'form': form})

def details (request):
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    form = UserDetailForm(initial = {'user':request.user})
    return render(request, 'register.html', {'form':form})
