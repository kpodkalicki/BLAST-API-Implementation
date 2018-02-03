_PARAMS = None


class Response:
    def __init__(self, text) -> None:
        self.text = text


def toggle_params(params=None):
    old_params = toggle_params.params
    toggle_params.params = params
    return old_params


toggle_params.params = None


def get(url, params):
    response = None
    if params['CMD'] == 'Put':
        response = Response('<!--QBlastInfoBegin\nRID=1337\nRTOE=17\nQBlastInfoEnd\n-->')

    elif params['CMD'] == 'Get':
        if 'FORMAT_OBJECT' in params and params['FORMAT_OBJECT'] == 'SearchInfo':
            status = 'WAITING' if get.waiting else 'READY'
            get.waiting = not get.waiting
            response = Response('<!--QBlastInfoBegin\nStatus={0}\nQBlastInfoEnd\n-->'.format(status))

        else:
            response = Response(params['FORMAT_TYPE'] + '_RESPONSE')

    toggle_params(params)
    return response


get.waiting = True
