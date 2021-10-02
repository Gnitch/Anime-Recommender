from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import random

from .Models.Recommend import AnimeRecommender
from .models import Anime

an_recommend_obj = AnimeRecommender()

def home(request):
    return render(request,'recommender/home.html')

def animeRecommend(request):
    global an_recommend_obj
    if request.method == "POST" :
        recommend_option = request.POST.get('input_option')
        anime_name = request.POST.get('input_anime')
        title_list = list(Anime.objects.filter(name__icontains=anime_name))
        if len(title_list) > 0 :
            if recommend_option == '1' :
                result = an_recommend_obj.content(anime_name).head(10)
                id_list = list(result['MAL_ID']) 
                anime_list = [ get_object_or_404(Anime,pk=mal_id)  for mal_id in id_list]
                print(anime_list)        

            else :
                num = random.randint(1,3000)
                id_list = list(an_recommend_obj.hybrid(num,anime_name)) 
                anime_list = [ get_object_or_404(Anime,pk=mal_id)  for mal_id in id_list]
                print(anime_list)  
        else :
            messages.error(request, 'Anime Not Found')             

    return redirect('/')
