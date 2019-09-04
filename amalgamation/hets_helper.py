import requests
import os
import glob

hetsapi_url = os.environ['HETSAPI_INTERNAL_URL']


def generate_th_files_from(file):
    return generate_files_from(file, 'th')


def generate_xml_file_from(file):
    return generate_files_from(file, 'xml')[0]


def generate_files_from(file, output_type):
    filesParam = {'file': file}
    th_generator_url = f"http://{hetsapi_url}/generator/{output_type}"
    print(f'request to hets to generate .{output_type} files.')
    res = requests.post(th_generator_url, files=filesParam)
    if res.status_code != 204:
        raise Exception(f'could not generate .{output_type} files.')

    output_filepaths = glob.glob(f'/data/*.{output_type}')
    generic_filename = get_generic_filename_for(file=file)
    generated_filepaths = list(filter(lambda filepath: generic_filename in filepath, output_filepaths))

    return list(map(lambda filepath: open(filepath), generated_filepaths))


def get_generic_filename_for(file=None, filename=None):
    if file:
        return get_generic_filename_for(filename=file.name)
    # remove path from filename
    base_filename = os.path.basename(filename)
    # remove ending from filename
    return os.path.splitext(base_filename)[0]
