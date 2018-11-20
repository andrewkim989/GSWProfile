from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from time import gmtime, strftime

from .models import *

def home(request):
    if not request.session.keys():
        request.session['login'] = 'logout'
    context = {
        "players": Player.objects.all(),
        "coaches": Coach.objects.all(),
        "others": Other.objects.all(),
    }
    return render (request, "home.html", context)

def signin(request):
    if request.session['login'] == 'login':
        return redirect('/profile')
    else:
        return render(request, "signin.html")

def reg_process(request):
    if request.method == 'POST':
        errors = User.objects.register_validate(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'register')
            return redirect('/signin')
        else: 
            request.session['login'] = 'login'
            p = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = request.POST['first_name'],
            last_name = request.POST['last_name'], email = request.POST['email'],
            password = p)

            request.session['id'] = user.id
            return redirect('/profile')

def log_process(request):
    if request.method == 'POST':
        errors = User.objects.login_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'login')
            return redirect('/signin')
        else:
            request.session['login'] = 'login'
            user = User.objects.filter(email = request.POST['email'])[0]
            request.session['id'] = user.id

            return redirect('/profile')

def profile(request):
    if request.session['login'] == 'logout':
        return redirect('/signin')
    else: 
        user = User.objects.get(id = request.session['id'])
        all_users = User.objects.all()
        activities = Activity.objects.all().order_by('-id')[:8]
        info = {
            "u": user,
            "users": all_users,
            "activities": activities,
        }
        return render(request, "profile.html", info)

def logout(request):
    request.session['login'] = 'logout'
    return redirect('/')

def addplayer(request):
    if request.session['login'] == 'logout':
        return redirect('/oops')
    else: 
        return render(request, "addplayer.html")

def addplayer_process(request):
    if request.method == 'POST':
        errors = User.objects.player_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'player')
            return redirect('/addplayer')
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            user = User.objects.get(id = request.session['id'])
            player = Player.objects.create(name = request.POST['name'],
            image = request.POST['image'], birth_month = request.POST['birth_month'],
            birth_day = request.POST['birth_day'], birth_year = request.POST['birth_year'],
            height_foot = request.POST['height_foot'], height_inches = request.POST['height_inches'],
            weight = request.POST['weight'], position = request.POST['position'],
            previous_teams = request.POST['previous_teams'], college = request.POST['college'],
            draft = request.POST['draft'], jersey = request.POST['jersey'],
            playfrom = request.POST['playfrom'], playto = request.POST['playto'],
            info = request.POST['info'], description = request.POST['description'],
            description2 = request.POST['description2'], description3 = request.POST['description3'],
            player_creator = user)
            Activity.objects.create(activity = 'Created the following page: '
            + str(player.name) + ' (' + str(t) + ')', act = user)
            return redirect('/player/' + str(player.id))
    
def player(request, num):
    a = 0
    player = Player.objects.get(id = num)
    comments = Comment.objects.filter(player_commented = player)
    for c in comments:
        a = a + int(c.replied_comment.count())
    a = a + int(comments.count())
    context = {
         "player": player,
         "comments": comments,
         "all": a
    }
    return render(request, "player.html", context)

def editplayer(request, num):
    if request.session['login'] == 'logout':
        return redirect('/oops')
    else:
        player = Player.objects.get(id = num)
        context = {
            "player": player
        }
        return render(request, "editplayer.html", context)

