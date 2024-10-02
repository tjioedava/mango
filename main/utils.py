from django.contrib.auth.models import User

'''
> Validates given username, password, and password confirmation
> Return type: 2-tuple consisting valid flag and invalid messages
> Checks whether:
  * Given username and password length is at minimum 8
  * Given username has been taken
  * Password confirmation does not match the given password
'''
def validate_user_creation_input(username: str, password: str, password_confirmation: str) -> tuple:
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

'''
> Validates given product name, price, and description
> Return type: 2-tuple consisting valid flag and invalid messages
> Checks whether:
  * Given name's length is at least 4
  * Given price is decimal and non negative integers
> Description is nullable. No check performed.
'''
def validate_product_form_input(name: str, price: str, description: str):
    invalid_messages = []
    valid_flag = True
    if len(name) < 4:
        invalid_messages.append('Product name must be at least 4 characters')
        valid_flag = False
    if price.isdecimal():
        price = int(price)
        if price < 0:
            invalid_messages.append('Price cannot be negative')
            valid_flag = False
    else:
        invalid_messages.append('Price must be an integer')
        valid_flag = False
    return (valid_flag, invalid_messages)
