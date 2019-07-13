import requests
import os
import glob

hetsapi_url = os.environ['HETSAPI_INTERNAL_URL']

def generate_th_files_from(file):
    generated_files = generate_files_from(file, 'th')
    print(generated_files)
    return generated_files


def generate_files_from(file, output_type):
    filesParam = {'file': file}
    th_generator_url = f"http://{hetsapi_url}/generator/{output_type}"
    print(f'requst to hets to generate .{output_type} files.')
    res = requests.post(th_generator_url, files=filesParam)
    if res.status_code != 204:
        raise Exception(f'could not generate .{output_type} files.')

    generated_filepaths = glob.glob(f'/data/{output_type}/*.{output_type}')
    return list(map(lambda filepath: open(filepath), generated_filepaths))


def get_generic_filename_for(file):
    # remove path from filename
    base_filename = os.path.basename(file.name)
    # remove ending from filename
    return os.path.splitext(base_filename)[0]
