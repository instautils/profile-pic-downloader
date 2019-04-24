import os
import sys
import requests
import time
from tqdm import tqdm
from instagram import Instagram
import multiprocessing as multiprocessing


def parallel_downloader(input_list):
    processes = [
        multiprocessing.Process(
            target=extract_image,
            args=(user,),
        ) for user in input_list
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()


def extract_image(user):
    path = os.path.join('images', '{}.jpg'.format(user["username"]))
    if os.path.exists(path):
        return
    try:
        r = requests.get(user["profile_pic_url"], allow_redirects=True)
        with open(path, 'wb') as handler:
            handler.write(r.content)
    except requests.exceptions.RequestException:
        return


def application(instagram):
    followers = instagram.followers(instagram.username_id)
    for follower in tqdm(followers["users"]):
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

        parallel_downloader(users)
        time.sleep(1)


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
