from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.http import HttpResponse
import os
import json
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
stopword = stopwords.words("english")

# Create your views here.
def mamax(l):
    k=None
    mama=0
    for i in l:
        if i[-1]>mama:
            mama = i[-1]
            k = i[0]
    if mama==0:
        return None
    return k    

def score(fq,swt):
    fq = fq.lower()
    fwt = nltk.word_tokenize(fq)
    fwt = [word for word in fwt if word not in stopword]
    fwt = set(filter(lambda x:x.isalnum(), fwt))
    return len(swt.intersection(fwt))
    
def searchfaq(request):    
    sq = request.GET.get('search','0')
    if sq=='0':
        return HttpResponse(json.dumps({'data':"Sorry! Couldn't find the question!"}),content_type="application/json")
    sq = sq.replace("%20"," ")
    sq = sq.lower()    
    swt = nltk.word_tokenize(sq)
    swt = [word for word in swt if word not in stopword]
    swt = set(filter(lambda x:x.isalnum(), swt))

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,"faq.txt")
    theFile = open(file_path,"r")
    js = theFile.read().strip()
    theFile.close()

    dct = json.loads(js)
    qscore = [(k,score(k,swt)) for k in dct]
    repP= "Closest question found is "
    repQ=mamax(qscore)

    if repQ==None:
        return HttpResponse(json.dumps({'data':"Sorry! Couldn't find the question!"}),content_type="application/json")
    repR=". "+dct[repQ]
    answer = repP+repQ+repR    
    
    return HttpResponse(json.dumps({'data':answer}),content_type="application/json")
def playStatistics(request):

    module_dir = os.path.dirname(__file__)
    fname = os.path.join(module_dir,"statistics.mp3")
    f = open(fname,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='audio/mp3'
    response['Content-Length'] =os.path.getsize(fname )
    return response

def playSentiment(request):

    module_dir = os.path.dirname(__file__)
    fname = os.path.join(module_dir,"sentiment.mp3")
    f = open(fname,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='audio/mp3'
    response['Content-Length'] =os.path.getsize(fname )
    return response

def playBigdata(request):

    module_dir = os.path.dirname(__file__)
    fname = os.path.join(module_dir,"bigdata.mp3")
    f = open(fname,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='audio/mp3'
    response['Content-Length'] =os.path.getsize(fname )
    return response

def playAudioFile(request):

    module_dir = os.path.dirname(__file__)
    fname = os.path.join(module_dir,"meetings.mp3")
    f = open(fname,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='audio/mp3'
    response['Content-Length'] =os.path.getsize(fname )
    return response

def show_json(request):
    k = request.GET.get('chapterNumber','0')    
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir,"theData.txt")
    theFile = open(file_path,"r")
    js = theFile.read().strip()
    dct = json.loads(js)
    text = dct.get(k,"Invalid Chapter Number")
    theFile.close()
    return HttpResponse(json.dumps({'data':text}),content_type="application/json")

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
