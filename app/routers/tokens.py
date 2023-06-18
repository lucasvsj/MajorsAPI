try:
    from fastapi import APIRouter, Body, HTTPException, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
except Exception as e:
    print(f'Error! Some Modules are Missing  : {e}')

from ..dependencies import *


router = APIRouter()


@router.post("/tokens/add", tags=["tokens"])
async def add_tokens(numero_alumno: str = Body(embed=True), tokens: str = Body(embed=True), authenticated: bool = Depends(token_authenticate)):
    valid_ids = get_auth_ids('ids.json')
    if numero_alumno not in valid_ids:
        raise HTTPException(status_code=404, detail="El numero de alumno solicitado no existe")
    if numero_alumno != '17640040':
        raise HTTPException(status_code=404, detail="Este numero de alumno no tiene los permisos necesarios")
    valid_ids[numero_alumno] += int(tokens)
    update_ids(valid_ids)
    return {"numero_alumno" : numero_alumno, "tokens" : tokens}