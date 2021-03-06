from .models import User,Bids,watchlist,Comments,Listing
#to check the watchlist item
def main():
    return("")

def check(userid, itemid):
    if watchlist.objects.filter(user_id = userid,item_id = itemid).count() >= 1 :
         return True
    else:
         return False


def add_watchlist(user, item):
    b = watchlist()
    userid = User.objects.get(pk=user)
    itemid = Listing.objects.get(pk=item)
    b.user_id = userid
    b.item_id = itemid
    b.watchlist = True
    b.save()
    return ("Remove From Watchlist")


def remove_watchlist(userid, itemid):
    watchlist.objects.filter(user_id = userid,item_id = itemid).delete()
    return ("Add to Watchlist")

if __name__ == "__main__":
    main()