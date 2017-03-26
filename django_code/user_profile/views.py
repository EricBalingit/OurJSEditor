import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

# username was captured by the regular expression that matched the url.
# It's passed to the function automatically.
def index(request, username):
    try:
        user = User.objects.select_related('profile').get(username=username)
        return render(request, 'user_profile/index.html', {'user': user})
    except User.DoesNotExist:
        return render(request, 'user_profile/doesNotExist.html', {'username': username}, status=404)

def edit(request, username):
    if (request.method == 'POST'):
       username = request.POST.get('username', '')
       firstName = request.POST.get('displayName', '')
       bio = request.POST.get('bio', '')
       if (username == '' or re.match(r"[^A-Za-z0-9_]", username)):
           return HttpResponse('null', content_type="application/json", status=400)
       if (firstName == ''):
           firstName = username
       request.user.username = username;
       request.user.firstName = firstName;
       request.user.profile.bio = bio;
       request.user.save()
       return redirect("/user/" + username)
    else:
        try:
            user = User.objects.select_related('profile').get(username=username)
            if (user.username == request.user.username):
                return render(request, 'user_profile/edit.html')
            else:
                return render(request, 'user_profile/accessDenied.html', {'username': username}, status=403)
        except User.DoesNotExist:
            return render(request, 'user_profile/doesNotExist.html', {'username': username}, status=404)