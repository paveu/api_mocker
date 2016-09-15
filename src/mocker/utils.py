import requests

def make_callback(callback_api, return_content_type, data):
    """
    Make callback API
    """
    if callback_api:
        callback_header = {'Content-type': str(return_content_type)}
        callback = requests.post(callback_api, data=data, headers=callback_header)
        #TODO: add handler for status codes
        return callback.status_code

def handler_http_methods(request_method, url):
    if request_method == "GET":
        r = requests.get(url, headers=destination_header)
        if r.status_code == requests.codes.ok:
            if callback_api:
                make_callback(callback_api, return_content_type, data=json.dumps(r.json()))
            return JsonResponse(json.dumps(r.json()), safe=False, status=r.status_code)
        else:
            return JsonResponse({"status": "Error"}, status=r.status_code)
    elif request_method == "POST":
        r = requests.post(url, headers=destination_header)
        if r.status_code == requests.codes.ok:
            if callback_api:
                make_callback(callback_api, return_content_type, data=json.dumps(r.json()))
            return JsonResponse(json.dumps(r.json()), safe=False, status=r.status_code)
        else:
            return JsonResponse({"status": "Error"}, status=r.status_code)            
    elif request_method == "PATCH":
        r = requests.patch(url, headers=destination_header)
        if r.status_code == requests.codes.ok:
            if callback_api:
                make_callback(callback_api, return_content_type, data=json.dumps(r.json()))
            return JsonResponse(json.dumps(r.json()), safe=False, status=r.status_code)
        else:
            return JsonResponse({"status": "Error"}, status=r.status_code)