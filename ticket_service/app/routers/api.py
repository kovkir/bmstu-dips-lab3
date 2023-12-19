from fastapi import APIRouter

from routers import ticket, manage


router = APIRouter()
router.include_router(ticket.router)
router.include_router(manage.router)
