from django.shortcuts import render,redirect
from markdown2 import Markdown

from . import util
import random

def converter(title):
    # this function convert HTML to Markdown
    markdowner = Markdown()
    folder = util.get_entry(title)
    
    if folder is None:
        return ""
    else:
        return markdowner.convert(folder)

    
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    #this function handle /wiki/<str>/
    converted_html = converter(title)
    # checking if the title existed in entry list 
    if converted_html == "":
        return render(request, "encyclopedia/error.html",{
            'error_message':"Sorry i can't found it for you"
        })

    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": converted_html
        })


def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        entries = util.list_entries()

        # Check if there's an exact match (case-insensitive)
        matching_entry = next((entry for entry in entries if entry.lower() == query.lower()), None)

        if matching_entry is not None:
        # If an exact match is found, redirect to the entry page
            return redirect('entry_page', title=matching_entry)
        else:
        # If no exact match, find entries containing the query substring (case-insensitive)
            matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, 'encyclopedia/search.html', {'recomendation': matching_entries})


def new(request):
    if request.method == "POST":
        # get the content from the form
        title= request.POST["title"]
        content = request.POST["newpage"]
        existed_title= util.get_entry(title)
        if existed_title is not None: #check if the page already existed by comparing title
            return render(request,'encyclopedia/error.html',{
                'error_message': 'Page already existed'
            })
        else:
            # save the entry and convert the html to markdown
            util.save_entry(title,content)
            html_content= converter(title)
            return render(request,'encyclopedia/entry.html',{
                'title': title,
                'content': html_content,
            })
       
    
    else:
         return render(request,'encyclopedia/new.html')


def edit(request):
    if request.method == 'POST':
        # get the content from the form
        title= request.POST["title"]
        # get the entry that already existed
        content= util.get_entry(title)
        return render(request,'encyclopedia/edit.html',{
            'title': title,
            'content': content,
        })
    

def saved(request):
    
    if request.method == 'POST':
        # Get the modified content from the form data
        title= request.POST["title"]
        modified_content = request.POST["content"]
        
        # Save the modified content as an updated version of the entry
        util.save_entry(title, modified_content)
        # convert to markdown
        html_content= converter(title)
        return render(request,'encyclopedia/entry.html',{
                'title': title,
                'content': html_content,
            })
    

def randomize(request):
      # Retrieve a list of all encyclopedia entries
    entries = util.list_entries()
    # randomize thee encyclopedia
    random_entry = random.choice(entries)
    #convert to markdown
    html_content= converter(random_entry)

    return render(request,'encyclopedia/entry.html',{
        'title': random_entry,
        'content': html_content
    })

    

           