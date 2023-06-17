try:
    from fastapi import APIRouter, Body, HTTPException, status
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
except Exception as e:
    print(f'Error! Some Modules are Missing  : {e}')

from ..dependencies import *


router = APIRouter()


@router.get("/major/{major_name}", tags=["major"])
async def read_major(major_name: str):
    major_data = get_major_data(major_name)
    return major_data


@router.put("/major/{major_name}", tags=["major"], status_code=status.HTTP_200_OK)
async def update_major(major_name: str, major_payload: dict = Body()):
    if check_major_structure(major_payload):
        json.dump(major_payload, open(f'{os.getcwd()}/data/majors/{major_name}.json', mode='w'), indent=2)
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'La estructura no es la correcta')
    return {}


@router.post("/major/{major_name}/validate", tags=["major"])
async def validate_major(major_name: str, cursos_aprobados: list = Body(embed=True), authenticated: bool = Depends(authenticate)):
    if major_name not in get_all_majors():
        raise HTTPException(status_code=404, detail="El major solicitado no existe")
    courses = cursos_aprobados
    is_major_approved = check_major(major_name, courses)
    return {"major" : major_name, "aprobado" : is_major_approved}


@router.get("/major/{major_name}/packages", tags=["major"])
async def read_major(major_name: str, authenticated: bool = Depends(authenticate)):
    major_data = get_all_packages(major_name)
    return major_data


@router.delete("/major/{major_name}/{course_name}", tags=["major"])
async def delete_major(major_name: str, course_name: str, authenticated: bool = Depends(authenticate)):
    # Delete the major data
    remove_course_from_major(major_name, course_name)
    return {"message": f"Course {course_name} from Major '{major_name}' deleted successfully"}