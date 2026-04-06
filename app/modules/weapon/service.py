from typing import List, Optional, Tuple

from sqlmodel import Session, select, func

from app.modules.weapon.models import Weapon
from app.modules.weapon.schemas import WeaponCreate, WeaponUpdate


def create_weapon(session: Session, data: WeaponCreate) -> Weapon:
    weapon = Weapon.model_validate(data)
    session.add(weapon)
    session.commit()
    session.refresh(weapon)
    return weapon


def get_weapons(
    session: Session,
    offset: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
) -> Tuple[int, List[Weapon]]:
    """
    Obtiene un listado paginado de armas desde la base de datos.

    Parámetros: 
        offset : int
            Cantidad de registros iniciales que deben omitirse.
            Navegacion entre paginas de resultados.

        limit : int
            Numero maximo de registros que se devolveran en la pagina actual.

        name : Optional[str]
            Filtro opcional para buscar armas por nombre. Si se proporciona.

    Retorna
    -------
    Tuple[int, List[Weapon]]
        Una tupla con dos elementos:
        - total: numero total de registros que coinciden con el filtro
        - items: lista de armas correspondientes a la página solicitada
    """

    # -----------------------------------------------------------
    # 1. CONSTRUCCIÓN DE LA CONSULTA BASE
    # -----------------------------------------------------------
    # Se crea una consulta inicial que selecciona todos los registros
    # de la tabla Weapon. A partir de esta consulta base se aplicarán
    # filtros y paginación.
    query = select(Weapon)

    # -----------------------------------------------------------
    # 2. FILTRO DINÁMICO
    # -----------------------------------------------------------
    # Si el cliente envía el parámetro 'name', se añade una cláusula
    # WHERE a la consulta. El operador ilike permite realizar una
    # búsqueda insensible a mayúsculas/minúsculas.
    if name:
        query = query.where(Weapon.name.ilike(f"%{name}%"))

    # -----------------------------------------------------------
    # 3. CÁLCULO DEL TOTAL DE REGISTROS
    # -----------------------------------------------------------
    # Calcula el total de registros que coinciden con los filtros
    # para que el frontend pueda construir la paginación.
    # Se usa COUNT(*) sobre la consulta filtrada.
    count_query = select(func.count()).select_from(query.subquery())

    # Se ejecuta la consulta de conteo.
    total = session.exec(count_query).one()

    # -----------------------------------------------------------
    # 4. APLICAR PAGINACIÓN
    # -----------------------------------------------------------
    # Finalmente se aplica paginación a la consulta principal.
    #
    # offset → cuántos registros se omiten
    # limit  → cuántos registros se devuelven
    #
    # Esto evita cargar todos los registros de la tabla en memoria.
    results = session.exec(query.offset(offset).limit(limit)).all()

    # -----------------------------------------------------------
    # 5. RETORNO DEL RESULTADO
    # -----------------------------------------------------------
    # Se devuelve una tupla con:
    # - el total de registros
    # - la lista de armas de la página actual
    
    return total, list(results)


def get_weapon(session: Session, weapon_id: int) -> Optional[Weapon]:
    return session.get(Weapon, weapon_id)


def update_weapon(
    session: Session, weapon_id: int, data: WeaponUpdate
) -> Optional[Weapon]:
    weapon = session.get(Weapon, weapon_id)
    if not weapon:
        return None

    weapon_data = data.model_dump(exclude_unset=True)

    for key, value in weapon_data.items():
        setattr(weapon, key, value)

    session.add(weapon)
    session.commit()
    session.refresh(weapon)

    return weapon


def delete_weapon(session: Session, weapon_id: int) -> bool:
    weapon = session.get(Weapon, weapon_id)

    if not weapon:
        return False

    session.delete(weapon)
    session.commit()

    return True