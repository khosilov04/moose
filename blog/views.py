from django.shortcuts import render, redirect
from .models import Post, Contact, Comment
import requests
from django.core.paginator import Paginator

BOT_TOKEN = '6635544737:AAEhve6m4BwG_iIKMGcBSuzoD4w39J4AvG8'
CHAT_ID = '6732545531'


def home_view(request):
    posts = Post.objects.filter(is_published=True).order_by('-view_count')[:2]
    return render(request, 'index.html', {'posts': posts, 'home': 'active'})


def blog_view(request):
    data = request.GET
    cat = data.get('cat', None)
    page = data.get('page', 1)
    if cat:
        posts = Post.objects.filter(is_published=True, category_id=cat)
        return render(request, 'blog.html', {'posts': posts, 'blog': 'active'})

    posts = Post.objects.filter(is_published=True)
    page_obj = Paginator(posts, 2)

    return render(request, 'blog.html', {'blog': 'active', 'posts' : page_obj.get_page(page)})


def blog_detail_view(request, pk):
    if request.method == 'POST':
        data = request.POST
        comment = Comment.objects.create(post_id=pk, name=data['name'], email=data['email'], message=data['message'])
        comment.save()
        return redirect(f'/blog/{pk}/')
    post = Post.objects.filter(id=pk).first()
    post.view_count += 1
    post.save(update_fields=['view_count'])
    comments = Comment.objects.filter(post_id=pk)
    return render(request,'blog-single.html', {'comments': comments, 'post': post, 'blog': 'active'})


def about_view(request):
    return render(request, 'about.html', {'about': 'active'})


def contact_view(request):
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(full_name=data['name'], email=data['email'],
                                     subject=data['subject'], message=data['message'])
        obj.save()
        text = f"""
        project : MOOSE \nid : {obj.id} \nname : {obj.full_name} \nsubject : {obj.subject} \nmessage : {obj.message}
        \n timestamp : {obj.created_at}
        """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        response = requests.get(url)
        print(response)
        return redirect('/contact')
    return render(request, 'contact.html', {'contact': 'active'})
