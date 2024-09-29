from fastapi import APIRouter, HTTPException, status, Depends
from .services import (add_post, get_post_by_id, get_all_post,
                       modify_post, remove_post, add_comment, get_all_comments, modify_comment, remove_comment)
from .schemas import PostResponse, PostCreate, PostUpdate, CommentCreate, CommentResponse, UpdateComment
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)


@router.post('/post/create', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostCreate, current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    new_post = await add_post(post, current_user)
    return PostResponse.from_orm(new_post.serialize())


@router.get('/post/{post_id}', response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: str, current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    post = await get_post_by_id(post_id)

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')

    return PostResponse.from_orm(post.serialize())


@router.get('/posts', response_model=list[PostResponse], status_code=status.HTTP_200_OK)
async def get_posts(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    posts = await get_all_post(skip, limit)

    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Posts Not Found')

    return [PostResponse(**post.serialize()) for post in posts]


@router.put('/post/update/{post_id}', response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update_post(post: PostUpdate, post_id: str, current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    post = await modify_post(post, post_id)

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')

    return PostResponse.from_orm(post.serialize())


@router.delete('/post/delete/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(post_id: str, current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    result = await remove_post(post_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')

    return {'message': 'Post Deleted Successfully'}


@router.post('/post/{post_id}/comments/add', status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
async def create_comment(post_id: str, comment: CommentCreate, user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    new_comment = await add_comment(comment, post_id, user_id)
    if new_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
    return CommentResponse.from_orm(new_comment.serialize())


@router.get('/post/{post_id}/comments', response_model=list[CommentResponse], status_code=status.HTTP_200_OK)
async def get_comments(post_id: str, user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    comments = await get_all_comments(post_id)
    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comments Not Found')

    return [CommentResponse(**comment.serialize()) for comment in comments]


@router.put('/post/{post_id}/comments/{comment_id}/update', response_model=CommentResponse, status_code=status.HTTP_200_OK)
async def update_comment(comment: UpdateComment, post_id: str,
                         comment_id: str, user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    post = await modify_comment(comment, post_id, comment_id)
    return CommentResponse.from_orm(post.serialize())


@router.delete('/post/{post_id}/comment/{comment_id}/delete', status_code=status.HTTP_200_OK)
async def delete_comment(post_id: str, comment_id: str, user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    result = await remove_comment(post_id, comment_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Comment with {comment_id} not found')

    return {'message': 'Comment Deleted Successfully'}
