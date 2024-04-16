from django.shortcuts import render

from . import util
from .util import list_entries, save_entry
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search_page(request) :
    query = request.GET.get('q', '')
    if query : 
        entries = list_entries()
        searching_entries = [entry for entry in entries if query.lower() in entry.lower()]

        if len(searching_entries) == 0 :
            return render(request, 'encyclopedia/404.html', {
                'message': 'No entries is found.'
            })
        elif len(searching_entries) == 1 and searching_entries[0].lower() == query.lower() :
            return HttpResponseRedirect(reverse('entry_page', args=[searching_entries[0]]))
        else :
            return render(request, 'encyclopedia/search_page.html', {
                'entries': searching_entries,
                'query': query
            })
    else :
        return HttpResponseRedirect(reverse('index'))

def entry_page(request, name):
    content = util.get_entry(name)  
    print(content)
    if content is not None:
        return render(request, 'encyclopedia/page_info.html', {'entry_name': name, 'entry_content': content})
    else:
        return render(request, 'encyclopedia/404.html', {'name': name})

def new_page(request) :
    if request.method == "POST" :
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content :
            existing_entries = list_entries()
            if title in existing_entries :
                return render(request, 'encyclopedia/409.html')
            else :
                save_entry(title, content)
                return redirect('../')
        else :
            return render(request, 'encyclopedia/new_page.html', {
                'Error': "Title and Content are both required."
            })
    else :
        return render(request, 'encyclopedia/new_page.html')

def edit_page(request, name) :
    if request.method == 'GET' :
        content = util.get_entry(name)
        if content is not None :
            return render(request, 'encyclopedia/edit_page.html', {'entry_name': name, 'entry_content': content})
        else:
            return render(request, 'encyclopedia/404.html', {'entry_name': name})
    elif request.method == 'POST':
        new_content = request.POST.get('content')
        util.save_entry(name, new_content)
        content = util.get_entry(name)
        return render(request, 'encyclopedia/page_info.html', {'entry_name': name, 'entry_content': content})

def random_page(request) :
    entries = list_entries()
    random_page = random.choice(entries)
    return HttpResponseRedirect(reverse('entry_page', args=[random_page]))
