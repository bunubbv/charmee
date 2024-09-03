from fastapi import APIRouter, Query
from core.library import *

router = APIRouter(prefix = '/api')

@router.get('/albums')
async def api_album_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
) -> dict | list[dict]:
    
    album_list = await Library.get_album_list(page, item)
    return album_list


@router.get('/albums/{hash}')
async def api_album_info(
    hash: str,
) -> dict | list[dict]:
    
    album_info = await Library.get_album_info(hash)
    return album_info