from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.patch import construct_patch_by_id_route_v1
from routing.routes_constructors.delete import construct_delete_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from routing.routes_constructors.post.user import construct_post_user_v1
from routing.routes_constructors.specific.users import construct_get_user_by_jwt_route_v1
from models.sqlalchemy import SaUser
from models.pydantic.patch import PdPatchUser
from models.pydantic.extended import PdExtUser
from models.pydantic.returning import PdUser

def _users_delete_patch_checker_v1(current_user: SaUser, user: SaUser) -> bool:
    return current_user.id == user.id

users_get_by_id_v1 = construct_get_by_id_route_v1(SaUser, PdUser)
users_delete_by_id_v1 = construct_delete_by_id_route_v1(SaUser, _users_delete_patch_checker_v1) # type: ignore
users_patch_by_id_v1 = construct_patch_by_id_route_v1(SaUser, PdUser, PdPatchUser, _users_delete_patch_checker_v1) # type: ignore
users_extended_get_v1 = construct_extended_get_v1(SaUser, PdExtUser, PdUser)
users_post_v1 = construct_post_user_v1()
users_get_by_jwt_v1 = construct_get_user_by_jwt_route_v1()