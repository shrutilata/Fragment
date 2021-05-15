from urlshortener import urls
from django.shortcuts import render,redirect
# get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShortUrl
import random,string
from .form import UpdateUrl


def dashboard(request):
    userr = request.user
    urls = ShortUrl.objects.filter(user = userr)
    return render(request, 'dashboard.html', {'url' : urls})

def random_gen():
    return''.join(random.choice(string.ascii_lowercase) for _ in range(6))


@login_required(login_url='/login/')
def generate(request):
    if request.method == "POST":
        if request.POST['original'] and request.POST['short']:
            userr = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = ShortUrl.objects.filter(short_query = short)
            if not check:
                newurl = ShortUrl(
                    user = userr,
                    original_url = original,
                    short_query = short,
                )
                newurl.save()
                return redirect(dashboard)
            else:
                messages.error(request, "Already exists")
                return redirect(dashboard)
        elif request.POST['original']:
            userr = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = random_gen()
                check = ShortUrl.objects.filter(short_query = short)
                if not check:
                    newurl = ShortUrl(
                        user = userr,
                        original_url = original,
                        short_query = short,
                    )
                    newurl.save()
                    return redirect(dashboard)
                else:
                    continue
        else:
            messages.error(request, "Empty Fields")
            return redirect(dashboard)
    else:
        return redirect('/dashboard')

        
def home(request, query=None):
    urls = ShortUrl.objects.all()
    if not query or query is None:
        return render(request, 'home.html',{'urls':urls})
    else:
        try:
            check = ShortUrl.objects.get(short_query = query)
            check.visits = check.visits + 1
            check.save()
            url_to_redirect = check.original_url
            return redirect(url_to_redirect)
        except ShortUrl.DoesNotExist:
             return render(request, 'home.html', {'error' : 'Url does not exist.'})

    



@login_required(login_url='/login/')
def delete_url(request):
    if request.method == "POST":
        short = request.POST['delete']
        try:
            check = ShortUrl.objects.filter(short_query=short)
            check.delete()
            return redirect(dashboard)
        except ShortUrl.DoesNotExist:
            return redirect(home)
    else:
        return redirect(home)

# @login_required(login_url='/login/')
# def url_update(request):
#     obj=get_object_or_404(ShortUrl, id=id)
#     if request.method == 'POST':
#         form = UpdateUrl(request.POST, instance=obj)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/")
#     else:
#         form = UpdateUrl()
#     return render(request, "update.html", {"form": form})

