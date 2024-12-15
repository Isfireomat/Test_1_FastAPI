from typing import Dict, Optional, List, Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_base import  CRUD

def router_update(router_set: APIRouter) -> None:
    router_dict: Dict = []
    routers: Dict = []
    for router in router_set.routes[::-1]:
        if {f"{router.path}": router.methods} not in router_dict:
            router_dict.append({f"{router.path}": router.methods})
            routers.append(router)
    router_set.routes = routers[::-1]
    
def updating(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        router_update(router_set=self)
        return result
    return wrapper
 

class UpdatingAPIRouter(APIRouter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @updating
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
    
    @updating
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
    
    @updating
    def put(self, *args, **kwargs):
        return super().put(*args, **kwargs)
    
    @updating
    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs)
    
    @updating
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
    
def http_exception_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            object = await func(*args, **kwargs)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f'{e}'
            )
        if not object:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{object}"
                )
        return object
    return wrapper

T = TypeVar("T", bound=BaseModel)    

class Id:
        id: Optional[int] = None 

def add_id(schema: Type[T], postscript: str = ''):
    class WithId(schema,Id):
        
        class Config:
            from_attributes = True
            
    WithId.__name__ = f"{schema.__name__}WithId {postscript}"
    return WithId
        
def create_CRUD_router(
        model, 
        schema: Type[T],
        api: str,
        session: AsyncSession
    ) -> UpdatingAPIRouter:
    
    crud: CRUD = CRUD(model=model)
    router: UpdatingAPIRouter = UpdatingAPIRouter()
    WithId: Type[BaseModel] = add_id(schema=schema, postscript='CRUD')
    
    @router.post(f'{api}', response_model=WithId)
    async def create(
                    response: Response, 
                    object: schema,
                    session: AsyncSession = Depends(session)
                ) -> T:
        """
        Создание объекта в БД и получение его.     
        """
        @http_exception_handler
        async def handler():
            return await crud.create(
                    session=session,
                    object=object 
                )
        return await handler()

    @router.get(f'{api}/{{id}}', response_model=WithId)
    async def read(
                    response: Response, 
                    id: int,
                    session: AsyncSession = Depends(session)
                ) -> T:
        """
        Получение объекта.
        """
        @http_exception_handler
        async def handler():
            return await crud.read(
                    session=session,
                    id=id
                )
        return await handler()

    @router.get(f'{api}', response_model=List[WithId])
    async def read_all(
                        response: Response, 
                        session: AsyncSession = Depends(session)
                    ) -> T:
        """
        Получение списка объектов из БД.
        """
        @http_exception_handler
        async def handler():
            return await crud.read_all(
                    session=session 
                )
        return await handler()

    @router.put(f'{api}/{{id}}', response_model=WithId)
    async def update(
                    response: Response, 
                    object: schema,
                    id: int,
                    session: AsyncSession = Depends(session)
                ) -> T:
        """
        Обновление информации о объекте.
        """
        @http_exception_handler
        async def handler():
            return await crud.update(
                    session=session,
                    id=id,
                    object=object 
                )
        return await handler()

    @router.delete(f'{api}/{{id}}', response_model=Dict[str, str])
    async def delete(
                    response: Response, 
                    id: int,
                    session: AsyncSession = Depends(session)
                ) -> Dict:
        """
        Удаление объекта.
        """
        @http_exception_handler
        async def handler():
            return await crud.delete(
                session=session,
                id=id 
            )
        await handler()
        return {'Message':'delete successful'}
    
    return router