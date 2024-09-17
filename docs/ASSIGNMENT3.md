## Assignment 3

1. Why do we need data delivery in web platform implementation?

    The entire functionality of web application service, often referred as CRUD (Create, Retreive, Update, Destroy), is based on data exchanges between client / customer machine and server or application service provider. Each data exchange is a two-way data delivery, where the client delivers a request data to the server and the server deliver a response data to the client as either HTML, CSS, script files, XML, or JSON string. 

    The server needs to know what operation does the client want to perform, thus the client needs to send the corresponding request through data delivery for the server to handle. The client needs a feedback after the operation, thus the server needs to send the response through, again, data delivery. Without data delivery, there won't be any communication between client and server, making web application service impossible.

2. Which one is better, XML or JSON. Why JSON is more popular compared to XML?

    Both XML and JSON come with their own set of advantages and drawbacks. They are formats to represent objects or data in efficient manner, and usually are used to deliver objects from server to client or via API. 
    
    XML syntax is more rigid and structured, making it suitable for concisely representing a document. In the other hand, JSON has more straightforward and simple syntax, making it more suitable for representing non document objects. 

    The answer for the first question depends on the usage context. If the context is that one party one to deliver a document to another party, then XML is superior. However, if the context is an exchange of simple data object, then XML's rigid syntax and structure is overkill, thus making JSON superior due to its simplicity.

    JSON is more popular in overall usage due to the fact that the majority of data deliveries, especially in API, is not in form of document object (if we do not considered HTML as subset of XML). Therefore, JSON is more suitable for most of data deliveries since we don't need XML over-structured and rigid syntax since the object is not in form of document and JSON format has less size relative to its XML's counterpart for the same object, thus requiring less packet size and bandwidth, making JSON more efficient. XML also requires the receiver to convert the string to a tree structure first, which contributes to quite unnecessary post-transfer processing.

3. What is the use of `is_valid()` and why do we need such method?

    `is_valid()` method in `django.forms.ModelForm` class is used to check whether a `ModelForm` instance has its attributes fields validly filled. It performs data cleaning and examination of filled values in fields. Then, it checks whether the cleaned values comply to the fields requirements defined in `ModelForm`'s subclass. The method will return `True` if and only if the data cleaning process went successfully and all the values comply to the requirements.

    `is_valid()` method is crucial when we want to validate POST request key and value pairs yielded from form submission. The pairs are used as parameters for instantiating `ModelForm` object, effectively fill the form fields with values from the request. Then the `is_valid()` method is invoked to check the validity of the values referring to the defined requirements. Usually, if the `is_valid()` method returns `True`, the server, from the form, will create the corresponding object to the database and redirect client. Otherwise, the server will re-render the submission page with the same, already-filled invalid form. 

4. Why do we need `csrf_token` in Django. What happens if we don't add `csrf_token` in Django forms and how can attackers exploit such vulnerabilities?

    One of the key feature of the internet is that a request for resource can be sent from anywhere, not necessarily only from certain page on certain site. For instance, POST request to perform account deletion operation, theoratically can be sent not only from the user's profile page, but also from malicious site that the victim user access. 
    
    This introduces a new technique for cyber-attack, named Cross Site Request Forgery, where a malicious site send a working client-side page that sneakily send certain request in hidden or tricky form that is automatically submitted without the user's consent. This technique is done, for instance, by sending JavaScript code that submits the form as soon as executed. The malicious request generated is still valid, since the request sender is the victim user, that has valid authorization through session ID cookies.
    
    The corresponding operation of the malicious request can be as dangerous as the attacker can construct. The attacker can sneak any operation as long as they know the request mechanisms along with the queries, which are easily-obtained information. Suppose an unintended operation of sending victim's whole bank account balance to attackers'. 

    One way to tackle CSRF vulnerability is to use CSRF token. CSRF token is a unique, long, unpredictable sequence of information, usually represented in hexadecimal, that is used to flag whether a POST or another state-changing request comes from trustworthy source, not malicious one.This token 'differentiates' valid and invalid POST requests. Whenever the server sends the client a form with state-changing method, the form is embedded with CSRF token that the user will send back. The server then will match the CSRF token from the request with the one that it has just generated. The state-changing request is valid if and only if the tokens match.

    Django framework abstracts the mechanism of CSRF token, packaging it inside `csrf_token` statement inside HTML form tags.

    With CSRF token, server can prevent malicious request from being processed and triggering some unintended operations in the name of victim client. CSRF token ensures that confidential POST requests are unavailable cross-sites.

    In the case where we don't include `{% csrf_token %}` statement within the `<form>` tag, Django still demands valid CSRF token for state-changing requests. However, the valid form won't be embedded with CSRF token, thus the request will yield in 403 Forbidden Error. 

    If we force the server not to demand valid CSRF token by imposing certain decorators on request handler method on `views.py`, the vulnerability of sites from CSRF attack is still persistent, thus posing risks to users.

5. How do you implement each checkpoint? Explain in step-by-step manner!
    
    * Create a form to add model object
        
        1. Define a subclass of `django.forms.ModelForm`, `ProductForm`, that wraps `Product` model as form class.
        2. Define fillable attributes for `ModelForm`, such as `name`, `price`, and `description`.
        3. Create a handler function `create_product` that will create an instance of `ModelForm`, with pre-filled key-values (the arguments) those from POST request parameters or `None`, indicating plain form instantiation. If the request is POST, which means that the form has already been sent, the values will be examined and validated. If they are valid, `Product` will be created through `<model_form_instance>.save()` and stored in database. Otherwise, the form will be returned again to the client for them to fill in correctly through `render(request, 'create-product.html, dict('form' = <model_form_instance>))`.
        4. Define a routing with path `create-product` relative to main application path prefix, that will be handled with `create-product` function that has just been created.
        5. Create a HTML file inside templates directory inside main application named `create-product.html` that displays form as dynamic content in `table` tags.
        6. Register `Product` model in main application `admin.py` by stating `admin.site.register(Product)` and create super user in terminal to access django's built-in admin site application for ensuring whether product creation has been successfully implemented.

    * Define a functionality to deliver every or specific `Product` entry, in XML or JSON format.

        1. Create two functions in `views.py`, `show-products(request)` and `show-product-by-id(request, pk)` that retreives all `Product` entries or specific, filtered entry whose primary key equals to `pk` from the function parameter. The entry or entries then will be serialized by `django.core.serializers.serialize()`. The serialization format depends on the GET request query, which is either `'json'` or `'xml'`. The serialized entry or entries then will be in form of string and returned as `HttpResponse` with appropriate content type.
        2. Create a routing with path `show-products`, that uses `show-products` function as the handler. Create another routing with path `show-product-by-id/<str:pk>`, that parameterize the second path as the primary key to pass as the `pk` parameter in `show-product-by-id` function.  

### Received Data through Postman Screenshoots

1. Retreival of every product in JSON
![Retreival of every product in JSON](/res/images/show-products-json.png) 
2. Retreival of every product in XML
![Retreival of every product in XML](/res/images/show-products-xml.png)
3. Retreival of specific product by ID in JSON
![Retreival of every product in JSON](/res/images/show-product-by-id-json.png) 
4. Retreival of specific product by ID in XML
![Retreival of every product in XML](/res/images/show-product-by-id-xml.png)






