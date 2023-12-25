from apps import app
from apps.api.user.controller import (
    email_verification,upload_image,create_user,
    update_user,suggest_usernames,current_email_verification,
    new_email_verification,get_user_profile,search_user,
    get_all_users,delete_users,log_out,testing_api
)

app.add_url_rule(
    '/testing_api/', 'testing_api', testing_api, methods=['GET']
    )

app.add_url_rule(
    '/email_verification/', 'email_verification', email_verification, methods=['POST']
    )

app.add_url_rule(
    '/current_email_verification/', 'current_email_verification', current_email_verification, methods=['POST']
    )

app.add_url_rule(
    '/new_email_verification/', 'new_email_verification', new_email_verification, methods=['POST']
    )

app.add_url_rule(
    '/create_user/', 'create_user', create_user, methods=['POST']
    )

app.add_url_rule(
    '/suggest_usernames/', 'suggest_usernames', suggest_usernames, methods=['POST']
    )

app.add_url_rule(
    '/update_user/', 'update_user', update_user, methods=['POST']
    )

app.add_url_rule(
    '/get_user_profile/', 'get_user_profile', get_user_profile, methods=['GET']
    )

app.add_url_rule(
    '/search_user/', 'search_user', search_user, methods=['GET']
    )

app.add_url_rule(
    '/get_all_users/', 'get_all_users', get_all_users, methods=['GET']
    )

app.add_url_rule(
    '/delete_users/', 'delete_users', delete_users, methods=['POST']
    )

app.add_url_rule(
    '/log_out/', 'log_out', log_out, methods=['POST']
    )

app.add_url_rule(
    '/upload_image/', 'upload_image', upload_image, methods=['POST']
    )