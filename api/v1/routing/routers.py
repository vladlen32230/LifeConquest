from fastapi import APIRouter
from routing.routes.auth import get_jwt_route_v1
from models.sqlalchemy import (
    SaUser, SaClan, SaClanRequest, 
    SaClanMembership, SaDivision, 
    SaDivisionMembership, SaPassedDivision,
    SaPassedDivisionMembership, SaDuel,
    SaPassedDuel, SaDuelInvite,
    SaClanWar, SaClanWarParticipant,
    SaPassedClanWar, SaPassedClanWarParticipant,
    SaClanWarInvite
)

from routing.routes.websockets import task_websocket_v1, task_websocket_docs_dummy_route_v1
from routing.routes.users import users_get_by_id_v1, users_delete_by_id_v1, users_patch_by_id_v1, users_extended_get_v1, users_post_v1, users_get_by_jwt_v1
from routing.routes.clans import clans_get_by_id_v1, clans_delete_by_id_v1, clans_patch_by_id_v1, clans_extended_get_v1, clans_post_v1
from routing.routes.duels import duels_get_by_id_v1, duels_extended_get_v1
from routing.routes.complex import complex_post_duel_v1, complex_post_clan_war_v1, complex_post_clan_membership_v1, complex_get_user_info_v1
from routing.routes.clan_wars import clan_wars_get_by_id_v1, clan_wars_extended_get_v1
from routing.routes.divisions import divisions_get_by_id_v1, divisions_extended_get_v1
from routing.routes.duel_invites import duel_invites_get_by_id_v1, duel_invites_extended_get_v1, duel_invites_delete_by_id_v1
from routing.routes.passed_duels import passed_duels_get_by_id_v1, passed_duels_extended_get_v1
from routing.routes.clan_requests import clan_requests_get_by_id_v1, clan_requests_delete_by_id_v1, clan_requests_extended_get_v1, clans_requests_post_v1
from routing.routes.clan_war_invite import clan_war_invites_get_by_id_v1, clan_war_invites_extended_get_v1, clan_war_invites_delete_by_id_v1
from routing.routes.clan_memberships import clan_memberships_get_by_id_v1, clan_memberships_delete_by_id_v1, clan_memberships_extended_get_v1
from routing.routes.passed_divisions import passed_divisions_get_by_id_v1, passed_divisions_extended_get_v1
from routing.routes.passed_clan_wars import passed_clan_wars_get_by_id_v1, passed_clan_wars_extended_get_v1
from routing.routes.division_memberships import division_memberships_get_by_id_v1, division_memberships_extended_get_v1
from routing.routes.clan_war_participants import clan_war_participants_get_by_id_v1, clan_war_participants_extended_get_v1
from routing.routes.passed_division_memberships import passed_division_memberships_get_by_id_v1, passed_division_memberships_extended_get_v1
from routing.routes.passed_clan_war_participants import passed_clan_war_participant_get_by_id_v1, passed_clan_war_participants_extended_get_v1

complex_router = APIRouter(tags=['complex'])
complex_router.add_api_route(**complex_post_duel_v1)
complex_router.add_api_route(**complex_post_clan_war_v1)
complex_router.add_api_route(**complex_post_clan_membership_v1)
complex_router.add_api_route(**complex_get_user_info_v1)

auth_router = APIRouter(tags=['authentication'])
auth_router.add_api_route(**get_jwt_route_v1)

users_router = APIRouter(tags=[SaUser.get_table_name()])
users_router.add_api_route(**users_get_by_id_v1)
users_router.add_api_route(**users_delete_by_id_v1)
users_router.add_api_route(**users_patch_by_id_v1)
users_router.add_api_route(**users_extended_get_v1)
users_router.add_api_route(**users_post_v1)
users_router.add_api_route(**users_get_by_jwt_v1)

clans_router = APIRouter(tags=[SaClan.get_table_name()])
clans_router.add_api_route(**clans_get_by_id_v1)
clans_router.add_api_route(**clans_delete_by_id_v1)
clans_router.add_api_route(**clans_patch_by_id_v1)
clans_router.add_api_route(**clans_extended_get_v1)
clans_router.add_api_route(**clans_post_v1)

