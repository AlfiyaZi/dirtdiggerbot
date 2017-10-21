import operator
import os
import pprint
import re

import praw

import config as cfg

reddit = praw.Reddit(client_id=cfg.client_id,
                     client_secret=cfg.client_secret,
                     password=cfg.password,
                     user_agent=cfg.user_agent,
                     username=cfg.username)

subreddit = reddit.subreddit(cfg.test_sub)


def find_top_submissions(user):
    response = "\n\n**Top submissions this past year**:\n\nSubreddit | Link\n:-- | :-:"
    for sub in reddit.redditor(user).submissions.top('year', limit=5):
        # pprint.pprint(vars(sub))
        response += "\n/" + sub.subreddit_name_prefixed + " | [link](" + sub.url + ")"
    return response


def find_controversial_submissions(user):
    response = "\n\n**Most controversial submissions this past year**:\n\nSubreddit | Link\n:-- | :-:"
    for sub in reddit.redditor(user).submissions.controversial('year', limit=5):
        response += "\n/" + sub.subreddit_name_prefixed + " | [link](" + sub.url + ")"
    return response


def find_top_comments(user):
    response = "\n\n**Top comments this past year**:\n\nSubreddit | Link\n:-- | :-:"
    for cmt in reddit.redditor(user).comments.top('year', limit=5):
        response += "\n/u/" + str(cmt.subreddit) + " | [link](" + cmt.permalink() + ")"
    return response


def find_controversial_comments(user):
    response = "\n\n**Most controversial comments this past year**:\n\nSubreddit | Link\n:-- | :-:"
    for cmt in reddit.redditor(user).comments.controversial('year', limit=5):
        response += "\n/u/" + str(cmt.subreddit) + " | [link](" + cmt.permalink() + ")"
    return response


def find_fav_subs_comment(user):
    num_things = {}
    for cmt in reddit.redditor(user).comments.top('year', limit=1000):
        if str(cmt.subreddit) in num_things:
            num_things[str(cmt.subreddit)] += 1
        else:
            num_things[str(cmt.subreddit)] = 1
    response = "\n\n**Favorite subs to comment in (past year)**:\n\nSub | # Posts \n:-- | :-:"
    for x in sorted(num_things.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        response += "\n/r/" + x[0] + " | " + str(x[1])
    return response


if not os.path.isfile("hits.txt"):
    hits = []
else:
    with open("hits.txt", "r") as f:
        hits = f.read()
        hits = hits.split("\n")
        hits = list(filter(None, hits))

for comment in subreddit.stream.comments():
    if comment.id not in hits:
        if re.search(cfg.search_phrase, comment.body, re.IGNORECASE):
            if re.search(r'(\/u\/[a-z_A-Z-0-9]+)', comment.body, re.IGNORECASE):
                user = re.search(r'\/u\/([a-z_A-Z-0-9]+)', comment.body, re.IGNORECASE).group(1)
                # try:
                comment.reply(
                    "Here is the dirty dirt on " + user + ". I hope this is revealing!" + find_fav_subs_comment(
                        user) + find_top_comments(user) + find_controversial_comments(user) + find_top_submissions(
                        user) + find_controversial_submissions(user))
                # except Exception:
                # comment.reply("Can't find that user.")
                hits.append(comment.id)
                print(hits)
                with open("hits.txt", "a") as f:
                    f.write(comment.id + "\n")
