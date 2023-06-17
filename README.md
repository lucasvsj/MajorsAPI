# MajorsAPI

## Endpoints

Esta API expone los siguientes *endpoints*:


### <span style="color: lightgreen;">GET</span> "/major/{major_name}"

Este *endpoint* es el encargado de obtener toda la informacion sobre el major `major_name`

### <span style="color: orange;">PUT</span> "/major/{major_name}"

Este *endpoint* es el encargado de actualizar el major `major_name` con los cursos que se entregan en el `body` de la *request*.

### <span style="color: red;">POST</span> "/major/{major_name}/validate"

Este *endpoint* es el encargado de validar si con los cursos entregados, el major `major_name` esta aprobado o no

### <span style="color: lightgreen;">GET</span> "/major/{major_name}/packages"

Este *endpoint* es el encargado de obtener todos los cursos que son parte del major `major_name`

### <span style="color: red;">DELETE</span> "/major/{major_name}/{course_name}" 

Este *endpoint* es el encargado de eliminar `course_name` del `major_name`.

## Config

* Comando para correr el servidor: `uvicorn app.main:app --reload --port 3000`

* Los requisitos estan en el archivo `requirements.txt`