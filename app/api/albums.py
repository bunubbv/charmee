from fastapi import APIRouter, Query, Depends, HTTPException, status
from models.album import AlbumListResponse, AlbumItemResponse
from sqlalchemy.exc import NoResultFound
from core.depends import get_service

router = APIRouter(prefix='/api')

@router.get(
    '/albums',
    summary="Album List",
    response_model=AlbumListResponse
)
async def api_album_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
    service: get_service = Depends()
) -> AlbumListResponse:
    
    album_list = await service.get_album_list(page, item)
    return album_list


@router.get(
    '/albums/{album_id}',
    summary="Album Item",
    response_model=AlbumItemResponse
)
async def api_album_item(
    album_id: str,
    service: get_service = Depends()
) -> AlbumItemResponse:
    
    album_info = await service.get_album_info(album_id)
    return album_info