import yaml
import requests

credentials = yaml.load(open('credentials.yaml', 'r'))
fedora_url = credentials['fedoraurl']
user_name = credentials['username']
password = credentials['password']
collection = "pid%7E{0}%2A".format(credentials['collection_namespace'])
data_stream = credentials['datastream']
find_objects_string = fedora_url + ":8080/fedora/objects?query=" + collection + "&pid=true&resultFormat=xml"


def get_collection_objects():
    return


def purge_a_dsid():
    return

if __name__ == "__main__":
    get_collection_objects(find_objects_string)
