from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) 

    website = models.URLField(blank = True)
    picture = models.ImageField(upload_to="profile_images", blank = True)

    def __str__(self):
        return self.user.username

class Game(models.Model):
    id = models.SlugField(unique = True, primary_key = True)

    title = models.CharField(max_length = 128, blank = False)
    genre = models.CharField(max_length = 128)                                   
    pictureId = models.CharField(max_length = 32)                               #Short ID which can be added to an URL to return a picture
    description = models.TextField(default = "This game has no description.")   
    views = models.IntegerField(default = 0)

    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        index = Game.objects.filter(id__startswith=slug).count()    #If we already have a game with the same name, we will want to add an
        if(index != 0):                                             #index to the slug. So we find games with the same slug and if they exist
            slug += "-" + str(index)                                #we add the index onto the end.
        self.id = slug                                              #e.g two games called: Test Game we get "test-game" and "test-game-1"
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = (
        (1, "½"), 
        (2, "★"),
        (3, "★½"),
        (4, "★★"),
        (5, "★★½"),
        (6, "★★★"),
        (7, "★★★½"),
        (8, "★★★★"),
        (9, "★★★★½"),
        (10, "★★★★★"),
    )

    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    user = models.ForeignKey(Author, on_delete = models.CASCADE)
   
    content = models.TextField(blank = False)
    views = models.IntegerField(default = 0)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)  #Only allows 1-10 ratings or 1/2-5 stars
    datePosted = models.DateTimeField(default = timezone.now())
    likes = models.IntegerField(default = 0)

    def save(self, *args, **kwargs):
        if int(self.rating) < 1 or int(self.rating) > 10:
            self.rating = max(min(self.rating, 10), 1) #Clamps rating between 1 and 10
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.user.username + " - " + self.game.title + ": " + self.RATING_CHOICES[self.rating-1][1]
          

class List(models.Model):
    user = models.ForeignKey(Author, on_delete = models.CASCADE)

    slug = models.SlugField()  #NOT UNIQUE as two users can have list with same name
    title = models.CharField(max_length = 128, blank = False)
    description = models.TextField(default = "", blank = True)

    def save(self, *args, **kwargs):
        #Same idea as gameslug, if user has list with two same names, create indexed slug
        slug = slugify(self.title)                                      
        index = List.objects.filter(user=self.user, slug__startswith=slug).count()    
        if(index != 0):                                             
            slug += "-" + str(index)                                
        self.slug = slug                                              
        super(List, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.user.username + " - " + self.title
    
class ListEntry(models.Model):
    list = models.ForeignKey(List, on_delete = models.CASCADE)
    game = models.ForeignKey(Game, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = "List Entries"

    def __str__(self):
        return str(self.list) + " : " + str(self.game)