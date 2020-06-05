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
        tag.post_tag.append(post)