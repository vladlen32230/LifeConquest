from routing.routes_constructors.websockets.task import construct_task_websocket_v1

task_websocket_v1 = construct_task_websocket_v1()
task_websocket_docs_dummy_route_v1 = {
    'path': '/task',
    'endpoint': lambda: None,
    'description': """DUMMY ENDPOINT ONLY FOR DOCUMENTATION

    path: /task?jwt=...&time=...
        jwt - JWT of a current user
        time - time for a task in minutes

    when time passes by and if websocket was opened, then score, which is equal to time in minutes, will be added to the user.

    possible websocket status codes:
        1000: websocket successfully closed!
        3000: JWT is invalid, should fetch new one
        3003: User is occupied, meaning he already has working websocket.
        1011: Undefined behaviour
"""
}