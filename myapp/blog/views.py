from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Post, AboutUs
from .forms import ContactForm
from .models import Contact


# Create your views here.
# static demo data
# posts = [
#     {'post_id':1, 'title':'Win-Win', 'content': 'All Sports Available'},
#     {'post_id':2, 'title':'Tech Solutions', 'content': 'Find Solutions Here'},
#     {'post_id':3, 'title':'Future Gen', 'content': 'Finding Engineers'},
#     {'post_id':4, 'title':'Play-Zone', 'content': 'Kids Only'},
#     {'post_id':5, 'title':'Faschion Hub', 'content': 'All Design Available'},
#     {'post_id':6, 'title':'Movies', 'content': 'Exploring Movies'}
    
# ]  
def index(request):
    blog_title = 'Latest Blog'
    # return HttpResponse("hello world")
    #getting data from relational mode
    posts = Post.objects.all()        #object relational Mapping
    return render(request,"blog/index.html", {"posts": posts, 'blog_title': blog_title})

def detail(request,post_id):
    # return HttpResponse(f'your viewing post details page and the id is {post_id}')
    #static data
    # post = next((post for post in posts if ['post_id' == post_id]),None)
    # getting data from post model
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponse("post not found")
    return render(request,"blog/detail.html",{"post":post})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("This is My new URL")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #manual save to db
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            success_message = 'Your message has been saved in the database!'
            return render(request, 'blog/contact.html', {
                'form': ContactForm(), #reset form
                'success_message' : success_message
            })
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form' : form})

def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here."
    else:
        about_content = about_content.content

    return render(request, 'blog/about.html', {'about_content':about_content})
