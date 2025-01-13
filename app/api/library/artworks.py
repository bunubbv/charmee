from fastapi import APIRouter, Query, HTTPException, status, Depends
from fastapi.responses import FileResponse, StreamingResponse
from core.depends import get_library_repo
from services.artwork import ArtworkService
from PIL import Image
import asyncio
import io

router = APIRouter()

@router.get('/artworks/{id}')
async def api_get_artwork(
    id: str,
    size: int = Query(300, ge=0),
    repo: get_library_repo = Depends(),
) -> FileResponse:
    
    service = ArtworkService(repo)

    # Check if artwork is available in the filesystem ('artworks' directory).
    path = service.get_artwork_path(id, size)
    if path:
        return FileResponse(path)
    
    if not id.startswith('playlist_'):
        # Check if id (album or track) exists in library and extract if possible.
        data = await service.init_artwork(id)

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if size != 0:
            loop = asyncio.get_running_loop()
            img = await loop.run_in_executor(service.executor, Image.open, io.BytesIO(data))
            format = img.format.lower()

            await loop.run_in_executor(service.executor, img.thumbnail, [size, size], Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format)
            buffer.seek(0)

            await loop.run_in_executor(service.executor, service.save_artwork, img, id, size, format)
            return StreamingResponse(buffer, media_type=f'image/{format}')
    else:
        # 플레이리스트의 트랙 id를 가져와야 함. 아직 구현도 안 했으니 나중에 생각하기로..
        pass
        