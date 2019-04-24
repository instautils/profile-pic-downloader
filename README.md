### Profile Picture Crawler
> This script will download the profile picture of all of your follower's follower.

It's a helpful script for neural-network trainers. Run it, label it then start to train your NN.

#### Crawler

```
$ # extractor.py is written on python 2
$ INSTAGRAM_USERNAME='' INSTAGRAM_PASSWORD='' python extractor.py
```

#### Labeling script

You have to installed OpenCV in your python environment.

```
$ python supervisor_label.py
```

**Caution** This script will remove the original file.