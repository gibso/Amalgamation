from flask import Blueprint, request, jsonify
import tempfile
import json
from amalgamation import settings, run_blending

bp = Blueprint('amalgamation', __name__)


@bp.route('/amalgamation', methods=['POST'])
def run_amalgamation():
    input_spec_file = save_request_file_temporary(request)
    input_space_names = json.loads(request.form.get('input-space-names'))

    settings.inputFile = input_spec_file.name
    settings.inputSpaceNames = input_space_names

    append_input_data_to_settings(input_spec_file, input_space_names)
    run_blending.run_blending()
    remove_input_data_from_settings()

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


# this is reeaally hacky, but at the moment
# i dont see an other way to inform the
# clingo process about the input space data
def append_input_data_to_settings(input_spec_file, input_space_names):
    settings_file = open('amalgamation/settings.py', 'a')
    settings_file.write(f'inputFile = "{input_spec_file.name}"\n'
                        f'inputSpaceNames = ["{input_space_names[0]}", "{input_space_names[1]}"]\n')
    settings_file.close()


def remove_input_data_from_settings():
    settings_file = open('amalgamation/settings.py')
    lines = settings_file.readlines()
    settings_file.close()
    settings_file = open('amalgamation/settings.py', 'w')
    settings_file.writelines([item for item in lines[:-2]])
    settings_file.close()
