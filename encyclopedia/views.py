from django.shortcuts import render
from django.http import HttpResponse

from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
# Returns a dic of the title entries in lower case with its original title
# for using get_entry
def get_mapping():
    return { i.lower():i for i in util.list_entries() }

def entry(request, title):
    titles = get_mapping()
    file = titles.get(title.lower(), None)
    entry = util.get_entry(file)
    if entry:
        markdowner = Markdown()
        entry = markdowner.convert(entry)
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
        titles = get_mapping()
        file = titles.get(entry_name.lower(), None)
        entry = util.get_entry(file)
        if entry:
            markdowner = Markdown()
            entry = markdowner.convert(entry)
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
        n_entry = request.POST['new-page']
        titles = get_mapping()
        file = titles.get(title.lower(), None)
        entry = util.get_entry(file)
        if not entry:
            util.save_entry(title, n_entry)
            markdowner = Markdown()
            entry = markdowner.convert(n_entry)
            return render(request, "encyclopedia/entry.html", {
                'title': title,
                'entry':  entry
            })
        else:
            return render(request, "encyclopedia/error.html", {
                'error': "New page already exist."
            })

def edit(request):
    print(request.GET['title'])
    print(request.POST['entry_title'])
    title = request.GET['title']
    titles = get_mapping()
    file = titles.get(title.lower(), None)
    entry = util.get_entry(file)
    if request.method == 'POST':
        entry_title = request.POST['entry_title']
        entry = util.save_entry(file, request.POST['content'])
        return render(request, "encyclopedia/entry.html", {
            'title': entry_title,
            'content': entry,
        })

    return render(request, "encyclopedia/edit.html", {
        'title': file,
        'content': entry
    })
 