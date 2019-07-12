import requests
import os

def generate_files_from(file, output_type):
    filesParam = {'file': file}
    hetsapi_url = os.environ['HETSAPI_INTERNAL_URL']
    th_generator_url = f"http://{hetsapi_url}/generator/{output_type}"
    res = requests.post(th_generator_url, files=filesParam)
    if res.status_code != 204:
        raise Exception(f'could not generate .{output_type} files.')


def get_generic_filename_for(file):
    # remove path from filename
    base_filename = os.path.basename(file.name)
    # remove ending from filename
    return os.path.splitext(base_filename)[0]