def editplayer_process(request, num):
    player = Player.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.player_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'player')
            return redirect('/editplayer/' + str(player.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            user = User.objects.get(id = request.session['id'])
            player.name = request.POST['name']
            player.image = request.POST['image']
            player.birth_month = request.POST['birth_month']
            player.birth_day = request.POST['birth_day']
            player.birth_year = request.POST['birth_year']
            player.height_foot = request.POST['height_foot']
            player.height_inches = request.POST['height_inches']
            player.weight = request.POST['weight']
            player.position = request.POST['position']
            player.previous_teams = request.POST['previous_teams']
            player.college = request.POST['college']
            player.draft = request.POST['draft']
            player.jersey = request.POST['jersey']
            player.playfrom = request.POST['playfrom']
            player.playto = request.POST['playto']
            player.info = request.POST['info']
            player.description = request.POST['description']
            player.description2 = request.POST['description2']
            player.description3 = request.POST['description3']
            player.save()
            Activity.objects.create(activity = 'Edited the following page: '
            + str(player.name) + ' (' + str(t) + ')', act = user)
            return redirect('/player/' + str(player.id))

def comment_player(request, num):
    player = Player.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.comment_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'comment')
            return redirect('/player/' + str(player.id))
        else:
            user = User.objects.get(id = request.session['id'])
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            commenter = User.objects.get(id = request.session['id'])
            c = Comment.objects.create(comment = request.POST['comment'], commenter = commenter)
            player.player_comments.add(c)
            Activity.objects.create(activity = 'Commented on the following page: '
            + str(player.name) + ' (' + str(t) + ')', act = user)
            return redirect('/player/' + str(player.id))

def reply_player(request, num, num2):
    player = Player.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.reply_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'reply')
            return redirect('/player/' + str(player.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            post = Comment.objects.get(id = num2)
            reply_user = User.objects.get(id = request.session['id'])
            Reply.objects.create(reply = request.POST['reply'], replier = reply_user, comment = post)
            Activity.objects.create(activity = 'Replied to a user on the following page: '
            + str(player.name) + ' (' + str(t) + ')', act = reply_user)
            return redirect('/player/' + str(player.id))

def addcoach(request):
    if request.session['login'] == 'logout':
        return redirect('/oops')
    else:
        return render(request, "addcoach.html")

def addcoach_process(request):
    if request.method == 'POST':
        errors = User.objects.coach_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'coach')
            return redirect('/addcoach')
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            user = User.objects.get(id = request.session['id'])
            coach = Coach.objects.create(name = request.POST['name'],
            image = request.POST['image'], birth_month = request.POST['birth_month'],
            birth_day = request.POST['birth_day'], birth_year = request.POST['birth_year'],
            height_foot = request.POST['height_foot'], height_inches = request.POST['height_inches'],
            weight = request.POST['weight'], position = request.POST['position'],
            teams_played = request.POST['teams_played'],
            teams_coached = request.POST['teams_coached'], college = request.POST['college'],
            draft = request.POST['draft'], playfrom = request.POST['playfrom'],
            playto = request.POST['playto'], coachfrom = request.POST['coachfrom'],
            coachto = request.POST['coachto'], coach_position = request.POST['coach_position'],
            info = request.POST['info'], description = request.POST['description'],
            description2 = request.POST['description2'],
            description3 = request.POST['description3'], coach_creator = user)
            Activity.objects.create(activity = 'Created the following page: '
            + str(coach.name) + ' (' + str(t) + ')', act = user)
            return redirect('/coach/' + str(coach.id))

def coach(request, num):
    a = 0
    coach = Coach.objects.get(id = num)
    comments = Comment.objects.filter(coach_commented = coach)
    for c in comments:
        a = a + int(c.replied_comment.count())
    a = a + int(comments.count())
    context = {
        "coach": coach,
        "comments": comments,
        "all": a
    }
    return render(request, "coach.html", context)

def editcoach(request, num):
    if request.session['login'] == 'logout':
        return redirect('/oops')
    else:
        coach = Coach.objects.get(id = num)
        context = {
            "coach": coach
        }
        return render(request, "editcoach.html", context)

def editcoach_process(request, num):
    coach = Coach.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.coach_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'coach')
            return redirect('/editcoach/' + str(coach.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            user = User.objects.get(id = request.session['id'])
            coach.name = request.POST['name']
            coach.image = request.POST['image']
            coach.birth_month = request.POST['birth_month']
            coach.birth_day = request.POST['birth_day']
            coach.birth_year = request.POST['birth_year']
            coach.height_foot = request.POST['height_foot']
            coach.height_inches = request.POST['height_inches']
            coach.weight = request.POST['weight']
            coach.position = request.POST['position']
            coach.teams_played = request.POST['teams_played']
            coach.teams_coached = request.POST['teams_coached']
            coach.college = request.POST['college']
            coach.draft = request.POST['draft']
            coach.playfrom = request.POST['playfrom']
            coach.playto = request.POST['playto']
            coach.coachfrom = request.POST['coachfrom']
            coach.coachto = request.POST['coachto']
            coach.coach_position = request.POST['coach_position']
            coach.info = request.POST['info']
            coach.description = request.POST['description']
            coach.description2 = request.POST['description2']
            coach.description3 = request.POST['description3']
            coach.save()
            Activity.objects.create(activity = 'Edited the following page: '
            + str(coach.name) + ' (' + str(t) + ')', act = user)
            return redirect('/coach/' + str(coach.id))

def comment_coach(request, num):
    coach = Coach.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.comment_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'comment')
            return redirect('/coach/' + str(coach.id))
        else:
            user = User.objects.get(id = request.session['id'])
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            commenter = User.objects.get(id = request.session['id'])
            c = Comment.objects.create(comment = request.POST['comment'], commenter = commenter)
            coach.coach_comments.add(c)
            Activity.objects.create(activity = 'Commented on the following page: '
            + str(coach.name) + ' (' + str(t) + ')', act = user)
            return redirect('/coach/' + str(coach.id))

def reply_coach(request, num, num2):
    coach = Coach.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.reply_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'reply')
            return redirect('/coach/' + str(coach.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            post = Comment.objects.get(id = num2)
            reply_user = User.objects.get(id = request.session['id'])
            Reply.objects.create(reply = request.POST['reply'], replier = reply_user, comment = post)
            Activity.objects.create(activity = 'Replied to a user on the following page: '
            + str(coach.name) + ' (' + str(t) + ')', act = reply_user)
            return redirect('/coach/' + str(coach.id))

def addother(request):
    if request.session['login'] == 'logout':
        return redirect('/oops')
    else:
        return render(request, "addother.html")

def addother_process(request):
    if request.method == 'POST':
        errors = User.objects.other_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'other')
            return redirect('/addother')
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            user = User.objects.get(id = request.session['id'])
            other = Other.objects.create(name = request.POST['name'],
            image = request.POST['image'], birth_month = request.POST['birth_month'],
            birth_day = request.POST['birth_day'], birth_year = request.POST['birth_year'],
            height_foot = request.POST['height_foot'], height_inches = request.POST['height_inches'],
            weight = request.POST['weight'], position = request.POST['position'],
            info = request.POST['info'], description = request.POST['description'],
            description2 = request.POST['description2'],
            description3 = request.POST['description3'], other_creator = user)
            Activity.objects.create(activity = 'Created the following page: '
            + str(other.name) + ' (' + str(t) + ')', act = user)
            return redirect('/other/' + str(other.id))

def other(request, num):
    a = 0
    o = Other.objects.get(id = num)
    comments = Comment.objects.filter(other_commented = o)
    for c in comments:
        a = a + int(c.replied_comment.count())
    a = a + int(comments.count())
    context = {
        "other": o,
        "comments": comments,
        "all": a
    }
    return render(request, "other.html", context)

def editother(request, num):
    if request.session['login'] == 'logout':
        return redirect('/oops')
    else:
        other = Other.objects.get(id = num)
        context = {
            "other": other
        }
        return render(request, "editother.html", context)

def editother_process(request, num):
    other = Other.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.other_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'other')
            return redirect('/editother/' + str(other.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            user = User.objects.get(id = request.session['id'])
            other.name = request.POST['name']
            other.image = request.POST['image']
            other.birth_month = request.POST['birth_month']
            other.birth_day = request.POST['birth_day']
            other.birth_year = request.POST['birth_year']
            other.height_foot = request.POST['height_foot']
            other.height_inches = request.POST['height_inches']
            other.weight = request.POST['weight']
            other.position = request.POST['position']
            other.info = request.POST['info']
            other.description = request.POST['description']
            other.description2 = request.POST['description2']
            other.description3 = request.POST['description3']
            other.save()
            Activity.objects.create(activity = 'Edited the following page: '
            + str(other.name) + ' (' + str(t) + ')', act = user)
            return redirect('/other/' + str(other.id))

def comment_other(request, num):
    other = Other.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.comment_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'comment')
            return redirect('/other/' + str(other.id))
        else:
            user = User.objects.get(id = request.session['id'])
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            commenter = User.objects.get(id = request.session['id'])
            c = Comment.objects.create(comment = request.POST['comment'], commenter = commenter)
            other.other_comments.add(c)
            Activity.objects.create(activity = 'Commented on the following page: '
            + str(other.name) + ' (' + str(t) + ')', act = user)
            return redirect('/other/' + str(other.id))

def reply_other(request, num, num2):
    other = Other.objects.get(id = num)
    if request.method == 'POST':
        errors = User.objects.reply_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'reply')
            return redirect('/other/' + str(other.id))
        else:
            t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
            post = Comment.objects.get(id = num2)
            reply_user = User.objects.get(id = request.session['id'])
            Reply.objects.create(reply = request.POST['reply'], replier = reply_user, comment = post)
            Activity.objects.create(activity = 'Replied to a user on the following page: '
            + str(other.name) + ' (' + str(t) + ')', act = reply_user)
            return redirect('/other/' + str(other.id))

