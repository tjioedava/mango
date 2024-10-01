from django.contrib.auth.models import User

'''
> Validates given username, password, and password confirmation
> Return type: 2-tuple consisting valid flag and invalid messages
> Checks whether:
  * Given username and password length is at minimum 8
  * Given username has been taken
  * Password confirmation does not match the given password
'''
def validate_user_generation_input(username: str, password: str, password_confirmation: str) -> tuple:
    invalid_messages = []
    valid_flag = True

    if len(username) < 4:
        invalid_messages.append('Username must contain at least 4 characters')
        valid_flag = False
    if len(User.objects.filter(username=username)) != 0:
        invalid_messages.append(f'Username {username} has been taken')
        valid_flag = False
    if len(password) < 8:
        invalid_messages.append('Password must contain at least 8 characters')
        valid_flag = False
    if password != password_confirmation:
        invalid_messages.append('Password confirmation not matching')
        valid_flag = False

    return (valid_flag, invalid_messages)