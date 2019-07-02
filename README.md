# MultithreadCacheBlogAPI

    Backend Assessment - Blog Posts
    -------------------------------

    Django Framework API that fetches data from another API:
    https://ha_____ys.io/api/assessment/blog/posts?tag=tech

    The source API can only filter one tag at a time - notice that the field “tag” is singular and not plural.
    It will return a JSON object with an array of blog posts.

![Array of blog posts](images\PostByTag.PNG)

    API has the following routes:
    - /api/ping
![Ping Route](images\PingRoute.PNG)

    - /api/posts
![Posts Route](images\PostsRoute.PNG)

    Successful Response:
    The response of the API will be a list of all the blog posts that have at least one tag
    specified in the tags parameter.
    The sortBy parameter specifies which parameter should be used to sort the results
    return. It is an optional parameter, with a default value of `id`.
    The direction parameter specifies if the results should be returned in ascending
    order (if the value is "asc") or descending order (if the value is "desc"). The default
    value of the direction parameter is `asc`.

    Examples:

![Responses](images\Responses.PNG)


    Implementation:
    ---------------
    ● For every tag specified in the tags parameter, all posts with that tag using
    the Ha______s API fetched ( make a separate API request for every tag specified)
    ● All the results from the API requests combined and all the repeated
    posts removed.
    ● API requests sent with multithreading
    ● Unittests for URLs implemented
    ● Memcached caching used to reduce the number of calls to a server?

    
    Installation instructions are for WINDOWS OS:
    ---------------------------------------------
    If you use different OS and need assistance how to install, 
    please let me know

    To install (all needed installations are in requirements.txt):
    --------------------------------------------------------------
    cd MultithreadCacheBlogAPI


    create virtual environment:
    ---------------------------
    python -m venv myvenv


    activate virtual environment:
    -----------------------------
    myvenv\Scripts\activate


    install pip:
    ------------
    python -m pip install --upgrade pip


    install using requirements.txt file:
    ------------------------------------
    pip install -r requirements.txt


    To start the project:
    ---------------------
    cd MultithreadCacheBlogAPI
    python manage.py runserver


    To run API using urls:
    ----------------------
    open the following URL:
    http://127.0.0.1:8000

    Here you will find examle links mapped between Original Solution URLs
    and Django API URLs


    Instructions for Django urls (Concatenate http://127.0.0.1:8000 with any of the following ):
    --------------------------------------------------------------------------------------------

    #  Request 						                            Django URL
    --------------------------------------------------------------------------
    1  ping 						                            /api/ping/
    2  One tag: tech 					                        /api/posts/tags=tech
    3  Two tags: tech,history 				                    /api/posts/tags=tech,history
    4  One tag, sorted by likes with default direction (asc)    /api/posts/tags=tech/sortBy=likes
    5  Two tags, sorted by likes with default direction (ASC)   /api/posts/tags=tech,science/sortBy=likes
    6  One tag, sorted by reads in ASC direction 		        /api/posts/tags=tech/sortBy=reads/sortDirection=asc
    7  Two tag, sorted by reads in ASC direction 		        /api/posts/tags=tech,culture/sortBy=reads/sortDirection=asc
    8  Two tag, sorted by popularity in DESC direction 	        /api/posts/tags=tech,culture/sortBy=popularity/sortDirection=desc

    
    To test (run file test.py located in folder blog):
    --------------------------------------------------
    cd MultithreadCacheBlogAPI
    python manage.py test blog.tests     
