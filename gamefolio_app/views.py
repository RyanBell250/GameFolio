from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from gamefolio_app.forms import UserForm , AuthorForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'gamefolio_app/index.html')
    
class RegisterView(View):
    template_name = 'register.html'  

    def get(self, request):
        user_form = UserForm()
        author_form = AuthorForm()
        return render(request, self.template_name, {'user_form': user_form, 'author_form': author_form})

    def post(self, request):
        registered = False
        user_form = UserForm(request.POST)
        author_form = AuthorForm(request.POST)

        if user_form.is_valid() and author_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            author = author_form.save(commit=False)
            author.user = user

            if 'picture' in request.FILES:
                author.picture = request.FILES['picture']

            author.save()

            registered = True
        else:
            print(user_form.errors, author_form.errors)

        return render(request, self.template_name, {'registered': registered, 'user_form': user_form, 'author_form': author_form})
    

class UserLoginView(View):
    template_name = 'gamefolio_app/login.html'  

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('gamefolio_app:index'))
            else:
                return HttpResponse("Your Gamefolio account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('gamefolio_app:index')

    

        
         

                

