from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from gamefolio_app.models import Author
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

from gamefolio_app.forms import UserForm , AuthorForm, CreateListForm
from gamefolio_app.models import Game, Review, List, ListEntry


class IndexView(View):
    def get(self, request):
        game_list = sorted(Game.objects.all(), key = lambda p : p.average_rating())[:5]
        reviews_list = Review.objects.order_by('-likes')[:6]
        
        context_dict = {}
        context_dict['games'] = game_list
        context_dict['reviews'] = reviews_list
        
        return render(request, 'gamefolio_app/index.html', context=context_dict)
      
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return reverse('gamefolio_app:register_profile')
    

@method_decorator(login_required, name='dispatch')
class RegisterProfileView(View):

    def get(self, request):
        form = AuthorForm()
        context = {'form': form}
        return render(request, 'gamefolio_app/profile_registration.html', context)

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
        return render(request, 'gamefolio_app/profile_registration.html', context)
    

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
                return redirect(reverse('gamefolio_app:profile'))
            else:
                return HttpResponse("Your Gamefolio account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")


@method_decorator(login_required, name='dispatch')
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('gamefolio_app:index')
    
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
            user_reviews = Review.objects.filter(author=user_profile)
        except TypeError:
            return redirect(reverse('gamefolio_app:index'))

        sort_reviews_by = request.GET.get('sort_reviews', 'recent')

        if sort_reviews_by == 'liked':
            user_reviews = user_reviews.annotate(likes_total=Sum('likes')).order_by('-likes_total', '-datePosted')
        else:
            user_reviews = user_reviews.order_by('-datePosted')

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form, 'user_reviews': user_reviews}
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
        sort_by = request.GET.get('sort_by', 'reviews')
        profiles = Author.objects.annotate(total_reviews=Count('review'), total_likes=Sum('review__likes'))
        
        if sort_by == 'likes':
            profiles = profiles.order_by('-total_likes')
        else:
            profiles = profiles.order_by('-total_reviews')
            
        return render(request,'gamefolio_app/list_profiles.html',{'authors': profiles})
        
class ListView(View):
    @method_decorator(login_required)
    def get(self, request, author_username, list_title, slug):
        list_obj = get_object_or_404(List, author__user__username=author_username, title=list_title, slug=slug)
        list_entries = list_obj.listentry_set.all()
        all_games = Game.objects.all()
        context = {'list_obj': list_obj, 'list_entries': list_entries, 'all_games': all_games}
        return render(request, 'gamefolio_app/list.html', context)
    
    @method_decorator(login_required)
    def post(self, request, author_username, list_title, slug):
        list_obj = get_object_or_404(List, author__user__username=author_username, title=list_title, slug=slug)
        if request.user == list_obj.author.user:
            game_id = request.POST.get('game')
            game = get_object_or_404(Game, id=game_id)
            ListEntry.objects.create(list=list_obj, game=game)
        return redirect('gamefolio_app:list', author_username=author_username, list_title=list_title, slug=slug)


class ListsView(View):
    @method_decorator(login_required)
    def get(self, request):
        create_list_form = CreateListForm()
        lists = List.objects.all()
        list = ListEntry.objects.all()

        context_dict = {'all_lists': lists,
                        'create_list_form': create_list_form,
                        'user_list' : list,}
        
        return render(request,'gamefolio_app/lists.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        create_list_form = CreateListForm(request.POST)
        if create_list_form.is_valid():
            new_list = create_list_form.save(commit=False)
            new_list.author = request.user.author
            new_list.save()
            games = create_list_form.cleaned_data['games']
            for game in games:
                ListEntry.objects.create(list=new_list, game=game)
            return redirect('gamefolio_app:lists')
        else:
            lists = List.objects.all()
            list = ListEntry.objects.all()

            context_dict = {
                'create_list_form': create_list_form,
                'all_lists': lists,
                'user_list': list,
            }

            return render(request, 'gamefolio_app/lists.html', context_dict)
