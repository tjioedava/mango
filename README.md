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


