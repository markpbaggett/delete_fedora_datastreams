import yaml
import urllib
import xmltodict
import json
import requests

credentials = yaml.load(open('configuration.yaml', 'r'))
collection = "pid%7E{0}%2A".format(credentials['collection_namespace'])
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
    if isinstance(object_lists, list):
        for item in object_lists:
            pids.append(item['pid'])
    else:
        pids.append(object_lists['pid'])
    if new_token:
        token = '&sessionToken={0}'.format(new_token)
        get_collection_objects(url, token, pids)
    return pids


def purge_a_dsid(pids):
    purge_url = credentials['fedoraurl'] + ":8080/fedora/objects/"
    deleted_pids = []
    for pid in pids:
        last_version_date = get_last_version_date(pid)
        if last_version_date:
            number_of_versions = len(last_version_date) - 1
            end = last_version_date[1]
            start = last_version_date[number_of_versions]
            url = '{0}{1}/datastreams/{2}/?&startDT={3}&endDT={4}' \
                  '&logMessage'.format(purge_url, pid, credentials['datastream'], start, end)
            x = requests.delete(url, auth=(credentials['username'], credentials['password']))
            if x.status_code == 200:
                if len(repr(x.text)) > 4:
                    deleted_pids.append("{0}:  {1}".format(pid, repr(x.text)))
            else:
                print("{0} had a status code of: {1}".format(pid, x.status_code))
    return deleted_pids


def build_markdown_file(array_of_pids):
    markdown_file = open('deleted_pids.md', 'w')
    markdown_file.write('# Deleted PIDS:\nVersions of the {0} datastream were deleted'
                        ' for the following PIDS:\n\n'.format(credentials['datastream']))
    for pid in array_of_pids:
        markdown_file.write('1. {0}\n'.format(pid))
    markdown_file.close()
    print("\n\tDeleted datastream versions for {0} pids.\n\t"
          "See deleted_pids.md for more details.\n".format(len(array_of_pids)))


def get_last_version_date(fedora_object):
    url = '{0}:8080/fedora/objects/{1}/datastreams/' \
          '{2}/history?format=xml'.format(credentials['fedoraurl'], fedora_object, credentials['datastream'])
    s = requests.get(url, auth=(credentials['username'], credentials['password']))
    if s.status_code == 200:
        x = s.text
        json_string = json.dumps(xmltodict.parse(x))
        data = json.loads(json_string)
        versions = []
        for objects in data['datastreamHistory']['datastreamProfile']:
            if type(objects) == dict:
                versions.append(objects['dsCreateDate'])
        versions.sort(reverse=True)
        return versions


if __name__ == "__main__":
    pids_in_collection = get_collection_objects(find_objects_string, initial_token, collection_objects)
    deleted_objects = purge_a_dsid(pids_in_collection)
    build_markdown_file(deleted_objects)
