## Assignment 4

1. Difference between `django.http.HttpResponseRedirect` and `django.shortcuts.redirect` 

    `HttpResponseRedirect` is used to redirect browser or client to passed URL. For instance, when a client successfully log in, they send a POST request, and the server will not return a new page of that same URL, but rather redirect the client to a new URL, usually main / home page. 

    `redirect` has same primary functionality with `HttpResponseRedirect`. It redirects the user to passed URL. 

    The main difference between `HttpResponseRedirect` and `redirect` is that `redirect` is a shortcut for `HttpResponseRedirect`. `redirect` wraps and eventually returns its `HttpResponseRedirect` counterpart. `redirect` usage is more versatile, since it additionally accepts URL pattern name (which will be mapped into its URL in application urls.py) and models (whose `get_absolute_url` method will be invoked). Also `redirect` is shorter in length, making it more suitable choice for cleaner code.  

2. Explain the process of connecting `Product` model with `User` model!

    The relation of `Product` and `User` in main application is <i>many to one</i>, meaning that many instances of `Product` can belong to one `User`, or in more SQL-ish term, each row of `Product`'s table has foreign key that maps to certain `User`'s row, with many row of `Product` can have reference to a single `User` row.

    By connecting `Product` to `User`, it creates a notion that products are clustered based on certain user belonging, thus the CRUD operation for users are limited to instances that they belong only. 

    The process of connecting `Product` and `User` starts by modifying Django models ORM, defining additional attribute for `Product` model, user, which is a `ForeignKey` that uses `User` as the foreign key model. The delete operation of the field will be `models.CASCADE`, meaning that a deletion of certain `User` instance will delete every `Product` instance whose foreign key refers to that `User` instance. After modifying the ORM, make the migrations schema and apply the migration to the database.

    In `views.py`, we will modify the logic of showing `Products`. Instead of showing all entries of `Product`, we will only show the entries that belong to current client, thus limiting the scope of CRUD operations to those belonging to current client. This is possible using `filter` method in `Product.models`.   

3. What are the differences between authentication and authorization? What happens when a user logs in? How Django implements those two concepts?

    Authentication is the process of verifying what a user claims to be. It checks inputted or sent credentials and whether they match a user account in the database.  

    Authorization is the process of determining what a user can do. It checks the type of the user, what group does the user belong in, and the permission flag. 

    When a user logs in, usually the client sends the credentials through POST method, and the credentials will be matched with a user existing in database. This is done by using `django.contrib.auth.authenticate` method, which returns the corresponding user if matches, and None otherwise. The corresponding user then will be passed to `django.contrib.auth.login` function that 'verifies' the claim of the client / browser that they are the legitimate corresponding user, by creating a new session of that user, and embed the session ID to the browser persistent cookies.

    Django implementation of authentication has been covered in the previous paragraph.

    Django implementation of authorization includes checking the permission flag and group, and usually is done using decorators from `django.cotrib.auth` API. The common pattern of the decorators is to pre-check the current user status, whether it is an anonymous user, a regular authenticated user, or a superuser. Then it will perform the views function that is passed in the decorator if the user is authorized, or otherwise do follow up actions such as error messages or redirecting to log in pages. 

4. How Django remembers logged in users? Explain other purposes of cookies. Are all cookies safe?

    Django remembers logged in users by using sessions and cookies. Whenever a user logs in, the server will create a new session, which is information about series of requests made my the same user. The server then will embed the session identifier (session ID) in the client's browser, by default in form of persistent cookies that last for two weeks. With session ID cookie in client's browser, the server can know whether the client has logged in, thus assuming the authenticity of the user and making stateful interaction. With sessions and cookies, a client doesn't have to log in everytime they visit a page or another different page.

    Cookies are also used to store user's preferences (yielded from session interaction) on the client side, making the web service more personalized. Eg. in social media web, the initial interaction of a client and the server yields information that the client has preferences over animal content, thus the server will store, perhaps animal keyword, in the client's browser cookies, so that next interaction will be more personalized by showing more animal contents.

    Cookies can be stored inside the browser app or local files. When cookies are stored in local files, client's other application or program can read the cookies, therefore making the cookies less secure. Henceforth, not all cookies are safe and cookies that contain confidential information such as session ID, CSRF token, and passwords should not be stored in local files. 

