from django.db.models import Count, Sum
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from gamefolio_app.forms import AuthorForm
from django.contrib.auth import authenticate, login
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
        profiles = Author.objects.all()
        return render(request,'gamefolio_app/list_profiles.html',{'user_profile_list': profiles})

class NotFoundView(View):
    def get(self, request):
        return render(request, "gamefolio_app/404.html")

class SearchView(View):
    def get(self, request):
        
        #Parameters
        MAX_RESULTS_PER_PAGE = 8
        SQL_QUERY = f"""
        SELECT G.id, title, pictureID, genre, avg(rating) AS average
        FROM gamefolio_app_game G LEFT JOIN gamefolio_app_review R
            ON G.id == R.game
        """
        #We do a LEFT JOIN to include games with 0 reviews
        
        #Getting URL parameters
        params = []
        try:
            query = request.GET['query'].strip()
            if(query != ""):
                SQL_QUERY += f"WHERE title LIKE %s\n"
                params.append("%"+query+"%")
        except Exception as e:
            query = ""
        
        try:
            page = request.GET['page'].strip()
        except Exception as e:
            page = 0

        try:
            genre = request.GET['genre'].strip()
            joining_word = "AND" if "LIKE" in SQL_QUERY else "WHERE"
            SQL_QUERY += f"{joining_word} genre = %s\n"
            params.append(genre)
        except Exception as e:
            genre = ""

        try:
            sort = request.GET['sort'].strip()
        except:
            sort = 0

        #Prevent duplicate results
        SQL_QUERY += "GROUP BY G.id, title, genre\n"

        #Sorting
        if sort == "rd":                   #Rating Descending
            SQL_QUERY += "ORDER BY average DESC"
        elif sort == "ra":                 #Rating Ascending
            SQL_QUERY += "ORDER BY average ASC"
        elif sort ==  "vd":                #Views Descending
            SQL_QUERY += "ORDER BY G.views DESC"
        elif sort ==  "va":                #Views Ascending
            SQL_QUERY += "ORDER BY G.views ASC"
        elif sort ==  "ta":                #Title Ascending
            SQL_QUERY += "ORDER BY title ASC"
        elif sort ==  "td":                #Title Descending
            SQL_QUERY += "ORDER BY title DESC"

        results = Game.objects.raw( SQL_QUERY, params )
        result_count = len(results)
        page_count = result_count/MAX_RESULTS_PER_PAGE
        if(page_count == int(page_count)):
            page_count = int(page_count)
        else:
            page_count = int(page_count) + 1
        page_count = max(page_count,1)
        
        try:
            page = int(page)
            assert(page >= 0)
            assert(page < page_count)
        except Exception as e:
            print(e)
            return redirect("gamefolio_app:404")

        offset = page * MAX_RESULTS_PER_PAGE
        actual_results = results[offset:MAX_RESULTS_PER_PAGE+offset]
        current_page = page + 1

        #Calculates what page buttons we need to show at the bottom
        def calculate_pages():
            pages = []
            if(page_count <= 5):
                return [i for i in range(1,int(page_count+1))]
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
                        jump_index = i
                    i+=1
                    last_page = page
            
                pages.insert(jump_index, "type")
                return pages
        pages = calculate_pages()

        def get_unique_genres():
            return  Game.objects.values('genre').distinct()
        genres = get_unique_genres()

        sort_name = {0: "Relevance", "rd": "Rating ▼", "ra": "Rating ▲", "vd": "Views ▼", "va" : "Views ▲", "ta": "Alphabetical ▼", "td": "Alphabetical ▲"}[sort]

        context_dict = {"results" : actual_results, "query" : query, "count": result_count, "pages": pages, "current_page": current_page, "page_count": page_count, "current_genre": genre, "genres": genres, "sort_id": sort, "sort_name": sort_name}
        return render(request, 'gamefolio_app/search.html', context_dict)
    
