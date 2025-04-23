from typing import Optional
import json

def read_json_chunk(file: str, chunk_size: int = 1000, key: Optional[str] = None):
    """
    Reads a JSON file incrementally in chunks, parsing individual JSON objects
    from within a list and handling large files efficiently. The function yields
    chunks of JSON objects of the specified size. Optionally, it can start reading
    from a specific key within a JSON structure.

    :param file: The path to the JSON file to read. Must be a file containing
                 valid JSON format.
    :type file: str
    :param chunk_size: The number of JSON objects to include in each chunk before
                       yielding. Defaults to 1000 if not specified.
    :type chunk_size: int
    :param key: An optional key within the JSON structure to locate the array to
                process. If None, the function assumes the JSON structure begins
                with a list.
    :type key: Optional[str]
    :return: Yields a list of parsed JSON objects within each chunk of the
             specified size. Empty lists are not yielded.
    :rtype: Generator[List[dict], None, None]
    """

    has_started_list = False
    has_started_object = False
    string_buffer = ''
    output = []
    with open(file, 'r') as f:

        line = f.readline()
        while line:

            contents = line.strip()

            if has_started_list:
                if not has_started_object:
                    if contents.startswith('{'):
                        string_buffer += contents
                        has_started_object = True
                else:
                    if contents.startswith('}'):
                        string_buffer += '}'
                        has_started_object = False
                        output.append(json.loads(string_buffer))
                        string_buffer = ''

                        if len(output) >= chunk_size:
                            yield output
                            output = []

                    else:
                        string_buffer += contents

            if not has_started_list:
                if key is None and contents == '[':
                    has_started_list = True

                elif key is not None and contents.startswith(f'"{key}":'):
                    has_started_list = True

            line = f.readline()

        if len(output) > 0:
            yield output
