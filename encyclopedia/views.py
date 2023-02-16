from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import util
from markdown2 import Markdown
from random import choice
from django.urls import reverse


# Returns a dic of the title entries in lower case with its original title
# for using get_entry
def get_mapping():
    return { i.lower() : i for i in util.list_entries() }

def find_entry(title):
    titles = get_mapping()
    file = titles.get(title.lower(), None)
    return file

def convert_to_html(entry):
    markdowner = Markdown()
    entry = markdowner.convert(entry)
    return entry

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    file = find_entry(title)
    entry = util.get_entry(file)
    if entry:
        entry = convert_to_html(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": file,
            "entry": entry
        })
    return render(request, "encyclopedia/error.html", {
        "error": f"Entry \"{title}\" does not exist."
    })

def search(request):
    if request.method == "POST":
        entry_name = request.POST['q']
        file = find_entry(entry_name)
        entry = util.get_entry(file)
        if entry:
            entry = convert_to_html(entry)
            return render(request, "encyclopedia/entry.html", {
            "title": entry_name,
            "entry": entry
            })
        options = []
        all_entries = util.list_entries()
        for entr in all_entries:
            if entry_name.lower() in entr.lower():
                options.append(entr)
        # Render error page if search does not match with anything
        if len(options) == 0:
            return render(request, "encyclopedia/error.html", {
                "error": f"\"{entry_name}\" does not match."
            })
        return render(request, "encyclopedia/search.html", {
            "options": options
        })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    elif request.method == "POST":
        title = request.POST['title']
        if not title:
            return render(request, "encyclopedia/error.html", {
                'error': "New page cannot be empty."
            })
        n_entry = request.POST['new-page']
        file = find_entry(n_entry)
        entry = util.get_entry(file)
        if not entry:
            util.save_entry(title, n_entry)
            entry = convert_to_html(n_entry)
            return render(request, "encyclopedia/entry.html", {
                'title': title,
                'entry':  entry
            })
        else:
            return render(request, "encyclopedia/error.html", {
                'error': "New page already exist."
            })

def edit(request):
    if request.method == 'POST':
        entry_title = request.POST['entry_title']
        file = find_entry(entry_title)
        entry = util.get_entry(file)
        entry = util.save_entry(file, request.POST['content'])
        return redirect('encyclopedia:entry', title=file)
    else:
        title = request.GET['title']
        file = find_entry(title)
        entry = util.get_entry(file)
        return render(request, "encyclopedia/edit.html", {
            'title': request.GET['title'],
            'content': entry
        })

def random(request):
    entries = util.list_entries()
    random_title = choice(entries)
    return redirect('encyclopedia:entry', random_title)
