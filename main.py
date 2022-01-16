import praw
from twilio.rest import Client

# The necessary credentials for the Reddit API
REDDIT_CLIENT_ID = 'REDDIT_CLIENT_ID'
REDDIT_CLIENT_SECRET = 'REDDIT_CLIENT_SECRET'

# The necessary credentials for the Twilio API
TWILIO_ACCOUNT_SID = 'TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'TWILIO_AUTH_TOKEN'


# Constructing a list of subreddits, and a properly formatted string from that list
def get_subreddits():
    subreddits = input('Which subreddit(s) would you like to monitor?\n'
                       '(Please separate multiple entries with a space): ')
    subreddits = subreddits.lower().split(' ')

    # Check if multiple subreddits were entered
    if subreddits.__len__() == 1:
        return subreddits[0]
    # For multiple subreddits:
    # subreddit = reddit.subreddit('subreddit_1+subreddit_2+..+subreddit_n')
    # Creating a properly formatted string
    elif subreddits.__len__() > 1:
        subreddits_string = ''
        for subreddit in subreddits:
            if subreddits.index(subreddit) == subreddits.__len__() - 1:
                subreddits_string += f'{subreddit}'
            else:
                subreddits_string += f'{subreddit}+'
    return subreddits_string


# Constructing a list of keywords
def get_keywords():
    keywords = input('Which keyword(s) would you like to be alerted about?\n'
                     '(Please separate multiple entries with a space): ')
    keywords = keywords.lower().split(' ')
    return keywords


def main():
    subreddits = get_subreddits()
    keywords = get_keywords()

    # Creating a READ-ONLY instance of Reddit
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="user_agent",
    )

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Creating an instance of the specified subreddit(s)
    subreddit = reddit.subreddit(subreddits)

    # Goes through new submissions in the subreddit(s) to see if the post title mentions any keyword
    for post in subreddit.stream.submissions():
        title_lower = post.title.lower()
        for keyword in keywords:
            if keyword in title_lower:
                message_body = f'There is a new post about {keyword}!\n\r' \
                               f'{post.title}\n\r' \
                               f'https://www.reddit.com{post.permalink}'

                message = client.messages.create(
                    body=message_body,
                    from_='+from_',
                    to='+to'
                )

                print(f'Sent a new message: {message.sid}')


if __name__ == '__main__':
    main()
