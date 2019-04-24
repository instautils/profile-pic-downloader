import os
import sys
from urllib import urlretrieve
from instagram import Instagram


def extract_image(user):
    print "Downloading user {} profile ...".format(user["username"])
    path = os.path.join('images', '{}.jpg'.format(user["username"]))
    if os.path.exists(path):
        return
    urlretrieve(user["profile_pic_url"], path)


def application(instagram):
    followers = instagram.followers(instagram.username_id)
    for follower in followers["users"]:
        users = [follower]
        targets = instagram.followers(follower["pk"])
        if not targets:
            print "Failed to fetch '{}' followers".format(follower["username"])
            continue
        elif targets["status"] != 'ok':
            print "Invalid status for '{}' followers: {}".format(
                follower["username"], targets["status"])
            continue
        else:
            users.extend(targets["users"])

        for user in users:
            extract_image(user)


if __name__ == "__main__":
    instagram = Instagram(
        username=os.getenv('INSTAGRAM_USERNAME'),
        password=os.getenv('INSTAGRAM_PASSWORD'),
    )
    if not instagram.login():
        print "Couldn't sign-in into Instagram."
        sys.exit(1)
    
    if not os.path.exists('images'):
        os.mkdir('images')
    
    try:
        application(instagram)
    except BaseException as e:
        print "Exception on {}".format(e)

    instagram.logout()
