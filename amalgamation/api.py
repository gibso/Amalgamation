from flask import Blueprint, request, jsonify
import tempfile
import json
from amalgamation import run_blending
import os
import glob

bp = Blueprint('amalgamation', __name__)


@bp.route('/amalgamation', methods=['POST'])
def run_amalgamation():
    remove_all_output_files()

    input_spec_file = save_request_file_temporary(request)
    input_space_names = json.loads(request.form.get('input-space-names'))
    save_input_metadata(input_spec_file, input_space_names)

    run_blending.run_blending()

    blendFile = open('/data/blend.json')
    blend = json.loads(blendFile.read())
    blendFile.close()

    return jsonify(blend)


def save_request_file_temporary(request):
    request_file = request.files['file']
    tmpfile = tempfile.NamedTemporaryFile(suffix='.casl')
    request_file.seek(0)
    tmpfile.write(request_file.read())
    tmpfile.seek(0)
    return tmpfile


def save_input_metadata(input_spec_file, input_space_names):
    f = open("/data/input.json", "w+")
    metadata = {
        'inputFile': input_spec_file.name,
        'inputSpaceNames': input_space_names
    }
    f.write(json.dumps(metadata))
    f.close()


def remove_all_output_files():
    fileList = glob.glob(f'/data/*')
    for fileName in fileList:
        os.remove(fileName)
