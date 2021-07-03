import requests
import config

# GLOBAL CONSTANTS
search_url = 'https://api.thedogapi.com/v1/breeds/search?q='
image_url = 'https://api.thedogapi.com/v1/images/'
rand_dog_url = image_url + 'search'

def request_breed(breed: str) -> str:
    """
    Makes request to The Dog API and searches for a breed. 
    param breed: breed of dog to search for
    return: reference image id for the dog if it exists, else None
    """
    try:
        res = requests.get(search_url + breed)
    except:
        return

    # when an error occurs, exit
    if res.status_code != requests.codes.ok:
        print('error')
        return

    obj = res.json()

    # get an image id from the list
    id = search_image(obj)
    
    # return id for next API call
    if id:
        return get_image_url(id)


def search_image(arr: list) -> str:
    """
    Searches an array of dictionaries searching for a reference image key.
    Returns the first image id it finds.
    param arr: list of dictionaries
    return: image id
    """
    # search results are empty
    if not arr:
        return
    
    # search for an object that contains an image id
    # if none are found, just exit
    for obj in arr:
        if 'reference_image_id' in obj:
            return obj['reference_image_id']

def get_image_url(id: str) -> str:
    """
    Makes request to The Dog API to get an image from the id.
    param id: image id to search for
    return: URL of image
    """
    try:
        res = requests.get(image_url + id)
    except:
        return

    # exit when there was an error
    if res.status_code != requests.codes.ok:
        return
    
    obj = res.json()
    
    # the object will have a 'url' key which holds the image url
    return obj['url']

def get_random_dog() -> str:
    """
    Gets a random dog picture.
    return: url of random dog picture
    """
    try:
        res = requests.get(rand_dog_url)
    except:
        return
    
    # exit if error
    if res.status_code != requests.codes.ok:
        return
    
    obj = res.json()
    return obj[0]['url']
