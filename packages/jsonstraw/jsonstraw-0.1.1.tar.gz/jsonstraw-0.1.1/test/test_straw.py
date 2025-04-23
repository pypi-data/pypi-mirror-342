import os

from jsonstraw import read_json_chunk

dir = os.path.dirname(os.path.realpath(__file__))

def generate_test_file(filename: str, key: str = 'data', length: int = 1000000):
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'w') as f:
        f.write('{\n')
        f.write(f'  "{key}": [\n')

        for i in range(length):
            f.write('    {\n')
            f.write(f'      "name": "Bob", \n')
            f.write(f'      "email": "bob_{i}@example.com", \n')
            f.write(f'      "date_of_birth": "1970-01-01", \n')
            f.write(f'      "id": {i},\n')
            f.write('      "role": "user"\n')
            f.write('    },\n')

        f.write('  ]\n')
        f.write('}')


def test_read_small_file():

    has_run = False
    for output in read_json_chunk(f"{dir}/small.json", key = 'data'):
        assert len(output) == 3
        assert output[0]['name'] == 'Bob'
        has_run = True

    assert has_run

def test_read_small_file_in_chunks():
    first_loop = True
    for output in read_json_chunk(f"{dir}/small.json", key = 'data', chunk_size = 2):
        if first_loop:
            assert len(output) == 2
            assert output[0]['name'] == 'Bob'
            first_loop = False
        else:
            assert len(output) == 1
            assert output[0]['name'] == 'Greg'

def test_read_large_file():
    generate_test_file(f"{dir}/large1.json", length=10000000)

    for output in read_json_chunk(f"{dir}/large1.json", key = 'data', chunk_size=1000):
        assert len(output) == 1000
        assert output[0]['name'] == 'Bob'
