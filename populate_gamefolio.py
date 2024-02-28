import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','gamefolio.settings')
import django
django.setup()

import requests
import random
import numpy
from datetime import datetime

from gamefolio_app.models import Author, Game, Review, List, ListEntry
from django.contrib.auth.models import User

### Game Parameters ###
#Secret API Key stuff, only reason its here is cos the repo is private
CLIENT_ID = "2w3wcvvgqis5plpiqbhxh7cud3szm0"
BEARER = "5obg1bjuw5aniisksxd401n5sbca2f"
BASE_REQUEST = {'headers': {'Client-ID': CLIENT_ID, 'Authorization': f'Bearer {BEARER}'}, "data" : ""}
NUMBER_OF_GAMES = 500 #Total number of games to load into database
RESULTS_PER_QUERY = 500  #Max results per query is 500

### User Parameters ###
NUMBER_OF_USERS = 100
descriptors = ["Little", "Big", "Small", "Hidden", "Crazy", "Blue", "Red", "Green", "Yellow", "Rainbow", "Silly"]
usernames = ["Mario", "Link", "Zelda", "Luigi", "Yoshi", "DonkeyKong", "Sonic", "Peach", "Steve", "Mastercheif", "Pikachu", "Goomba", "Bowser"]

#Review Parameters
AVG_REVIEWS_PER_GAME = 15
reviews = ["Great game!", "I hated this.", ":(", "This is maybe the best thing I've ever played in my life!", "This was so horrible", "Ok!", 
           "It was alright", "I've played better.", "I can't believe this cost money.", "How to refund?", 
           "I would sacrifice my first born to play this for the first time again"]
start_date = datetime(2020, 1, 1)
end_date = datetime.now()

#List Parameters
USER_WITH_LIST_PERCENT = 0.7
list_names = ["Worst games of all time", "{username}'s list of best games of all time", "Recommend", "Temp", "My list", "Good", "2024 Ranked", 
              "Games to play on the train", "Games to play on the plane", "Games to never play on the train", "Made me cry", "Good stories",
              "Wishlist", "Play later", "These look good", "Interesting", "Try out?"]

def populate_games():
    query_count = 0
    for games_left in range(NUMBER_OF_GAMES, 0, -RESULTS_PER_QUERY):

        offset = query_count * RESULTS_PER_QUERY
        games_this_query = min(RESULTS_PER_QUERY, games_left)

        request = BASE_REQUEST
        request['data'] += "fields name, summary, genres.name, cover.image_id;"                            #Fields we want
        request['data'] += f"limit {games_this_query};"                                                    #Max 500 results per query
        request['data'] += f"offset {offset};"                                                             #Offsets the results
        request['data'] += "where version_parent =n & cover!=n & rating_count >= 0 & parent_game =n;"     #Found this mixture of parameters removes console editions of games etc.
        request['data'] += "sort rating desc;"                                                            #Only get the "good/popular" games first

        response = requests.post('https://api.igdb.com/v4/games', **BASE_REQUEST)
        games_data = response.json()
        query_count += 1

        for entry in games_data:
            name = entry['name'] 
            if 'summary' in entry:
                description = entry['summary']
            if 'genres' in entry:
                genre = entry['genres'][0]['name']
            if 'cover' in entry:
                picture = entry['cover']['image_id']

            game = Game(title = name, description = description, genre = genre, pictureId = picture)
            game.save()

def populate_users():
    for i in range(NUMBER_OF_USERS):
        try:
            #generate random username
            username = random.choice(descriptors) + random.choice(usernames) + str(random.randint(1000, 9999))
            password = username #use username for password so it is easy to sign in to test account
            email = username +"@email.com" #fake email
            user = User.objects.create_user(username, email, password)

            author = Author(user = user)
            author.save()
        except Exception as e:
            print(e)
            return

def populate_reviews():
    seconds_delta = ((end_date - start_date).days * 24 * 60 * 60)
    start_date_seconds = start_date.day *24*60*60
    for game in Game.objects.all():
        avg_rating = random.randint(3, 7)
        for i in range(int(numpy.random.normal(loc = AVG_REVIEWS_PER_GAME, scale = 10))):       #Most games will get 15 reviews, some will get more, others less
            user = Author.objects.order_by('?').first()                                         #Gets random user
            content = random.choice(reviews)
            rating = int(numpy.random.normal(loc = avg_rating, scale = 3))                      #Generates reviews normally around a point for more realism
            
            views = random.randint(0, 10000)
            likes = int(views * random.random()*0.5)                                            #Likes will be a percentage of the views
            
            random_date = start_date_seconds + random.randint(0, seconds_delta)
            datePosted = datetime.fromtimestamp(random_date)    
            
            review = Review(user = user, game = game, rating = rating, content = content, likes = likes, views = views, datePosted = datePosted)
            review.save()

def populate_lists():
    for user in Author.objects.all():
        #Not every user is gonna have lists
        if(random.random() > USER_WITH_LIST_PERCENT):
            continue
        
        #Create random number of lists
        for i in range(1, 5):
            #first make list
            list_name = random.choice(list_names).format(username = user.user.username)
            description = random.choices(["", "This is just a placeholder list description rather than nothing."])
            list = List(user = user, title = list_name, description = description)
            list.save()
            
            #then make entries
            number_of_games = random.randint(5, 30)
            games = Game.objects.order_by('?')[:number_of_games]    #Get first x random games

            for game in games:
                listEntry = ListEntry(list = list, game = game)
                listEntry.save()


def clear_database():
    for listEntry in ListEntry.objects.all():
        listEntry.delete()
    for list in List.objects.all():
        list.delete()
    for review in Review.objects.all():
        review.delete()
    for game in Game.objects.all():
        review.delete()
    for user in User.objects.filter(is_superuser = False, is_staff = False).all():
        user.delete()

if __name__ == '__main__':
    populate_users()
    populate_games()
    populate_reviews()
    populate_lists()