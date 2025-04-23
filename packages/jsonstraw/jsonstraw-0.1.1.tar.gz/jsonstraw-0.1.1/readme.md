# Json Straw

A simple library to read massive JSON files.

## What is it for?

Working with large JSON files is hard. It normally requires you to load the entire file into memory and use the `json` library to parse it. The problem is that loading the whole file is a challenge with very large JSON.

To solve this problem `jsonstraw` will read the file line by line, parse a number of objects and return them as an iterator.

## Example

Image we need to parse a large file like this:

```json
{
  "data": [
    {
      "name": "Bob",
      "id": 0,
      "role": "user"
    },
    {
      "name": "Sue",
      "id": 1,
      "role": "user"
    },
    {
      "name": "Alan",
      "id": 2,
      "role": "user"
    }
    // plus 10,000,000 more
  ]
}
```

We have a large JSON document with a list of data that we need to parse.

```python
from jsonstraw import read_json_chunk

for output in read_json_chunk("large_file.json", key = 'data', chunk_size=1000):
    assert len(output) == 1000
```

We can use an iterator to read the JSON file. It will parse each object, convert it to a `dict` and provide lists based on your `chunk_size`.