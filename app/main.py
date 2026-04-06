from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.database import engine

# ── Importar TODOS los modelos antes de create_all ───────────────────────
# SQLModel necesita que las clases estén en memoria para crear las tablas.
# El orden importa: primero los modelos sin dependencias externas.
from app.modules.weapon.models import Weapon          # noqa: F401  (1:1)
from app.modules.hero.models import Hero, HeroTeamLink  # noqa: F401 (1:1, 1:N, N:M)
from app.modules.team.models import Team              # noqa: F401  (1:N, N:M)

# ── Routers ───────────────────────────────────────────────────────────────
from app.modules.health.router import router as health_router
from app.modules.hero.router import router as hero_router
from app.modules.team.router import router as team_router
from app.modules.weapon.router import router as weapon_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: crea todas las tablas registradas en SQLModel.metadata.
    Shutdown: espacio para cerrar conexiones, caches, etc.
    """
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="FastAPI + SQLModel — Relaciones 1:1 · 1:N · N:M",
    version="1.0.0",
    description=(
        "Proyecto modular que demuestra las tres relaciones principales:\n\n"
        "- **1:1** Hero ↔ Weapon (FK `weapon_id` en Hero)\n"
        "- **1:N** Team → Heroes (FK `team_id` en Hero, lado N)\n"
        "- **N:M** Hero ↔ Team via `HeroTeamLink`"
    ),
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(weapon_router)
app.include_router(team_router)
app.include_router(hero_router)