clan_requests_router = APIRouter(tags=[SaClanRequest.get_table_name()])
clan_requests_router.add_api_route(**clan_requests_get_by_id_v1)
clan_requests_router.add_api_route(**clan_requests_delete_by_id_v1)
clan_requests_router.add_api_route(**clan_requests_extended_get_v1)
clan_requests_router.add_api_route(**clans_requests_post_v1)

clan_memberships_router = APIRouter(tags=[SaClanMembership.get_table_name()])
clan_memberships_router.add_api_route(**clan_memberships_get_by_id_v1)
clan_memberships_router.add_api_route(**clan_memberships_delete_by_id_v1)
clan_memberships_router.add_api_route(**clan_memberships_extended_get_v1)

divisions_router = APIRouter(tags=[SaDivision.get_table_name()])
divisions_router.add_api_route(**divisions_get_by_id_v1)
divisions_router.add_api_route(**divisions_extended_get_v1)

division_memberships_router = APIRouter(tags=[SaDivisionMembership.get_table_name()])
division_memberships_router.add_api_route(**division_memberships_get_by_id_v1)
division_memberships_router.add_api_route(**division_memberships_extended_get_v1)

passed_divisions_router = APIRouter(tags=[SaPassedDivision.get_table_name()])
passed_divisions_router.add_api_route(**passed_divisions_get_by_id_v1)
passed_divisions_router.add_api_route(**passed_divisions_extended_get_v1)

passed_division_memberships_router = APIRouter(tags=[SaPassedDivisionMembership.get_table_name()])
passed_division_memberships_router.add_api_route(**passed_division_memberships_get_by_id_v1)
passed_division_memberships_router.add_api_route(**passed_division_memberships_extended_get_v1)

duels_router = APIRouter(tags=[SaDuel.get_table_name()])
duels_router.add_api_route(**duels_get_by_id_v1)
duels_router.add_api_route(**duels_extended_get_v1)

passed_duels_router = APIRouter(tags=[SaPassedDuel.get_table_name()])
passed_duels_router.add_api_route(**passed_duels_get_by_id_v1)
passed_duels_router.add_api_route(**passed_duels_extended_get_v1)

duel_invites_router = APIRouter(tags=[SaDuelInvite.get_table_name()])
duel_invites_router.add_api_route(**duel_invites_get_by_id_v1)
duel_invites_router.add_api_route(**duel_invites_extended_get_v1)
duel_invites_router.add_api_route(**duel_invites_delete_by_id_v1)

clan_wars_router = APIRouter(tags=[SaClanWar.get_table_name()])
clan_wars_router.add_api_route(**clan_wars_get_by_id_v1)
clan_wars_router.add_api_route(**clan_wars_extended_get_v1)

clan_war_participants_router = APIRouter(tags=[SaClanWarParticipant.get_table_name()])
clan_war_participants_router.add_api_route(**clan_war_participants_get_by_id_v1)
clan_war_participants_router.add_api_route(**clan_war_participants_extended_get_v1)

passed_clan_wars_router = APIRouter(tags=[SaPassedClanWar.get_table_name()])
passed_clan_wars_router.add_api_route(**passed_clan_wars_get_by_id_v1)
passed_clan_wars_router.add_api_route(**passed_clan_wars_extended_get_v1)

passed_clan_war_participants_router = APIRouter(tags=[SaPassedClanWarParticipant.get_table_name()])
passed_clan_war_participants_router.add_api_route(**passed_clan_war_participant_get_by_id_v1)
passed_clan_war_participants_router.add_api_route(**passed_clan_war_participants_extended_get_v1)

clan_war_invites_router = APIRouter(tags=[SaClanWarInvite.get_table_name()])
clan_war_invites_router.add_api_route(**clan_war_invites_get_by_id_v1)
clan_war_invites_router.add_api_route(**clan_war_invites_extended_get_v1)
clan_war_invites_router.add_api_route(**clan_war_invites_delete_by_id_v1)

websocket_router = APIRouter(tags=['websocket'])
websocket_router.add_api_websocket_route(**task_websocket_v1)
websocket_router.add_api_route(**task_websocket_docs_dummy_route_v1)