from flask_api import status
import json


def test_tritone_demo(client):
    # open file as binary
    file = open('tests/examples/music/tritone_demo.casl', 'rb')
    data = {
        'file': file,
        'input-space-names': json.dumps(['G7', 'Bbmin'])
    }
    response = client.post('/amalgamation', data=data, content_type='multipart/form-data')

    assert response.status_code == status.HTTP_200_OK
    assert list(response.json[0].keys()) == ['blend', 'blendId', 'blendName', 'cost', 'genericSpace', 'input1', 'input2']
    assert response.json[0]['blendName'] == 'Blend_v39__G7_0_Bbmin_0'


def test_house_boat(client):
    # open file as binary
    file = open('tests/examples/concept_net/house_boat_minimal.casl', 'rb')
    data = {
        'file': file,
        'input-space-names': json.dumps(['House', 'Boat'])
    }
    response = client.post('/amalgamation', data=data, content_type='multipart/form-data')

    assert response.status_code == status.HTTP_200_OK
    assert list(response.json[0].keys()) == ['blend', 'blendId', 'blendName', 'cost', 'genericSpace', 'input1', 'input2']
    assert response.json[0]['blendName'] == 'Blend_v8__House_0_Boat_0'
