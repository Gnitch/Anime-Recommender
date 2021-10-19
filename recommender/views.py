from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import random
import pandas as pd

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
        
        title_list = list(Anime.objects.filter(name=anime_name))
        if len(title_list) > 0 :
            context = {}
            if recommend_option == '1' :
                result = an_recommend_obj.content(anime_name)
                result = result.head(5)
                mal = list(result['MAL_ID']) 
                name = list(result['Name']) 
                score = list(result['Score'])
                genre = list(result['Genres'])
                rank = list(result['Popularity'])
                anime_list = zip(name,score,mal,genre,rank)                
                context = {'object_list':anime_list}

            else :
                num = random.randint(1,5)
                result = an_recommend_obj.hybrid(num,anime_name)
                mal = list(result['MAL_ID']) 
                name = list(result['Name']) 
                score = list(result['Score'])
                genre = list(result['Genres'])
                rank = list(result['Popularity'])
                anime_list = zip(name,score,mal,genre,rank)                
                context = {'object_list':anime_list}
            return render(request,'recommender/result.html',context)

        else :
            messages.error(request, 'Anime Not Found')             

    return redirect('/')
