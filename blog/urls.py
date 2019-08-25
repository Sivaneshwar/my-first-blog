from django.urls import path
from . import views

urlpatterns = [
	path('faq/',views.searchfaq, name = 'searchfaq'),
	path('sentiments/',views.playSentiment, name = 'playSentiment'),
	path('statistics/',views.playStatistics, name = 'playStatistics'),
	path('bigdata/',views.playBigdata, name = 'playBigdata'),
	path('audio/',views.playAudioFile, name = 'playAudioFile'),
	path('',views.post_list, name = 'post_list'),
	path('showFile/',views.show_file, name = 'show_file'),
	path('showJson',views.show_json, name = 'show_json'),
	path('post/<int:pk>/', views.post_detail, name = 'post_detail'),
	path('post/new',  views.post_new, name = 'post_new'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

]