import json
import random
import sys
import os


def getPath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # base_path = sys._MEIPASS
        base_path = os.path.abspath(".")

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


with open(getPath('knjiga.json')) as f:
    knjiga = json.load(f)


def getRandomZad():
    # get random object from knjiga
    radnomNumber = random.randint(0, len(knjiga)-1)

    obj = knjiga[radnomNumber]
    cjelina, lekcija, podlekcija = obj['cjelina'], obj['lekcija'], obj['podlekcija']

    # rjesenja array to rjesenja links
    rjesenja = [getPath('rjesenja/{}.jpg'.format(r))
                for r in obj['rjesenja']]

    # get random zadatak & zadatak array to zadatak link
    zad = random.choice(obj['zadatci'])
    zadatak = getPath(
        'book/{}/{}/{}/{}.jpg'.format(cjelina, lekcija, podlekcija, zad))

    res = {
        'zadatak': zadatak,
        'rjesenja': rjesenja,
        'cjelina': cjelina,
        'lekcija': lekcija,
        'podlekcija': podlekcija
    }

    return res


def removeZadatak(zadatakLink):
    # get data from zadatak link
    _, cjelina, lekcija, podlekcija, zadatak = zadatakLink.split('/')
    zadatak = zadatak.split('.')[0]

    for i in range(len(knjiga)):
        obj = knjiga[i]

        # check if obj is same
        if obj['cjelina'] == cjelina and obj['lekcija'] == lekcija and obj['podlekcija'] == podlekcija:
            knjiga[i]['zadatci'].remove(int(zadatak))

    # update file knjiga
    with open('knjiga.json', 'w') as json_file:
        json.dump(knjiga, json_file)


def restartFile():
    # import template
    with open(getPath('knjigaTemplate.json')) as f:
        knj = json.load(f)

    # update knjiga to template
    with open(getPath('knjiga.json'), 'w') as json_file:
        json.dump(knj, json_file)
