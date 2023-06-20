try:
    from fastapi import APIRouter, Body, HTTPException, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
except Exception as e:
    print(f'Error! Some Modules are Missing  : {e}')

from ..dependencies import *

MAX_TOKENS = 15

router = APIRouter()


@router.post("/tokens/add", tags=["tokens"])
async def add_tokens(numero_alumno: str = Body(embed=True), tokens: str = Body(embed=True), authenticated: bool = Depends(token_authenticate)):
    valid_ids = get_auth_ids('ids.json')
    if numero_alumno not in valid_ids:
        raise HTTPException(status_code=404, detail="El numero de alumno solicitado no existe")
    if numero_alumno not in ['17640040+9grBXJmYUZ']:
        raise HTTPException(status_code=404, detail="Este numero de alumno no tiene los permisos necesarios")

    actual_tokens = int(valid_ids[numero_alumno])
    new_tokens = int(tokens)
    valid_ids[numero_alumno] = min(actual_tokens+new_tokens, MAX_TOKENS)
    update_ids(valid_ids)
    output_msg = {"numero_alumno" : numero_alumno.split("+")[0], "tokens" : valid_ids[numero_alumno]}
    if actual_tokens + new_tokens > MAX_TOKENS:
        warning_msg = {"warning": f"Remember that the maximum amount of tokens is {MAX_TOKENS}. If you want more tokens, email lfvansintjan@uc.cl"}
        output_msg.update(warning_msg)
    return output_msg