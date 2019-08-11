from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.http import HttpResponse
import os
import json
# Create your views here.
def playAudioFile(request):
    module_dir = os.path.dirname(__file__)
    fname = os.path.join(module_dir,"myaudio.mp3")
    f = open(fname,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='audio/mp3'
    response['Content-Length'] =os.path.getsize(fname )
    return response

def show_json(request):    
    if request.method=='GET':
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir,"theData.txt")
        theFile = open(file_path,"r")
        text = theFile.read()
        theFile.close()
        text = {'data':text}
    elif request.method=='POST':
        dct = {1:"Hi", 2:"Hello",3:"Bye",4:"Tata"}
        text = {'data':dct[request.POST.get("chapterNumber", "Empty")]}

    return HttpResponse(json.dumps(text),content_type="application/json")

def show_file(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,"theData.txt")
    theFile = open(file_path,"r")
    text = theFile.read()
    theFile.close()
    return render(request, 'blog/show_file.html', {'text':text})
    
    

def post_list(request):
	posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk = pk)
	return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})