from apps import app
from apps.api.friends.controller import *


app.add_url_rule(
    '/other_user_profile/<int:id>', 'other_user_profile', other_user_profile, methods=['GET']
    )

app.add_url_rule(
    '/send_friend_request/<int:receiver_id>', 'send_friend_request', send_friend_request, methods=['POST']
    )

app.add_url_rule(
    '/get_pending_requests/', 'get_pending_requests', get_pending_requests, methods=['GET']
    )

app.add_url_rule(
    '/handle_friend_request/', 'handle_friend_request', handle_friend_request, methods=['POST']
    )

app.add_url_rule(
    '/cancel_request/<int:receiver_id>', 'cancel_request', cancel_request, methods=['POST']
    )

app.add_url_rule(
    '/get_friends_list/', 'get_friends_list', get_friends_list, methods=['GET']
    )

app.add_url_rule(
    '/remove_friend/<int:friend_id>', 'remove_friend', remove_friend, methods=['POST']
    )