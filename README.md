Link = http://dava-hannas-mango.pbp.cs.ui.ac.id/

1. How do I implement each task?
    # Note that libraries import statements are not mentioned
    # Git and remote Github repository have already been made from the beginning to track the checkpoints, thus won't be mentioned
    * Create a new Django project
        > Create a new directory and python virtual environment to isolate necessary dependencies.
        > Install dependencies listed in requirements.txt, including django library.
        > Create a django project with prompt 'django-admin startproject <project-name> .' ('.' included to place the project directory within the main directory).
        > In this case, the <project-name> is 'mango', inspired by the framework name, 'django', combined with the authenticity of using fruit name as brand name.
        > Adding 127.0.0.1 IP (which refers to local IP) in ALLOWED_HOST in settings.py to let the web be accessed from local host.
    * Create an application named 'main' in the project
        > Prompt 'python manage.py startapp <app-name>' to create a new application. The prompt will automatically create a new directory with pre-built modifiable files that define the application.
        > Register the application in settings.py by adding '<app-name>' to INCLUDED_APPS list.
        > In this case, the '<app-name>' is 'main'.
    * Configure project URL routing to include the 'main' application
        > Create urls.py inside the 'main' application.
        > Define a variable 'app_name' with value 'main' to define a namespace for 'main' application url routing.
        > Define a variable 'url_patterns' with value list of path objects. Add a path element from django.urls.path, with instantiation 'path('', lambda request: HttpResponseRedirect('Hello, World!'), name='home')'. This will set the routing for ANY path, relative to the application prefix path, to return a simple 'Hello, World!' hypertext to client.
        > Configure routing in the project level by inserting path('', include('main.urls')) in 'urlpatterns' in urls.py. This will direct the routing with '' prefix to main application routing.
    * Define a model named 'Product' in 'main' application
        > In models.py, create 'Product' class that extends models.Model
        > Define the model attributes, such as name, price, description, items_purcashed, rating, and a derived attribute, recommended, based on the rating.
        > Make migration using prompt 'python manage.py makemigrations' to create a schema for the model.
        > Prompt 'python manage.py migrate' to apply models schema to the database.
    * Create a function in views.py in 'main' application that returns a html template showing developer's name and class
        > Create a directory in 'main' application named 'templates'. Inside it, create a HTML template that shows developer's name and class, with file name 'home.html'.
        > Create a function in views.py named home that returns render(request, 'home.html', dict()). This will return the request as a http response in form of 'home.html', with empty context. Django will automatically seek the 'home.html' file inside the templates directory within the same application.
    * Create 'main' application routing to call the home function
        > Inside urls.py in the 'main' application directory, create a new path pattern 'home', which will map to 'home' function in views.py, with name 'home'.
        > Change the empty pattern path's name from 'home' to 'default', and change the lambda function to redirect to home url instead with 'django.shortcuts.redirect('main:home')'.
        > These steps will ensure that empty and 'home' url path will both lead to 'home' path that returns 'home.html' to client.
    * Deploy project to Pacil Web Service (PWS) to serve the project through third party service.
        > Create a PWS project and link the project with git local repository as remote.
        > Add web application link to ALLOWED_HOST in settings.py to let the third party service serve the project.
        > Push commits in git local repository to PWS remote.
        > PWS will build and serve the project, providing a domain service for the project, thus the web application can be accessed via internet.
    
2. Referring to client-request-flow.png, these are how application's urls.py, views.py, models.py, and templates interact with each other. 

Whenever there is an incoming request to the application, application's urls.py will route the request based on the URL request path using regular expression, mapping the path to assigned handler functions, either anonymous or defined in views.py. 

Usually in views.py, functions defined interact with the models in models.py. Possible interactions are: creation, retreival, update, and deletion. The model defined in models.py acts as a class representation of a table in database, while each model instance represents the row or entry. Django provides a way to manipulate database through the model class and instance methods as a way of query encapsulation (one of the main reason is to prevent SQL injection). This way, one can manipulate the database from views.py.

HTML files in templates directory is used to return a HTTP response back to client. HTML files usually contain dynamic content, dependent to values that are defined in context dictionary. Views.py interact with HTML files through render function that fetches a HTML and combine it with pairs of key:value that acts as a context to fill in the dynamic content.

3. Git acts as a version controller, that tracks changes or updates in developer's project. With git, a developer can easily create a new project version, rollback to previous version, and safely experiment with current version without the fear of messing the current project.

Git's cloud counterpart, eg. GitHub and GitLab, acts as a cloud based platform based on git, streches the scope and functionality of git beyond mere local machine, that enables developer to collaborate with another developer and save the project remotely.

4. Django framework is chosen for PBP course since Fasilkom 2023 students are already familiar with Python, a programming language that drives the framework. Other framework not driven by python programming language, eg. Laravel that uses PHP, might introduce unecessary learning curve variable, since students need to learn PHP as well in the process. Spring framework, although using Java, which has been taught during the second semester, might not be as suitable as Django, since Django has more managable learning curve for Fasilkom 2023 students. Another Django superiority is its pupolarity. Based on blog.jetbrains.com/pycharm/2024/06/the-state-of-django/ blog, 74% of web developers use Django as their web framework.

5. Django models are termed as ORM (Object Relational Mapping) due to the fact that Django uses python OOP to encapsulate or represent the database tables and rows / entries. Django models also allow developer to manipulate the database programmatically from the project instead of from direct SQL queries to the middleware, making it essentially an ORM.








