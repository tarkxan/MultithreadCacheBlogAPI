
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from timeit import default_timer
from threading import Thread
from django.views.decorators.cache import cache_page

def welcome(request):

    # return HttpResponse('Welcome!')
    return render(request,
                  'index.html',
                  {})

def ping(request):

    base_url = 'https://hatchways.io/api/assessment/blog/posts?tag='
    url = base_url + '/ping'
    response = requests.get(url)
    return JsonResponse({'Body': {"success": True if response.status_code == 200 else False},
                         'Status': response.status_code})

def mt_worker(response,
              idx,
              f,
              *args):

    response[idx] = f(*args).json()

# multi-threading solution
# save cache 30 minutes (60 seconds * 30)
@cache_page(60*30)
def posts(request,
          tags = None,
          sortBy = None,
          sortDirection = None):

    # if no tags provided - return error_400
    try:
        tag_lst = [tags_ls.split(',') for tags_ls in tags.split('=')][1]

    except:
        return JsonResponse({'Body': {"error": "Tags parameter is required"},
                             'Status': 400})

    # if tag value is invalid
    if not tag_lst or not tag_lst[0].isalpha():
        return JsonResponse({'Body': {"error": "Tags parameter is required"},
                             'Status': 400})

    # optional, if exists - check is valid
    if sortBy:
        try:
            sortBy = sortBy.split('=')[1]
        except:
            return JsonResponse({'Body': {"error": "sortBy parameter is invalid"},
                                 'Status': 400})

    # optional, if exists - check is valid
    if sortDirection:
        try:
            sortDirection = sortDirection.split('=')[1]
        except:
            return JsonResponse({'Body': {"error": "sortBy parameter is invalid"},
                                 'Status': 400})

    fields = ['id', 'author', 'authorid', 'likes', 'popularity', 'reads', 'tags']
    directions = ['asc', 'desc']

    # return error_400 if provided values are not valid
    if (sortBy and sortBy not in fields) or (sortDirection and sortDirection not in directions):
        return JsonResponse({'Body': {"error": "sortBy parameter is invalid"},
                             'Status': 400})

    # mutlithreading
    total_start_time = default_timer()
    threads = [None] * len(tag_lst)
    response = [None] * len(tag_lst)

    # Init and start processes
    for i, tag in enumerate(tag_lst):

        base_url = 'https://hatchways.io/api/assessment/blog/posts?tag='
        url = base_url + tag

        threads[i] = Thread(target=mt_worker, args=(response, i, requests.get, url))
        threads[i].start()

    # Wait for the processes to finish
    for i, tag in enumerate(tag_lst):
        threads[i].join()

        elapsed = default_timer() - total_start_time
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(tag, time_completed_at))

    data = response

    posts_lst = list()
    posts_dct = dict()

    # create a list of unique posts
    for tag_data in data:

        for post in tag_data['posts']:

            if not posts_dct.get(post['id']):
                posts_dct[post['id']] = True
                posts_lst.append(post)

    # if sortBy not provided - return unsorted data
    if not sortBy:
        return JsonResponse({'Body': {"posts": posts_lst},
                             'Status': 200})

    # if sortDirection not provided - default is asc
    if not sortDirection or sortDirection == 'asc':
        return JsonResponse({'Body': {"posts": sorted(posts_lst, key=lambda dct: dct[sortBy])},
                             'Status': 200})

    elif sortDirection == 'desc':
        return JsonResponse({'Body': {"posts": sorted(posts_lst, key=lambda dct: dct[sortBy], reverse=True)},
                             'Status': 200})

def error_404(request,
              exception):

    return JsonResponse({'Body': {"error": "Tags parameter is required"},
                         'Status': 400})