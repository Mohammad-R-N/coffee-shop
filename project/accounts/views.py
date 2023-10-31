from django.shortcuts import render,redirect
from django.views import View
from .form import UserRegistrationForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(View):
    form_class=UserRegistrationForm
    template_name="accounts/registration.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            User.objects.create_user(cd["username"],cd["email"],cd["password"])
            messages.success(request,"you registered successfully","green")
            return redirect("core:home")
        return render(request,self.template_name,{"form":form})



class UserLoginView(View):
    form_class=UserLoginForm
    template_name="accounts/login.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request,*args,**kwargs)
    
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{"form":form})
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd["username"],password=cd["password"])
            if user is not None:
                login(request,user)
                messages.success(request,"you login successfully","green")
                return redirect("core:home")
        
            messages.success(request,"username or password is wrong","red")
            
        return render(request,self.template_name,{"form":form})
    

class UserLogoutView(LoginRequiredMixin,View):

    def get(self,request):
        logout(request)
        messages.success(request,"logout","red")
        return redirect("core:home")