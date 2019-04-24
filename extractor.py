import os
import sys
import requests
from tqdm import tqdm
from instagram import Instagram


def extract_image(user):
    path = os.path.join('images', '{}.jpg'.format(user["username"]))
    if os.path.exists(path):
        return
    try:
        r = requests.get(user["profile_pic_url"], allow_redirects=True)
        with open(path, 'wb') as handler:
            handler.write(r.content)
    except requests.exceptions.RequestException:
        pass


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

        for user in tqdm(users):
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
