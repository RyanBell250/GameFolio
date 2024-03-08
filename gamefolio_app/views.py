from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from gamefolio_app.forms import UserForm , AuthorForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView
from gamefolio_app.models import Game, Review, Author

class IndexView(View):
    def get(self, request):
        game_list = sorted(Game.objects.all(), key = lambda p : p.average_rating())[:5]
        reviews_list = Review.objects.order_by('-likes')[:6]
        
        context_dict = {}
        context_dict['games'] = game_list
        context_dict['reviews'] = reviews_list
        
        return render(request, 'gamefolio_app/index.html', context=context_dict)
      
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('gamefolio_app:register_profile')
    
class RegisterView(View):
    template_name = 'gamefolio/registration_form.html'  

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
    template_name = 'gamefolio_app/registration/login.html'  

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

@method_decorator(login_required, name='dispatch')
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('gamefolio_app:index')


@method_decorator(login_required, name='dispatch')
class RegisterProfileView(View):
    template_name = 'gamefolio_app/registration_profile.html'

    def get(self, request):
        form = AuthorForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('gamefolio_app:index'))
        else:
            print(form.errors)

        context = {'form': form}
        return render(request, self.template_name, context)
    


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = Author.objects.get_or_create(user=user)[0]
        form = AuthorForm({'website': user_profile.website, 'picture': user_profile.picture})

        return (user, user_profile, form)
    

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('gamefolio_app:index'))
        
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
                
        return render(request, 'gamefolio_app/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('gamefolio_app:index'))
        
        if request.user != user:
            return HttpResponse("Unauthorized access")
            
        form = AuthorForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('gamefolio_app:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
        return render(request, 'gamefolio_app/profile.html', context_dict)

class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = Author.objects.all()
        return render(request,'gamefolio_app/list_profiles.html',{'user_profile_list': profiles})

class NotFoundView(View):
    def get(self, request):
        return render(request, "gamefolio_app/404.html")

MAX_RESULTS_PER_PAGE = 8
class SearchView(View):
    def get(self, request):
        try:
            query = request.GET['query'].strip()
        except Exception as e:
            query = ""
        
        try:
            page = request.GET['page'].strip()
        except Exception as e:
            page = 0

        try:
            genre = request.GET['genre'].strip()
        except Exception as e:
            genre = ""

        if(genre != ""):
            results = Game.objects.filter(genre__contains=genre)
        else:
            results = Game.objects.filter(title__icontains=query)

        try:
            sort = request.GET['sort'].strip()
        except:
            sort = 0

        if sort == "rd":                   #Rating Descending
            results = sorted(results, key = lambda p : p.average_rating(), reverse=True)
        elif sort == "ra":                 #Rating Ascending
            results = sorted(results, key = lambda p : p.average_rating())
        elif sort ==  "vd":                #Views Descending
            results = results.order_by("-views")
        elif sort ==  "va":                #Views Ascending
            results = results.order_by("views")
        elif sort ==  "ta":                #Title Ascending
            results = results.order_by("title")
        elif sort ==  "td":                #Title Descending
            results = results.order_by("-title")

        result_count = len(results)
        
        page_count = result_count/MAX_RESULTS_PER_PAGE
        page_count = int(page_count) + 1

        try:
            page = int(page)
            assert(page >= 0)
            assert(page < page_count)
        except:
            return redirect(f"gamefolio_app:404")

        offset = page * MAX_RESULTS_PER_PAGE
        actual_results = results[offset:MAX_RESULTS_PER_PAGE+offset]
        current_page = page + 1

        pages = []
        if(page_count <= 5):
            pages = [i for i in range(1,int(page_count+1))]
        else:
            count = 0
            for i in range(current_page-1, 1, -1):
                if(count == 2):
                    break
                count += 1;
                pages.append(i)
            
            count = 0
            for i in range(current_page, page_count, 1):
                if(count == 3):
                    break
                count += 1;
                pages.append(i)

            if(1 not in pages):
                pages.append(1)
            if(page_count not in pages):
                pages.append(page_count)

            pages.sort()

            last_page = pages[0]
            jump_index = -1
            i = 0
            for page in pages:
                if(page-last_page > 1):
                    print(page, last_page)
                    jump_index = i
                i+=1
                last_page = page
        
            pages.insert(jump_index, "type")

        context_dict = {"results" : actual_results, "query" : query, "count": result_count, "pages": pages, "current_page": current_page, "page_count": page_count, "current_genre": genre}
        return render(request, 'gamefolio_app/search.html', context_dict)
    