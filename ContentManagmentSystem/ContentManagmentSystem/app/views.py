"""
Definition of views.
"""
from django.shortcuts import redirect
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.forms import TextEditorForm
from app.models import TextEditor

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def textbox(request):
    form = TextEditorForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            textinput = "asdklfj" #form.save(commit=False)
            #textinput.save()
            TextEditor.textoutput = textinput
            return render(request,
                'app/output.html',
                {
                    'title':'Output',
                    'message':'Your output page.',
                    'year':datetime.now().year,
                    'output': TextEditor
                })
            #return redirect("home")
    #        return redirect(request, "app/index.html", {"alert": "dsklfj"})
    #        return redirect(
    #    request,
    #    'app/about.html',
    #    {
    #        'title':'About',
    #        'message':'Your application description page.',
    #        'year':datetime.now().year,
    #    }
    #)
    else:
        return render(request, "app/textbox.html", {"form": form})


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })

def output(request):
    """Renders the output page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/output.html',
        {
            'title':'Output',
            'message':'Your output page.',
            'year':datetime.now().year,
        })
