from database import *

init_db()

user_id = create_user(
    "abel@example.com",
    "hashed_password"
)

print(user_id)

code = create_url(
    "https://www.google.com",
    user_id
)

print(code)

print(get_url(code))

print(get_urls_for_user(user_id))