def player_commentlike(request, num, num2):
    if request.session['login'] == 'logout':
        return redirect('/signin')
    else:
        t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
        player = Player.objects.get(id = num)
        user = User.objects.get(id = request.session['id'])
        c = Comment.objects.get(id = num2)
        exists = user.liked_comment.filter(id = c.id)
        print(exists)
        if exists: 
            return redirect('/player/' + num)
        else:
            user.liked_comment.add(c)
            Activity.objects.create(activity = 'Liked a comment on the following page: '
            + str(player.name) + ' (' + str(t) + ')', act = user)
            return redirect('/player/' + num)

def player_replylike(request, num, num2):
    if request.session['login'] == 'logout':
        return redirect('/signin')
    else:
        t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
        player = Player.objects.get(id = num)
        user = User.objects.get(id = request.session['id'])
        r = Reply.objects.get(id = num2)
        exists = user.liked_reply.filter(id = r.id)
        if exists:
            return redirect('/player/' + num)
        else:
            user.liked_reply.add(r)
            Activity.objects.create(activity = 'Liked a reply on the following page: '
            + str(player.name) + ' (' + str(t) + ')', act = user)
            return redirect('/player/' + num)

def coach_commentlike(request, num, num2):
    if request.session['login'] == 'logout':
        return redirect('/signin')
    else:
        t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
        coach = Coach.objects.get(id = num)
        user = User.objects.get(id = request.session['id'])
        c = Comment.objects.get(id = num2)
        exists = user.liked_comment.filter(id = c.id)
        if exists: 
            return redirect('/coach/' + num)
        else:
            user.liked_comment.add(c)
            Activity.objects.create(activity = 'Liked a comment on the following page: '
            + str(coach.name) + ' (' + str(t) + ')', act = user)
            return redirect('/coach/' + num)

