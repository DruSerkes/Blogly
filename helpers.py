from models import Tag, PostTag

def tag_post(tags, post):
    """ 
    Expects array of tag names and SQLAlchemy post object 
    Removes tags from post
    Sets new tags on post 
    """
    # Remove current tags from post relations 
    PostTag.query.filter(PostTag.post_id == post.id).delete() 

    for tag in tags:
        # Use tag name to find tag in db 
        tag = Tag.query.filter(Tag.name == tag).one()
        # Add new post to a tag 
        post.tags.append(tag)


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc

    Found on Stack Overflow at 
    https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python

    Updates: 
    1. added .astimezone() for aware datetime
    2. add int() wrapper for seconds/minutes/hours ago  
    """
    from datetime import datetime
    now = datetime.now().astimezone()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"