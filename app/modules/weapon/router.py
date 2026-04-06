from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.core.database import get_session
from app.modules.weapon import service
from app.modules.weapon.schemas import (
    WeaponPaginatedResponse,
    WeaponCreate,
    WeaponRead,
    WeaponUpdate,
)

router = APIRouter(prefix="/weapons", tags=["weapons"])


@router.post("/", response_model=WeaponRead, status_code=201)
def create_weapon(weapon: WeaponCreate, session: Session = Depends(get_session)):
    return service.create_weapon(session, weapon)

@router.get("/", response_model=WeaponPaginatedResponse)
def list_weapons(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """
    Endpoint de listado de armas con soporte para:
    - paginación
    - filtros dinámicos
    - validación automática de parámetros

    Parámetros
    ----------
    offset : int
        Cantidad de registros iniciales que se deben omitir.
        Permite navegar entre páginas de resultados.

        Validación:
        - ge=0 → el valor debe ser mayor o igual a 0

    limit : int
        Cantidad máxima de registros que se devolverán en la respuesta.

        Validación:
        - ge=1  → mínimo 1 registro
        - le=100 → máximo 100 registros

        Esto evita que un cliente solicite volúmenes excesivos.

    name : Optional[str]
        Filtro opcional para buscar armas por nombre.
        Si se envía, el servicio aplicará una condición WHERE
        en la consulta SQL.

    Retorna
    -------
    WeaponPaginatedResponse
    """

    # 1. LLAMADA AL SERVICIO
    total, items = service.get_weapons(
        session=session,
        offset=offset,
        limit=limit,
        name=name,
    )

    # -----------------------------------------------------------
    # 2. CONSTRUCCIÓN DE LA RESPUESTA
    # -----------------------------------------------------------
    # El router construye el objeto que será serializado como JSON
    # y enviado al cliente.
    #
    # FastAPI validará automáticamente que la estructura coincida
    # con el modelo WeaponPaginatedResponse
    return {
        "total": total,
        "items": items,
    }


@router.get("/{weapon_id}", response_model=WeaponRead)
def get_weapon(weapon_id: int, session: Session = Depends(get_session)):
    weapon = service.get_weapon(session, weapon_id)

    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")

    return weapon


@router.patch("/{weapon_id}", response_model=WeaponRead)
def update_weapon(
    weapon_id: int, data: WeaponUpdate, session: Session = Depends(get_session)
):
    weapon = service.update_weapon(session, weapon_id, data)

    if not weapon:
        raise HTTPException(status_code=404, detail="Weapon not found")

    return weapon


@router.delete("/{weapon_id}", status_code=204)
def delete_weapon(weapon_id: int, session: Session = Depends(get_session)):
    if not service.delete_weapon(session, weapon_id):
        raise HTTPException(status_code=404, detail="Weapon not found")