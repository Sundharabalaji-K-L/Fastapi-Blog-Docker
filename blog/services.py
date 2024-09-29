from app.mongodb import database
from .schemas import PostCreate, PostUpdate, CommentCreate, UpdateComment
from bson import ObjectId
from .models import Post, Comment


async def add_post(post: PostCreate, current_user: str):
    new_post = post.model_dump()
    new_post['user_id'] = ObjectId(current_user)
    result = await database['posts'].insert_one(new_post)
    return Post(**new_post, id=result.inserted_id)


async def get_post_by_id(post_id: str):
    post = await database['posts'].find_one({'_id': ObjectId(post_id)})

    if post is not None:
        return Post(**post)

    return None


async def get_all_post(skip: int = 0, limit: int = 10):
    posts = await database['posts'].find().skip(skip).limit(limit).sort('created_at', -1)\
        .sort('modified_at', -1).to_list(limit)
    if posts:
        return [Post(**post) for post in posts]

    return None


async def modify_post(post: PostUpdate, post_id: str):
    result = await database['posts'].update_one({'_id': ObjectId(post_id)}, {'$set': post.model_dump()})

    if result.modified_count == 0:
        return None

    return await get_post_by_id(post_id)


async def remove_post(post_id: str):
    result = await database['posts'].delete_one({'_id': ObjectId(post_id)})

    if result.deleted_count == 0:
        return None

    comment_result = await database['comments'].delete_many({'post_id': ObjectId(post_id)})
    return result.deleted_count


async def add_comment(comment: CommentCreate, post_id: str, user_id: str):
    post = await database['posts'].find_one({'_id': ObjectId(post_id)})

    if post is None:
        return None

    new_comment = comment.model_dump()
    new_comment['user_id'] = ObjectId(user_id)
    new_comment['post_id'] = ObjectId(post_id)
    result = await database['comments'].insert_one(new_comment)

    return Comment(**new_comment, id=result.inserted_id)


async def get_all_comments(post_id):
    posts = await database['comments'].find({'post_id': ObjectId(post_id)}).sort('modified_at', -1).to_list(None)

    if posts:
        return [Comment(**post) for post in posts]

    return None


async def modify_comment(comment: UpdateComment, post_id: str, comment_id: str):
    result = await database['comments'].update_one({'_id': ObjectId(comment_id), 'post_id': ObjectId(post_id)},
                                                   {'$set': comment.model_dump()})

    if result.modified_count == 0:
        return None

    comment = await database['comments'].find_one({'_id': ObjectId(comment_id)})
    if comment is None:
        return None

    return Comment(**comment)


async def remove_comment(post_id: str, comment_id: str):
    result = await database['comments'].delete_one({'_id': ObjectId(comment_id), 'post_id': ObjectId(post_id)})

    if result.deleted_count == 0:
        return None

    return result.deleted_count