def coach_replylike(request, num, num2):
    if request.session['login'] == 'logout':
        return redirect('/signin')
    else:
        t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
        coach = Coach.objects.get(id = num)
        user = User.objects.get(id = request.session['id'])
        r = Reply.objects.get(id = num2)
        exists = user.liked_reply.filter(id = r.id)
        if exists:
            return redirect('/coach/' + num)
        else:
            user.liked_reply.add(r)
            Activity.objects.create(activity = 'Liked a reply on the following page: '
            + str(coach.name) + ' (' + str(t) + ')', act = user)
            return redirect('/coach/' + num)

def other_commentlike(request, num, num2):
    if request.session['login'] == 'logout':
        return redirect('/signin')
    else:
        t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
        other = Other.objects.get(id = num)
        user = User.objects.get(id = request.session['id'])
        c = Comment.objects.get(id = num2)
        exists = user.liked_comment.filter(id = c.id)
        if exists: 
            return redirect('/other/' + num)
        else:
            user.liked_comment.add(c)
            Activity.objects.create(activity = 'Liked a comment on the following page: '
            + str(other.name) + ' (' + str(t) + ')', act = user)
            return redirect('/other/' + num)

def other_replylike(request, num, num2):
    if request.session['login'] == 'logout':
        return redirect('/signin')
    else:
        t = strftime("%B/%d/%Y, %I:%M %p", gmtime())
        other = Other.objects.get(id = num)
        user = User.objects.get(id = request.session['id'])
        r = Reply.objects.get(id = num2)
        exists = user.liked_reply.filter(id = r.id)
        if exists:
            return redirect('/other/' + num)
        else:
            user.liked_reply.add(r)
            Activity.objects.create(activity = 'Liked a reply on the following page: '
            + str(other.name) + ' (' + str(t) + ')', act = user)
            return redirect('/other/' + num)

def userprofile (request, num):
    u = User.objects.get(id = num)
    activities = Activity.objects.filter(act = u)
    context = {
        "u": u,
        "activities": activities,
    }
    return render(request, "user.html", context)

def edit(request):
    if request.session['login'] == 'logout':
        return redirect('/oops')
    else:
        user = User.objects.get(id = request.session['id'])
        context = {
            "user": user
        }
        return render (request, "edit.html", context)

def edit_process(request):
    user = User.objects.get(id = request.session['id'])

    if request.method == 'POST':
        errors = User.objects.edit_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'edit')
            return redirect('/editprofile')
        else:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
        return redirect("/profile")

def oops(request):
    return render(request, "oops.html")

# http://13.59.234.218/

'''
purplesmart@eq.net Twily123
glimglam@eq.net Glimmy25
20cooler@eq.net Dashie20
partypony@eq.net Pinkie30
nightprincess@eq.net Moon0204
sunprincess@eq.net Sunny111
'''