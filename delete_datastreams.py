import yaml
import urllib
import xmltodict
import json
import requests

credentials = yaml.load(open('configuration.yaml', 'r'))
collection = "pid%7E{0}%2A".format(credentials['collection_namespace'])
data_stream = credentials['datastream']
find_objects_string = credentials['fedoraurl'] + ":8080/fedora/objects?query=" + collection \
                      + "&pid=true&resultFormat=xml"
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


def purge_a_dsid(pids):
    purge_url = credentials['fedoraurl'] + ":8080/fedora/objects/"
    deleted_pids = []
    for pid in pids:
        url = purge_url + pid + '/datastreams/{0}/?&startDT={1}&endDT={2}&logMessage'.format(credentials['datastream'], credentials['start'], credentials['end'])
        x = requests.delete(url, auth=(credentials['username'], credentials['password']))
        if x.status_code == 200:
            deleted_pids.append(pid)
        else:
            print("{0} had a status code of: {1}".format(pid, x.status_code))
    return deleted_pids


if __name__ == "__main__":
    pids_in_collection = get_collection_objects(find_objects_string, initial_token, collection_objects)
    deleted_objects = purge_a_dsid(pids_in_collection)
