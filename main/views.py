from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Blog, Contact
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,"home.html")
def about(request):
    return render(request, "about.html")
def contact(request):
    return render(request, "contact.html")
def docontact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        subject = request.POST.get('subject')  # Add this line
        message = request.POST.get('message')
        
        contact = Contact( name=name, email=email, contact=number, subject=subject, message=message )
        contact.save()
        
        messages.success(request, "We have received your message. We will get back to you soon.")
        return render(request, "contact.html")
    
    return render(request, "contact.html")

def development(request):
    return render(request, "service_devlopment.html")
def marketing(request):
    return render(request, "sercice_marketing.html")
def branding(request):
    return render(request, "service_branding.html")
def automation(request):
    return render(request, "service_automation.html")
def institutions(request):
    return render(request, "service_institutions.html")
def blog_list_view(request):
    blog_list = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blog_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog_list.html', {
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })
def blog_detail_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    recent_posts = Blog.objects.exclude(id=blog.id).order_by('-created_at')[:5]

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'recent_posts': recent_posts
    })
