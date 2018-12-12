import json


def test_successfulmerge():
    objects = json.loads('[{"firstname":"a", "lastname":"b", "uid":"c"}, {"firstname":"a", "lastname":"b", "income":9999}]')
    keys = json.loads('["firstname","lastname"]')
