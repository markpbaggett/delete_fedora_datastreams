import yaml
import urllib
import xmltodict
import json

credentials = yaml.load(open('credentials.yaml', 'r'))
collection = "pid%7E{0}%2A".format(credentials['collection_namespace'])
data_stream = credentials['datastream']
find_objects_string = credentials['fedoraurl'] + ":8080/fedora/objects?query=" + collection \
                      + "&pid=true&resultFormat=xml&maxResults=2"
collection_objects = []
initial_token = ''

def get_collection_objects(url, token, pids):
    x = urllib.request.urlopen(url + token)
    s = x.read()
    json_string = json.dumps(xmltodict.parse(s))
    data = json.loads(json_string)
    new_token = ''
    if 'listSession' in data['result']:
        new_token = data['result']['listSession']['token']
    object_lists = data['result']['resultList']['objectFields']
    for item in object_lists:
        pids.append(item['pid'])
    if new_token:
        token = '&sessionToken={0}'.format(new_token)
        get_collection_objects(url, token, pids)
    return pids


def purge_a_dsid():
    return

if __name__ == "__main__":
    pids_in_collection = get_collection_objects(find_objects_string, initial_token, collection_objects)
    print(pids_in_collection)