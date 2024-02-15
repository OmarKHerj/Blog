from django.urls import path

from encyclopedia import views

urlpatterns = [

    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry_page, name="entry_page"),
    path("search/", views.search, name="search"),
    path("new/",views.new,name="new"),
    path("edit/",views.edit,name="edit"),
    path("saved/",views.saved,name="saved"),
    path("randomize/",views.randomize,name="randomize"),
    


    
]