5. How do you implement each checkpoint? Explain in step-by-step manner!
    
    * Implement registration feature

        1. Use built in user creation form `django.contrib.auth.forms.UserCreationForm` for dynamic content passing.

        2. Create a registration view in `views.py` that will instantiate a new user creation form and deliver a HTML template with that user creation form passed as dynamic content. If the request method is POST, instantiate the form with existing values from request parameters instead, then check the validity. If it is valid, create a new user based on the credentials.

        3. Create the HTML template referred in point (2) that shows the form in table format, wrapped with form tags with POST method.

        4. Define application URL routing for the view, eg. `register`.

    * Implement log in feature

        1. Same process as the implementation of registration feature, only differs in the creation of view.

        2. Instead of using `django.contrib.auth.forms.UserCreationForm` as mentioned in the first (1) point of previous step, use `django.contrib.auth.forms.AuthenticationForm` to prompt credentials necessary for authentication.

        3. Instead of creating a new user if the input is valid, as mentioned in point (2) in previous steps, we authenticate the credentials, that yields `User` or None. If the credentials are valid that they yield `User`, log in that user using `django.contrib.auth.login` to create a new session, with ID stored in client browser's cookies.

    * Implement log out feature

        1. Create a view that simply logs out user using `django.contrib.auth.logout` method then redirect to log in page.
        2. Use that view as a handler for log out URL pattern.
        3. Optionally, add `django.views.decorators.http.required_http_methods` decorator for the view, and set it to allow POST method only. With this way, user won't be logged out if accidentally accessing log out URL through GET method. 

    * Add hyperlink for connectivity between log in, register, and log out functionality.

        1. Add hyperlink that directs user to log in page in register page if the user already has an account and vica versa, if the user doesn't have any account.

        2. In home page, add a button wrapped with a form that yields POST request to log out. Referring to the previous step point (3), users can only log out through this button, assuming correct usage of CSRF token.

    * Add `django.contrib.auth.decorators.login_required` decorators in appropriate views to require users for authentication before accessing certain pages / URL.

        1. Add the decorators in appropriate views with parameter `login_url` equals to the URL path of log in page.

        2. In log in view, instead of redirecting client to home page after successfull log in, redirect them to the path specified by `next` query instead. This query is appended automatically by `django.contrib.auth.decorators.login_required` when the client is temporarily redirected from original URL to log in URL for authentication.

        This way, if a client with session ID not referring to authenticated user session, eg. `AnonymousUser`, then Django will redirect the client to land on log in page.

    * Link the `Product` model with `User`

        1. Already well-explained in number two, elaborated in the next step
        2. In `models.py`, create additional field of `Product`, named `user`, with value `models.ForeignKey(Product, on_delete=models.CASCADE)`. This will create a foreign key that refers to `User` model, with cascading deletion, meaning that deletion of a user implies deletion of every products that refers to that user.
        3. Make the migration schema based on the changes made in `models.py` with command `python manage.py makemigrations` in terminal. To deal with already existing products that don't have corresponding user, provide default value with primary key 1, assuming that at least one user has been created in local database (which is true, since in the previous assignment, a `superuser` is created). This will make the pre-existing products belong to the `superuser`.
        4. Apply the migration to the local database by command `python manage.py migrate`
        5. In `views.py`, change the logic of CRUD operation on products. Instead of showing all available products in the database, show products that belong to the current user instead, by substituting `Product.models.all()` to `Product.models.filter(user=request.user)`. Apply this to the views that deliver product(s) in JSON/XML format. Change the product creation logic by not immediately saving the form of product creation into product instance, rather using `commit=False` argument so that the `form.save()` method only returns the instance of the product, not saving it to the database. Then, assign current user `request.user` to the product's user field, then save the product using `product.save()` to save the product in the database. This approach will avoid errors yielded due to user field being null.

    * Create two users, with each user having three products

        1. Assuming `superuser` counts, we only need to create three products of that `superuser` and create one additional user with three products as well. This is easily done by using the web service that we have developed.

    * Make use of cookies to display last log in. Additionally, display user's username in home page instead of static content.

        1. In home view, pass `request.user.username` as a context for dynamic content to render `home.html`. In `home.html`, display the username along with greetings phrase right below the header line.

        2. In log in view, after `login()` is invoked, temporarily store the return value (HTTP response) in variable, eg. response, so that we can perform method `set_cookie()` to assign cookies to the client. Set a cookie with key `'last_log_in'` and value `datetime.datetime.now()`, with cookie max age 60 * 60 * 24 * 7 or 2 weeks. The max age is specifically set to two weeks to align with the max age of session ID cookie, which is also 2 weeks.

        3. In home view, simply display the last log in cookie by retrieving it using key, `user.COOKIES['last_log_in']`, then pass it as context for dynamic content.

        4. In log out view, delete the cookie after `logout` function is invoked.

    


 






