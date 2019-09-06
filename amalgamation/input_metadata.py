import json


class InputMetadata:

    # input_metadata_file = open("/data/input.json", "r")
    # input_metadata = json.loads(input_metadata_file.read())
    # inputFile = input_metadata['inputFile']
    # inputSpaceNames = input_metadata['inputSpaceNames']

    def __init__(self):
        input_metadata_file = open("/data/input.json", "r")
        metadata = json.loads(input_metadata_file.read())
        self.inputFile = metadata['inputFile']
        self.inputSpaceNames = metadata['inputSpaceNames']
