from flask import request
import http as http
def paginar_10(response, ix):
        characters = []
        if ix > 0 and ix <10:
            try:
                if ix == 1:
                    for i in range(0, 10):
                        if response[i]['publish'] == True:
                            character = response[i]
                            characters.append(character)
                        else:
                            continue
                else:
                    for i in range((10*ix)-10, (ix*10)):
                        if response[i]['publish'] == True:
                            character = response[i]
                            characters.append(character)
                        else:
                            continue
            except IndexError:
                    pass
        else:
            message = {'message': 'Resource Not Found: ' + request.url,'status' : 404},http.HTTPStatus.OK
            return message
        return characters

def searchReport(response, ix):
    characters = []
    for i in range(len(response)):
        if response[i]['publish'] == True:
            character = response[i]
            characters.append(character)
        else:
            continue
    character = characters[ix-1]
    return character