from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Bids,watchlist,Comments,Listing,Winner
from django.db.models import Max
from .help import *


def index(request):
    return render(request, "auctions/index.html" ,{
    "listings" : Listing.objects.all().filter(active = True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login/')
def newitem(request):
     if request.method =='POST':
           userid = request.user
           title = request.POST["title"]
           description = request.POST["description"]
           first_bid = request.POST["price"]
           image_url = request.POST["image_url"]
           category = request.POST["category"]
           l = Listing(title=title,description = description, category=category , first_bid = first_bid, image_url = image_url, user_id= userid)
           l.save()
           no = l.id
           return redirect('listing', item_id = no)
     return render(request, "auctions/newitem.html")
  
     
@login_required(login_url='/login/')    
def listing(request,item_id):
      userid = request.user
      item = Listing.objects.get(pk=int(item_id))
      comments = Comments.objects.filter(item_id =int(item_id))
      if check(userid.id, item.id):
            message = "Remove From watchlist"
      else:
            message = "Add to Watchlist"
      if item.active == False:
             win = Winner.objects.get(item_id = int(item_id))
             if win.user_id == userid:
                  winer = "You "
             else :
                  winer = win.user_id.username
             return render(request, "auctions/item.html",{
              "item" : item,
              "comments" : comments,
              "message" : message,
              "winner": winer
             })
      if item.user_id == userid:
           close = "Close"
           return render(request, "auctions/item.html",{
            "item" : item,
            "comments" : comments,
            "message" : message,
            "close": close
           })
      highbid = Bids.objects.filter(item_id = int(item_id))
      price = highbid.aggregate(Max('bids'))
      if price['bids__max'] == None:
            return render(request, "auctions/item.html",{
            "item" : item,
            "comments" : comments,
            "message" : message
            })
      c = str(price['bids__max'])
      list =[]
      temp =""
      for i in c: 
         list.append(i)
      for j in list:
          if j == "0":
              continue
          temp=temp+j
      print(temp)
      return render(request, "auctions/item.html",{
       "item" : item,
       "comments" : comments,
       "message" : message,
       "price" : temp
       })


@login_required(login_url='/login/')
def Commentsubmit(request):
      if request.method == 'POST':
          comment = request.POST['comment']
          userid = request.user
          itemid = int(request.POST['item_id'])
          item = Listing.objects.get(id=itemid)
          c = Comments()
          c.user_id = userid
          c.item_id = item
          c.comment = comment
          c.save()
          return redirect('listing', item_id = itemid)

@login_required(login_url='/login/')
def Bidpost(request):
      if request.method == 'POST':
          bid = request.POST['bid']
          itemid = int(request.POST['item_id'])
          item = Listing.objects.get(id=itemid)
          userid = request.user
          temp = 0
          if float(bid) > float(item.first_bid):
              if  Bids.objects.filter(item_id = itemid).count()>=1:
                   bid_obj = Bids.objects.filter(item_id = itemid)
                   for i in bid_obj:
                       if float(i.bids) > float(bid):
                          temp = 1
                   if temp == 0:
                        b = Bids()
                        b.item_id = item
                        b.user_id = userid
                        b.bids = bid
                        b.save()
                        return redirect('listing', item_id = itemid)
                   else:
                        messaget = "place the greater bid"
              else :
                   b = Bids()
                   b.item_id = item
                   b.user_id = userid
                   b.bids = bid
                   b.save()
                   return redirect('listing', item_id = itemid)
          else : 
             messaget = "Place the greater value than first bid"
          if check(userid.id, item.id):
                message = "Remove From watchlist"
          else:
                message = "Add to Watchlist"
          comments = Comments.objects.filter(item_id =int(itemid))
          return render(request, "auctions/item.html",{
       "item" : item,
       "comments" : comments,
       "message" : message,
       "messaget": messaget
       })

def category(request, category):
      lists = Listing.objects.filter(category = category)
      return render(request, "auctions/category.html",{
        "listing" : lists,
        "category" : category.capitalize()
      })


@login_required(login_url='/login/')
def watchlistpage(request):
     userid = request.user
     lists = watchlist.objects.filter(user_id = userid, watchlist=True)
     print(lists)
     return render(request, "auctions/watchlist.html",{
        "listing" : lists
     })

@login_required(login_url='/login/')
def watchlistwork(request):
     userid = request.user
     if request.method+"POST":
         itemid = int(request.POST['item_id'])
         item = Listing.objects.get(pk=int(itemid))
         if check(userid.id, item.id):
              message = remove_watchlist(userid.id, item.id)
         else :
              message = add_watchlist(userid.id, item.id)
         return redirect('listing', item_id = itemid)



@login_required(login_url='/login/')
def closelisting(request):
      if request.method == "POST":
          userid = request.user
          itemid = int(request.POST['item_id'])
          item = Listing.objects.get(pk = int(itemid))
          if item.active:
             item.active = False
             item.save()
             bid = Bids.objects.filter(item_id = itemid)
             arg = bid.order_by('-bids')[0]
             win = Winner()
             win.item_id = item
             win.user_id = arg.user_id
             win.save()
             winner = win.user_id.username
             comments = Comments.objects.filter(item_id =int(itemid))
             if check(userid.id, item.id):
               message = "Remove From watchlist"
             else:
               message = "Add to Watchlist"
             return render(request, "auctions/item.html",{
              "item" : item,
              "comments" : comments,
              "message" : message,
              "winner": winner
              })
          messaget : "This Item is Already Closed"
          return render(request, "auctions/item.html",{
              "item" : item,
              "comments" : comments,
              "message" : message,
              "messaget": messaget
          })


def closelist(request):
     return render(request, "auctions/closed.html" ,{
    "listings" : Listing.objects.all().filter(active = False)
    })


def categorylist(request):
     f = "fashion"
     t = "technology"
     to = "toy"
     s =  "sports"
     a = "automotive"
     e = "electronic"
     h = "home"
     lists = {"fashion" : f,"technology" : t,"toy" : to,"sports" : s,"automotive" : a,"electronic" : e,"home" : h}
     return render(request, "auctions/categorylist.html" ,lists )