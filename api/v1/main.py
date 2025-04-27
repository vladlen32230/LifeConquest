from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routing.routers import (
    auth_router, users_router, clans_router, 
    clan_requests_router, clan_memberships_router,
    divisions_router, division_memberships_router,
    passed_divisions_router, passed_division_memberships_router,
    duels_router, passed_duels_router, duel_invites_router,
    clan_wars_router, clan_war_participants_router,
    passed_clan_wars_router, passed_clan_war_participants_router,
    clan_war_invites_router, complex_router, websocket_router
)

app = FastAPI(root_path='/api/v1', title='LifeConquest')

routers = [
    auth_router, complex_router, users_router, clans_router, 
    clan_requests_router, clan_memberships_router,
    divisions_router, division_memberships_router,
    passed_divisions_router, passed_division_memberships_router,
    duels_router, passed_duels_router, duel_invites_router,
    clan_wars_router, clan_war_participants_router,
    passed_clan_wars_router, passed_clan_war_participants_router,
    clan_war_invites_router, websocket_router
]

for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)