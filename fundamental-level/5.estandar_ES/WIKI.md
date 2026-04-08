# Python: `pathlib` and File Handling

## 1. What Is `pathlib`?

`pathlib` is Python’s object-oriented filesystem path library.

It lets you work with files and directories using path objects instead of plain strings.

This usually makes code:
- cleaner
- easier to read
- more portable between operating systems

---

## 2. Why Use `pathlib`?

`pathlib` is often easier to use than older approaches like `os.path`.

Instead of writing:

```python
import os

path = os.path.join("data", "report.txt")
```

You can write:

```python
from pathlib import Path

path = Path("data") / "report.txt"
```

This is usually more readable.

---

## 3. Importing `Path`

```python
from pathlib import Path
```

`Path` is the class you will use most of the time for working with filesystem paths.

---

## 4. Creating Paths

```python
from pathlib import Path

file_path = Path("notes.txt")
folder_path = Path("data")
nested_path = Path("data") / "reports" / "summary.txt"
```

The `/` operator joins path parts in a clean and cross-platform way.

---

## 5. Absolute and Relative Paths

A path can be relative:

```python
from pathlib import Path

path = Path("data/report.txt")
print(path)
```

Or absolute:

```python
from pathlib import Path

path = Path("/home/user/data/report.txt")
print(path)
```

You can also resolve a path:

```python
from pathlib import Path

path = Path("data/report.txt")
print(path.resolve())
```

---

## 6. Common `Path` Properties

```python
from pathlib import Path

path = Path("data/report.txt")

print(path.name)       # report.txt
print(path.stem)       # report
print(path.suffix)     # .txt
print(path.parent)     # data
```

These are useful for inspecting parts of a path.

---

## 7. Checking Whether Something Exists

```python
from pathlib import Path

path = Path("notes.txt")

print(path.exists())
```

This returns `True` if the path exists and `False` otherwise.

---

## 8. Checking File or Directory Type

```python
from pathlib import Path

path = Path("notes.txt")

print(path.is_file())
print(path.is_dir())
```

Use:
- `.is_file()` to check whether it is a file
- `.is_dir()` to check whether it is a directory

---

## 9. Creating Directories

```python
from pathlib import Path

folder = Path("output")
folder.mkdir()
```

To create nested directories:

```python
from pathlib import Path

folder = Path("output/reports/2026")
folder.mkdir(parents=True, exist_ok=True)
```

### Meaning
- `parents=True` creates missing parent folders
- `exist_ok=True` avoids an error if the folder already exists

---

## 10. Iterating Through a Directory

```python
from pathlib import Path

folder = Path("data")

for item in folder.iterdir():
    print(item)
```

This loops through the contents of the directory.

---

## 11. Finding Files with `glob()` and `rglob()`

```python
from pathlib import Path

folder = Path("data")

for file in folder.glob("*.txt"):
    print(file)
```

Recursive version:

```python
from pathlib import Path

folder = Path("data")

for file in folder.rglob("*.txt"):
    print(file)
```

### Difference
- `glob("*.txt")` searches only inside that folder
- `rglob("*.txt")` searches recursively inside subfolders too

---

## 12. Reading a Text File with `read_text()`

```python
from pathlib import Path

path = Path("notes.txt")
content = path.read_text(encoding="utf-8")
print(content)
```

This is a simple way to read a text file.

---

## 13. Writing a Text File with `write_text()`

```python
from pathlib import Path

path = Path("notes.txt")
path.write_text("Hello, Python", encoding="utf-8")
```

This writes text directly to the file.

If the file already exists, its content is replaced.

---

## 14. Reading and Writing Bytes

For binary data, use bytes methods.

```python
from pathlib import Path

path = Path("image.bin")
data = path.read_bytes()
```

```python
from pathlib import Path

path = Path("image.bin")
path.write_bytes(b"ABC")
```

Use this for:
- images
- PDFs
- ZIP files
- other binary formats

---

## 15. The Built-in `open()` Function

Even when using `pathlib`, you will often use `open()`.

```python
from pathlib import Path

path = Path("notes.txt")

with path.open("r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

Or with built-in `open()`:

```python
from pathlib import Path

path = Path("notes.txt")

with open(path, "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

Both are valid.

---

## 16. Why `with` Is Important

The `with` statement makes sure the file is closed automatically, even if an error happens.

```python
from pathlib import Path

path = Path("notes.txt")

with path.open("r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

This is safer than opening and closing files manually.

---

## 17. File Modes

Common file modes:

- `"r"` → read text
- `"w"` → write text, replacing existing content
- `"a"` → append text
- `"rb"` → read binary
- `"wb"` → write binary

### Examples

```python
with open("notes.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("New content")
```

```python
with open("notes.txt", "a", encoding="utf-8") as file:
    file.write("\nAnother line")
```

```python
with open("image.bin", "rb") as file:
    data = file.read()
```

---

## 18. Text Mode vs Binary Mode

### Text mode
- reads and writes `str`
- uses an encoding
- default mode when opening files

### Binary mode
- reads and writes `bytes`
- no text encoding parameter
- used for images, PDFs, ZIP files, and other binary data

---

## 19. Reading a Whole File

```python
from pathlib import Path

path = Path("notes.txt")

with path.open("r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

This is convenient for small files.

---

## 20. Reading Line by Line

```python
from pathlib import Path

path = Path("notes.txt")

with path.open("r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

Reading line by line is usually better for large files.

---

## 21. Writing Multiple Lines

```python
from pathlib import Path

lines = ["first line\n", "second line\n", "third line\n"]

with Path("notes.txt").open("w", encoding="utf-8") as file:
    file.writelines(lines)
```

### Important
`writelines()` does not automatically add newline characters, so you usually include `\n` yourself.

---

## 22. Appending to a File

```python
from pathlib import Path

with Path("log.txt").open("a", encoding="utf-8") as file:
    file.write("New log entry\n")
```

Append mode adds content to the end of the file instead of replacing it.

---

## 23. Renaming and Moving Files

```python
from pathlib import Path

source = Path("old_name.txt")
target = Path("new_name.txt")

source.rename(target)
```

This can be used to rename files and, in many cases, move them too.

---

## 24. Replacing Files

```python
from pathlib import Path

source = Path("temp.txt")
target = Path("final.txt")

source.replace(target)
```

This replaces the target if it already exists.

---

## 25. Deleting Files and Directories

Delete a file:

```python
from pathlib import Path

path = Path("notes.txt")
path.unlink()
```

Delete an empty directory:

```python
from pathlib import Path

folder = Path("empty_folder")
folder.rmdir()
```

### Important
- `.unlink()` removes a file
- `.rmdir()` removes an empty folder only

---

## 26. Getting File Information

```python
from pathlib import Path

path = Path("notes.txt")
stats = path.stat()

print(stats.st_size)
```

This gives file metadata such as:
- size
- timestamps
- other filesystem information

---

## 27. Good Practice: Always Specify Encoding for Text

For text files, a good default is:

```python
from pathlib import Path

with Path("notes.txt").open("r", encoding="utf-8") as file:
    content = file.read()
```

Using `encoding="utf-8"` helps avoid platform-related encoding problems.

---

## 28. Common Beginner Mistakes

### Using string paths everywhere

Less clear:

```python
path = "data/report.txt"
```

Often better:

```python
from pathlib import Path

path = Path("data") / "report.txt"
```

### Forgetting `with`

```python
file = open("notes.txt", "r", encoding="utf-8")
content = file.read()
file.close()
```

Better:

```python
with open("notes.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

### Mixing text and binary logic

Wrong:

```python
with open("image.bin", "rb", encoding="utf-8") as file:
    data = file.read()
```

In binary mode, `encoding` is not used.

### Forgetting that `read()` may load the full file

```python
with open("huge.log", "r", encoding="utf-8") as file:
    content = file.read()
```

That may be inefficient for very large files.

### Manually concatenating paths

Less ideal:

```python
folder = "data"
file = "report.txt"
full_path = folder + "/" + file
```

Better:

```python
from pathlib import Path

full_path = Path("data") / "report.txt"
```

---

## 29. Summary

- `pathlib` provides object-oriented filesystem paths
- `Path` is the main class for everyday path handling
- Use `/` to join path parts cleanly
- Common methods include:
  - `.exists()`
  - `.is_file()`
  - `.is_dir()`
  - `.iterdir()`
  - `.glob()`
  - `.rglob()`
  - `.read_text()`
  - `.write_text()`
  - `.read_bytes()`
  - `.write_bytes()`
- Use `with` when opening files so they are closed automatically
- Text mode works with `str`
- Binary mode works with `bytes`
- `encoding="utf-8"` is usually the safest default for text files

# Python: CSV / JSON / YAML — Parsing and Serialization

## 1. What Are Parsing and Serialization?

These two ideas appear constantly when working with files, APIs, and data exchange.

### Parsing
Parsing means:
- reading external data
- converting it into Python objects

Examples:
- CSV text → lists or dictionaries
- JSON text → Python dicts/lists
- YAML text → Python dicts/lists

### Serialization
Serialization means:
- taking Python objects
- converting them into a storable or transferable format

Examples:
- Python dict → JSON string
- list of rows → CSV file
- config dict → YAML text

---

## 2. CSV, JSON, and YAML at a Glance

### CSV
CSV is a plain-text tabular format.

Best for:
- spreadsheets
- table-like data
- simple imports/exports

### JSON
JSON is a structured text format based on objects and arrays.

Best for:
- APIs
- configuration
- nested structured data

### YAML
YAML is a human-friendly serialization format often used for configuration.

Best for:
- config files
- readable structured data
- DevOps and infrastructure files

---

## 3. Working with CSV in Python

Python provides the built-in `csv` module.

```python
import csv
```

The `csv` module is designed for reading and writing CSV data.

---

## 4. Reading CSV with `csv.reader`

Use `csv.reader` when you want each row as a list.

### Example
```python
import csv

with open("users.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

### Example output
```python
['name', 'age', 'city']
['Janette', '24', 'Mexico City']
['Ana', '30', 'Puebla']
```

### Note
Each row is a list of strings.

---

## 5. Reading CSV with `csv.DictReader`

Use `DictReader` when the first row contains headers and you want dictionaries.

### Example
```python
import csv

with open("users.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)
```

### Example output
```python
{'name': 'Janette', 'age': '24', 'city': 'Mexico City'}
{'name': 'Ana', 'age': '30', 'city': 'Puebla'}
```

This is often easier to work with than plain lists.

---

## 6. Writing CSV with `csv.writer`

Use `csv.writer` when you want to write rows as lists.

### Example
```python
import csv

rows = [
    ["name", "age", "city"],
    ["Janette", 24, "Mexico City"],
    ["Ana", 30, "Puebla"]
]

with open("users.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
```

### Why `newline=""`?
When working with `csv`, using `newline=""` is the recommended pattern to avoid newline handling problems.

---

## 7. Writing CSV with `csv.DictWriter`

Use `DictWriter` when your data is in dictionary form.

### Example
```python
import csv

rows = [
    {"name": "Janette", "age": 24, "city": "Mexico City"},
    {"name": "Ana", "age": 30, "city": "Puebla"}
]

with open("users.csv", "w", encoding="utf-8", newline="") as file:
    fieldnames = ["name", "age", "city"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)
```

This is very useful when your Python data already uses dictionaries.

---

## 8. Custom Delimiters in CSV

Not all CSV files use commas.

Some use:
- `;`
- `\t`
- `|`

### Example with semicolon
```python
import csv

with open("users.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file, delimiter=";")

    for row in reader:
        print(row)
```

### Example with tab-separated values
```python
import csv

with open("users.tsv", "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file, delimiter="\t")

    for row in reader:
        print(row)
```

---

## 9. CSV Parsing Caveat

CSV data is usually read as strings.

```python
import csv

with open("users.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        age = int(row["age"])
        print(age)
```

If you need numbers, dates, or booleans, you often convert them manually.

---

## 10. Working with JSON in Python

Python provides the built-in `json` module.

```python
import json
```

JSON maps naturally to Python structures:

- JSON object → Python `dict`
- JSON array → Python `list`
- JSON string → Python `str`
- JSON number → Python `int` or `float`
- JSON boolean → Python `bool`
- JSON null → Python `None`

---

## 11. Parsing JSON with `json.loads()`

Use `json.loads()` when you already have a JSON string in memory.

### Example
```python
import json

text = '{"name": "Janette", "age": 24, "active": true}'
data = json.loads(text)

print(data)
print(type(data))
```

### Output
```python
{'name': 'Janette', 'age': 24, 'active': True}
<class 'dict'>
```

---

## 12. Parsing JSON Files with `json.load()`

Use `json.load()` when reading from a file.

### Example
```python
import json

with open("user.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data)
```

This reads the JSON file and converts it into Python objects.

---

## 13. Serializing to JSON with `json.dumps()`

Use `json.dumps()` when you want a JSON string.

### Example
```python
import json

data = {
    "name": "Janette",
    "age": 24,
    "active": True
}

text = json.dumps(data)
print(text)
print(type(text))
```

### Output
```python
{"name": "Janette", "age": 24, "active": true}
<class 'str'>
```

---

## 14. Writing JSON Files with `json.dump()`

Use `json.dump()` when writing JSON directly to a file.

### Example
```python
import json

data = {
    "name": "Janette",
    "age": 24,
    "skills": ["Python", "SQL", "React"]
}

with open("user.json", "w", encoding="utf-8") as file:
    json.dump(data, file)
```

---

## 15. Pretty JSON Output

For readable JSON, use `indent`.

```python
import json

data = {
    "name": "Janette",
    "age": 24,
    "skills": ["Python", "SQL", "React"]
}

print(json.dumps(data, indent=2))
```

### Example output
```json
{
  "name": "Janette",
  "age": 24,
  "skills": [
    "Python",
    "SQL",
    "React"
  ]
}
```

This is useful for:
- logs
- config files
- debugging
- readable exports

---

## 16. Keeping Unicode Characters Readable in JSON

By default, JSON serialization may escape some non-ASCII characters.

Use `ensure_ascii=False` to keep UTF-8 text more readable.

```python
import json

data = {"city": "México", "name": "José"}

text = json.dumps(data, ensure_ascii=False, indent=2)
print(text)
```

---

## 17. Common JSON Limitation

JSON only supports certain basic data types directly.

For example, this fails:

```python
import json
from datetime import datetime

data = {"created_at": datetime.now()}
# json.dumps(data)  # TypeError
```

That is because `datetime` is not JSON-serializable by default.

### Simple workaround
```python
import json
from datetime import datetime

data = {"created_at": datetime.now().isoformat()}
print(json.dumps(data, indent=2))
```

---

## 18. Custom Serialization in JSON

You can customize serialization using `default=`.

```python
import json
from datetime import datetime

def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type not serializable: {type(obj)}")

data = {"created_at": datetime.now()}

text = json.dumps(data, default=serializer, indent=2)
print(text)
```

---

## 19. Working with YAML in Python

YAML is not handled by the Python standard library in the same way as `csv` and `json`.

A common library is **PyYAML**.

### Installation
```bash
pip install pyyaml
```

### Import
```python
import yaml
```

---

## 20. Parsing YAML with `yaml.safe_load()`

Use `safe_load()` for normal YAML parsing.

### Example
```python
import yaml

text = '''
name: Janette
age: 24
skills:
  - Python
  - SQL
  - React
'''

data = yaml.safe_load(text)
print(data)
print(type(data))
```

### Output
```python
{'name': 'Janette', 'age': 24, 'skills': ['Python', 'SQL', 'React']}
<class 'dict'>
```

---

## 21. Parsing YAML Files

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

print(data)
```

This reads YAML and converts it into Python objects.

---

## 22. Serializing YAML with `yaml.safe_dump()`

Use `safe_dump()` to convert Python objects into YAML text.

### Example
```python
import yaml

data = {
    "name": "Janette",
    "age": 24,
    "skills": ["Python", "SQL", "React"]
}

text = yaml.safe_dump(data)
print(text)
```

Possible output:
```yaml
age: 24
name: Janette
skills:
- Python
- SQL
- React
```

---

## 23. Writing YAML to a File

```python
import yaml

data = {
    "app": "demo",
    "debug": True,
    "port": 8080
}

with open("config.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(data, file)
```

---

## 24. Making YAML Output More Readable

You can control formatting options.

```python
import yaml

data = {
    "name": "Janette",
    "skills": ["Python", "SQL", "React"]
}

text = yaml.safe_dump(data, sort_keys=False)
print(text)
```

### Why `sort_keys=False`?
Without it, YAML output may reorder keys alphabetically.

---

## 25. JSON vs YAML

### JSON
- stricter syntax
- very common in APIs
- excellent for machine-to-machine exchange

### YAML
- more human-friendly
- often used in configuration
- supports a more flexible visual style

### Example JSON
```json
{
  "name": "Janette",
  "age": 24
}
```

### Example YAML
```yaml
name: Janette
age: 24
```

---

## 26. CSV vs JSON vs YAML

### CSV
Best when:
- data is tabular
- rows and columns are the main structure

### JSON
Best when:
- data is nested
- APIs are involved
- objects and arrays are needed

### YAML
Best when:
- humans will read/edit the file often
- configuration is the main use case

---

## 27. Common Beginner Mistakes

### Confusing `load()` and `loads()`
- `load()` reads from a file object
- `loads()` reads from a string

Examples:
```python
import json

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
```

```python
import json

text = '{"name": "Janette"}'
data = json.loads(text)
```

The same general idea applies to YAML parsing patterns.

---

## 28. Forgetting Encoding in Text Files

Good:
```python
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
```

Also good:
```python
with open("config.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)
```

Using `encoding="utf-8"` is usually the safest default for text data files.

---

## 29. Using Unsafe YAML Loading

Prefer:

```python
yaml.safe_load(text)
```

Instead of more permissive loaders, unless you specifically need advanced behavior and understand the risks.

---

## 30. Assuming CSV Types Are Automatic

CSV values are usually read as strings.

```python
import csv

with open("users.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        age = int(row["age"])
        print(age)
```

If you need numbers or booleans, convert them yourself.

---

## 31. Forgetting That JSON Cannot Serialize Every Python Object by Default

This fails for many custom or complex objects:

```python
import json
from datetime import datetime

data = {"created_at": datetime.now()}
# json.dumps(data)  # TypeError
```

You often need:
- conversion first
- or a custom serializer

---

## 32. Summary

- **Parsing** means converting external text/data into Python objects
- **Serialization** means converting Python objects into storable/exportable text
- Python’s built-in **`csv`** module handles CSV files
- Python’s built-in **`json`** module handles JSON parsing and serialization
- A common YAML library is **PyYAML**
- For CSV:
  - `csv.reader`
  - `csv.DictReader`
  - `csv.writer`
  - `csv.DictWriter`
- For JSON:
  - `json.load()`
  - `json.loads()`
  - `json.dump()`
  - `json.dumps()`
- For YAML:
  - `yaml.safe_load()`
  - `yaml.safe_dump()`
- CSV is best for tabular data
- JSON is best for structured nested data and APIs
- YAML is best for human-readable configuration


# Python: `datetime` and Time Zones

## 1. What Is `datetime`?

The `datetime` module is Python’s standard library for working with:
- dates
- times
- combined date-and-time values
- time differences
- timezone-aware date and time objects

You usually import the classes you need from the module.

```python
from datetime import date, time, datetime, timedelta
```

---

## 2. Main Types in `datetime`

The most common types are:

- `date` → calendar date only
- `time` → time of day only
- `datetime` → date and time together
- `timedelta` → difference between two dates/times
- `tzinfo` / `timezone` → timezone support

### Example
```python
from datetime import date, time, datetime, timedelta

today = date.today()
now = datetime.now()
meeting_time = time(14, 30)
duration = timedelta(days=2, hours=3)

print(today)
print(now)
print(meeting_time)
print(duration)
```

---

## 3. `date`

A `date` stores:
- year
- month
- day

### Example
```python
from datetime import date

birthday = date(2000, 5, 10)
print(birthday)
print(birthday.year)
print(birthday.month)
print(birthday.day)
```

### Getting today’s date
```python
from datetime import date

today = date.today()
print(today)
```

---

## 4. `time`

A `time` stores:
- hour
- minute
- second
- optional microseconds
- optional timezone info

### Example
```python
from datetime import time

alarm = time(7, 30)
print(alarm)
```

### With seconds
```python
from datetime import time

exact_time = time(14, 45, 30)
print(exact_time)
```

---

## 5. `datetime`

A `datetime` combines:
- date
- time

### Example
```python
from datetime import datetime

moment = datetime(2026, 4, 7, 15, 30, 45)
print(moment)
```

### Current local date and time
```python
from datetime import datetime

now = datetime.now()
print(now)
```

### Current UTC date and time
```python
from datetime import datetime, UTC

now_utc = datetime.now(UTC)
print(now_utc)
```

---

## 6. `timedelta`

A `timedelta` represents a duration or difference between two date/time values.

### Example
```python
from datetime import timedelta

delta = timedelta(days=5, hours=2, minutes=30)
print(delta)
```

### Adding a `timedelta`
```python
from datetime import datetime, timedelta

now = datetime.now()
future = now + timedelta(days=7)
print(future)
```

### Subtracting two datetimes
```python
from datetime import datetime

start = datetime(2026, 4, 1, 10, 0, 0)
end = datetime(2026, 4, 3, 12, 30, 0)

difference = end - start
print(difference)
```

---

## 7. Formatting Dates and Times

Use `strftime()` to convert date/time objects into strings.

### Example
```python
from datetime import datetime

now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)
```

### Common format codes
- `%Y` → 4-digit year
- `%m` → 2-digit month
- `%d` → 2-digit day
- `%H` → hour (24-hour clock)
- `%M` → minute
- `%S` → second

### Example
```python
from datetime import datetime

now = datetime(2026, 4, 7, 16, 45, 30)
print(now.strftime("%d/%m/%Y"))
print(now.strftime("%Y-%m-%d"))
print(now.strftime("%H:%M:%S"))
```

---

## 8. Parsing Strings into Dates and Times

Use `strptime()` to parse a string into a `datetime`.

### Example
```python
from datetime import datetime

text = "2026-04-07 16:45:30"
dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
print(dt)
```

### Parsing a date only
```python
from datetime import datetime

text = "2026-04-07"
dt = datetime.strptime(text, "%Y-%m-%d")
print(dt.date())
```

---

## 9. ISO Format

ISO 8601 is a very common standard for date/time strings.

### Convert to ISO string
```python
from datetime import datetime

now = datetime(2026, 4, 7, 16, 45, 30)
print(now.isoformat())
```

### Parse from ISO string
```python
from datetime import datetime

text = "2026-04-07T16:45:30"
dt = datetime.fromisoformat(text)
print(dt)
```

---

## 10. Naive vs Aware Datetimes

This is one of the most important concepts.

### Naive datetime
A **naive** datetime does not contain enough timezone information to locate itself unambiguously in time.

```python
from datetime import datetime

dt = datetime.now()
print(dt)
print(dt.tzinfo)
```

### Aware datetime
An **aware** datetime includes timezone information and represents a specific moment in time.

```python
from datetime import datetime, UTC

dt = datetime.now(UTC)
print(dt)
print(dt.tzinfo)
```

### Rule of thumb
- use **naive** datetimes only for simple local/internal cases
- use **aware** datetimes when correctness across time zones matters

---

## 11. `timezone` for Fixed Offsets

The `datetime` module includes `timezone`, which is useful for fixed UTC offsets.

### UTC example
```python
from datetime import datetime, UTC

dt = datetime.now(UTC)
print(dt)
```

### Custom fixed offset
```python
from datetime import datetime, timezone, timedelta

mx_fixed = timezone(timedelta(hours=-6))
dt = datetime.now(mx_fixed)
print(dt)
```

### Important
Fixed offsets are not the same as full regional time zones with daylight saving rules.

---

## 12. Why Fixed Offsets Are Not Enough

A fixed offset like `UTC-6` does not automatically handle:
- daylight saving time
- historical timezone changes
- regional timezone rules

For real geographic time zones, use `zoneinfo`.

---

## 13. `zoneinfo`

The `zoneinfo` module provides IANA time zone support.

```python
from zoneinfo import ZoneInfo
```

This is the standard modern way to work with real time zones in Python.

### Example
```python
from datetime import datetime
from zoneinfo import ZoneInfo

mx_time = datetime.now(ZoneInfo("America/Mexico_City"))
ny_time = datetime.now(ZoneInfo("America/New_York"))

print(mx_time)
print(ny_time)
```

---

## 14. Creating Timezone-Aware Datetimes with `ZoneInfo`

```python
from datetime import datetime
from zoneinfo import ZoneInfo

dt = datetime(2026, 4, 7, 12, 0, 0, tzinfo=ZoneInfo("America/Mexico_City"))
print(dt)
```

This creates an aware datetime attached to a real IANA timezone.

---

## 15. Converting Between Time Zones

Use `astimezone()` to convert an aware datetime into another timezone.

### Example
```python
from datetime import datetime
from zoneinfo import ZoneInfo

mx = ZoneInfo("America/Mexico_City")
tokyo = ZoneInfo("Asia/Tokyo")

dt_mx = datetime(2026, 4, 7, 10, 0, 0, tzinfo=mx)
dt_tokyo = dt_mx.astimezone(tokyo)

print(dt_mx)
print(dt_tokyo)
```

This keeps the same instant in time, but expresses it in another timezone.

---

## 16. Working in UTC

A very common practice is:
- store timestamps in UTC
- convert to local timezone only for display

### Example
```python
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

stored = datetime.now(UTC)
shown = stored.astimezone(ZoneInfo("America/Mexico_City"))

print("Stored:", stored)
print("Shown:", shown)
```

This avoids many timezone-related bugs.

---

## 17. Replacing `tzinfo` vs Converting Time Zones

This is a common source of confusion.

### `replace(tzinfo=...)`
This attaches or changes timezone metadata without converting the clock time.

```python
from datetime import datetime
from zoneinfo import ZoneInfo

dt = datetime(2026, 4, 7, 12, 0, 0)
attached = dt.replace(tzinfo=ZoneInfo("America/Mexico_City"))

print(attached)
```

### `astimezone(...)`
This converts one aware datetime into another timezone while preserving the same instant.

```python
from datetime import datetime
from zoneinfo import ZoneInfo

mx = ZoneInfo("America/Mexico_City")
utc = ZoneInfo("UTC")

dt = datetime(2026, 4, 7, 12, 0, 0, tzinfo=mx)
converted = dt.astimezone(utc)

print(dt)
print(converted)
```

### Important
Use `astimezone()` for conversion.
Use `replace()` only when you truly mean “attach/change metadata”.

---

## 18. Unix Timestamps

A Unix timestamp is the number of seconds since the Unix epoch.

### Current timestamp
```python
from datetime import datetime, UTC

now = datetime.now(UTC)
print(now.timestamp())
```

### From timestamp to datetime
```python
from datetime import datetime, UTC

ts = 1712500000
dt = datetime.fromtimestamp(ts, UTC)
print(dt)
```

---

## 19. Comparing Datetimes

You can compare datetimes, but they should be compatible.

### Example
```python
from datetime import datetime

a = datetime(2026, 4, 7, 10, 0, 0)
b = datetime(2026, 4, 7, 12, 0, 0)

print(a < b)   # True
```

### Important
Mixing naive and aware datetimes in comparisons usually raises an error.

```python
from datetime import datetime, UTC

naive = datetime.now()
aware = datetime.now(UTC)

# print(naive < aware)  # Error
```

Use either:
- all naive
- or all aware

Do not mix them.

---

## 20. Common Timezone Pitfalls

### Pitfall 1: Using local naive times everywhere
```python
from datetime import datetime

created_at = datetime.now()
```

This can be ambiguous when your code runs on different machines or in multiple regions.

### Better
```python
from datetime import datetime, UTC

created_at = datetime.now(UTC)
```

### Pitfall 2: Using fixed offsets as real locations
```python
from datetime import timezone, timedelta

tz = timezone(timedelta(hours=-6))
```

This does not represent all historical and daylight-saving behavior of a real region.

### Better
```python
from zoneinfo import ZoneInfo

tz = ZoneInfo("America/Mexico_City")
```

### Pitfall 3: Mixing naive and aware datetimes
This often causes bugs or exceptions.

---

## 21. Example: Scheduling in a Real Time Zone

```python
from datetime import datetime
from zoneinfo import ZoneInfo

meeting = datetime(2026, 4, 7, 9, 0, 0, tzinfo=ZoneInfo("America/Mexico_City"))

print("Meeting in MX:", meeting)
print("Meeting in UTC:", meeting.astimezone(ZoneInfo("UTC")))
print("Meeting in Tokyo:", meeting.astimezone(ZoneInfo("Asia/Tokyo")))
```

This is a good example of why timezone-aware datetimes matter.

---

## 22. Example: Store in UTC, Display Locally

```python
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

# store
created_at = datetime.now(UTC)

# display for Mexico City
displayed = created_at.astimezone(ZoneInfo("America/Mexico_City"))

print("Stored in UTC:", created_at.isoformat())
print("Displayed locally:", displayed.strftime("%Y-%m-%d %H:%M:%S %Z"))
```

This is a very common and reliable pattern.

---

## 23. Common Beginner Mistakes

### Using `datetime.utcnow()`
Older code often uses:

```python
from datetime import datetime

dt = datetime.utcnow()
```

This returns a naive datetime and is often less safe than creating an aware UTC datetime.

Better:
```python
from datetime import datetime, UTC

dt = datetime.now(UTC)
```

### Confusing `replace()` with timezone conversion
Wrong idea:
```python
dt = dt.replace(tzinfo=ZoneInfo("UTC"))
```

That does not convert the moment. It just changes timezone metadata.

### Forgetting daylight saving rules
Using only fixed offsets can be incorrect for real locations.

### Comparing naive and aware datetimes
This usually raises an error.

### Parsing strings without knowing their timezone meaning
A timestamp string without timezone info can be ambiguous.

---

## 24. Summary

- `datetime` is Python’s standard library for dates and times
- Main types include:
  - `date`
  - `time`
  - `datetime`
  - `timedelta`
- Use `strftime()` to format
- Use `strptime()` to parse custom date/time strings
- Use `isoformat()` and `fromisoformat()` for ISO 8601-style strings
- A **naive** datetime has no clear timezone context
- An **aware** datetime includes timezone information
- `timezone` is good for fixed offsets
- `zoneinfo` is the standard modern tool for real IANA time zones
- Use `astimezone()` to convert between time zones
- A common best practice is:
  - store in UTC
  - display in the user’s local timezone

  # Python: Logging and Configuration

## 1. What Is Logging?

**Logging** is a way to record events that happen while a program runs.

It is useful for:
- debugging
- monitoring
- tracing errors
- understanding program flow
- keeping operational records

Python includes the `logging` module in the standard library.

---

## 2. Why Use Logging Instead of `print()`?

`print()` is fine for simple console output, but `logging` is better when you need:

- different severity levels
- configurable output destinations
- timestamps
- structured formatting
- file logging
- filtering
- flexible configuration

### Rule of thumb
- use `print()` for ordinary user-facing console output
- use `logging` for diagnostics, monitoring, and application events

---

## 3. Importing the Module

```python
import logging
```

---

## 4. Logging Levels

Python logging has standard severity levels:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

### Basic idea
- `DEBUG` → detailed diagnostic information
- `INFO` → normal application events
- `WARNING` → something unexpected or noteworthy happened
- `ERROR` → an operation failed
- `CRITICAL` → a very serious failure

---

## 5. Simple Logging Example

```python
import logging

logging.warning("This is a warning")
logging.error("This is an error")
logging.critical("This is critical")
```

This uses the root logger.

---

## 6. Using `basicConfig()`

For simple scripts, configure logging with `basicConfig()`.

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
```

### What this does
- sets the minimum level to display
- configures a basic handler if none is already configured

With `level=logging.INFO`, `DEBUG` messages are ignored, but `INFO` and above are shown.

---

## 7. Common Logging Functions

```python
import logging

logging.debug("Debug")
logging.info("Info")
logging.warning("Warning")
logging.error("Error")
logging.critical("Critical")
```

These convenience functions operate on the root logger.

---

## 8. Creating a Logger

A more common real-world pattern is to create a logger for the current module.

```python
import logging

logger = logging.getLogger(__name__)
```

### Why `__name__`?
It creates a logger name based on the module name, which fits naturally into Python’s logger hierarchy.

---

## 9. Logging with a Named Logger

```python
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
```

This is usually preferred over using the root logger directly.

---

## 10. Log Message Formatting

You can control how log messages look.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### Common format fields
- `%(asctime)s` → timestamp
- `%(name)s` → logger name
- `%(levelname)s` → level name
- `%(message)s` → the log message

---

## 11. Logging to a File

You can send logs to a file.

```python
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Application started")
logging.error("Something failed")
```

This is useful for keeping persistent logs.

---

## 12. Logging to Console and File

For more control, use handlers.

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", encoding="utf-8")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("Application started")
```

This sends the same log messages to both:
- console
- file

---

## 13. Handlers

A **handler** decides where log messages go.

Common handlers include:
- `StreamHandler` → console or another stream
- `FileHandler` → a file
- `NullHandler` → does nothing

### Example
```python
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

logger.addHandler(handler)
```

---

## 14. Formatters

A **formatter** controls how the log message looks.

```python
import logging

formatter = logging.Formatter("%(levelname)s: %(message)s")
```

Then attach it to a handler:

```python
import logging

handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")

handler.setFormatter(formatter)
```

---

## 15. Logger Hierarchy

Loggers form a hierarchy based on their names.

For example:
- `app`
- `app.db`
- `app.api`

A child logger usually passes records up to its parent unless propagation is disabled.

```python
import logging

logger = logging.getLogger("app.api")
```

This fits into the hierarchy under `app`.

---

## 16. Propagation

By default, log messages usually propagate up the logger hierarchy.

This means a child logger can pass records to parent loggers and their handlers.

If needed, you can disable propagation:

```python
import logging

logger = logging.getLogger("app.api")
logger.propagate = False
```

This is sometimes useful to avoid duplicate logs.

---

## 17. Logging Exceptions

If an exception happens, `logging.exception()` is very useful.

```python
import logging

logging.basicConfig(level=logging.ERROR)

try:
    1 / 0
except ZeroDivisionError:
    logging.exception("Something went wrong")
```

This logs:
- your message
- the traceback

### Important
`logging.exception()` should usually be called inside an `except` block.

---

## 18. Using Variables in Log Messages

Prefer this:

```python
import logging

logger = logging.getLogger(__name__)
user_id = 123

logger.info("User %s logged in", user_id)
```

Instead of this:

```python
logger.info(f"User {user_id} logged in")
```

### Why?
The logging system handles formatting efficiently and only formats the message when needed.

---

## 19. Basic Configuration Example for Small Scripts

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Script started")
logging.warning("Low disk space")
logging.error("File not found")
```

This is enough for many small programs.

---

## 20. More Structured Configuration with `logging.config`

For larger applications, Python provides `logging.config`.

```python
import logging.config
```

The most common modern option is `dictConfig()`.

---

## 21. Configuring Logging with `dictConfig()`

```python
import logging
import logging.config

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": "app.log",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "myapp": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

logging.config.dictConfig(config)

logger = logging.getLogger("myapp")
logger.info("Application started")
logger.debug("Debug details")
```

### Why `dictConfig()` is useful
It keeps configuration separate from the logging calls and scales better for larger applications.

---

## 22. `fileConfig()`

Python also supports configuration from an INI-style file through `logging.config.fileConfig()`.

```python
import logging.config

logging.config.fileConfig("logging.conf")
```

This is supported, but `dictConfig()` is often more flexible in modern projects.

---

## 23. Library Logging Best Practice

If you are writing a reusable library, do **not** configure logging globally for the application.

Instead, create a logger and attach a `NullHandler`.

```python
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
```

### Why?
The application using your library should decide:
- where logs go
- how they are formatted
- which level is enabled

---

## 24. Avoid Adding Real Handlers in Libraries

In library code, avoid doing this:

```python
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
```

That can interfere with application-wide logging behavior.

Prefer `NullHandler()` in libraries.

---

## 25. Common Beginner Mistakes

### Mistake 1: Calling `basicConfig()` many times
`basicConfig()` is meant for simple top-level setup. Repeating it in many modules can lead to confusing behavior.

### Mistake 2: Configuring logging inside a library
Library code should generally not decide global logging behavior.

### Mistake 3: Using `print()` for diagnostics everywhere
That makes filtering, formatting, and redirection much harder.

### Mistake 4: Building strings manually
Less ideal:
```python
logger.info("User " + user_name + " logged in")
```

Better:
```python
logger.info("User %s logged in", user_name)
```

### Mistake 5: Duplicate log messages
This often happens because:
- multiple handlers were added
- propagation was not understood
- the same logger was configured more than once

---

## 26. Recommended Pattern for Applications

A good pattern for applications is:

1. configure logging once at startup
2. use `logging.getLogger(__name__)` in each module
3. choose handlers centrally
4. use `dictConfig()` for medium or large projects

### Example module
```python
import logging

logger = logging.getLogger(__name__)

def process_user(user_id: int) -> None:
    logger.info("Processing user %s", user_id)
```

### Example startup
```python
import logging.config

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s - %(name)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}

logging.config.dictConfig(config)
```

---

## 27. Summary

- Python’s `logging` module provides a flexible event logging system
- Common logging levels are:
  - `DEBUG`
  - `INFO`
  - `WARNING`
  - `ERROR`
  - `CRITICAL`
- `basicConfig()` is useful for small scripts
- `getLogger(__name__)` is a common best practice for modules
- **handlers** decide where logs go
- **formatters** decide how logs look
- `logging.exception()` is useful inside `except` blocks
- `logging.config.dictConfig()` is the main structured configuration tool for larger applications
- reusable libraries should usually attach `NullHandler()` and let the application configure logging


# Python: `subprocess` and Automation

## 1. What Is `subprocess`?

The `subprocess` module lets Python start and control external programs.

You can use it to:

- run system commands
- execute scripts
- capture command output
- automate command-line workflows
- connect Python with external tools

Examples:
- running `git`
- executing a shell command
- calling another Python script
- automating backups or reports
- launching CLI tools from Python

---

## 2. Why Use `subprocess` for Automation?

Automation often means:

- repeating tasks
- running external tools
- combining multiple commands
- processing files automatically
- generating reports or exports
- integrating scripts with the operating system

`subprocess` is useful when Python needs to control programs outside Python itself.

---

## 3. Basic Import

```python
import subprocess
```

---

## 4. The Simplest Approach: `subprocess.run()`

For most cases, `subprocess.run()` is the main function you use.

### Example
```python
import subprocess

result = subprocess.run(["echo", "Hello"])
print(result.returncode)
```

### What it does
- runs the command
- waits for it to finish
- returns a result object

---

## 5. Why Pass a List of Arguments?

The safest and most common pattern is to pass the command as a list.

```python
import subprocess

subprocess.run(["python", "--version"])
```

This is usually better than building one big command string.

### Good
```python
subprocess.run(["ls", "-l"])
```

### Less ideal
```python
subprocess.run("ls -l", shell=True)
```

Using a list avoids many quoting and shell-parsing problems.

---

## 6. Capturing Output

If you want to read what the command printed, use `capture_output=True`.

```python
import subprocess

result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True
)

print("stdout:", result.stdout)
print("stderr:", result.stderr)
```

### Why `text=True`?
Without it, output is returned as bytes.

With `text=True`, output is returned as normal strings.

---

## 7. Understanding the Result Object

`subprocess.run()` returns a `CompletedProcess` object.

Common attributes:
- `returncode`
- `stdout`
- `stderr`

### Example
```python
import subprocess

result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True
)

print(result.returncode)
print(result.stdout)
print(result.stderr)
```

---

## 8. Checking for Failures with `check=True`

If you want Python to raise an exception when the command fails, use `check=True`.

```python
import subprocess

subprocess.run(["python", "--version"], check=True)
```

### Example with error handling
```python
import subprocess

try:
    subprocess.run(["false"], check=True)
except subprocess.CalledProcessError as error:
    print("Command failed")
    print("Return code:", error.returncode)
```

This is useful in automation because failures should often stop the workflow.

---

## 9. Timeouts

You can prevent a command from running forever.

```python
import subprocess

try:
    subprocess.run(["sleep", "10"], timeout=2)
except subprocess.TimeoutExpired:
    print("Command took too long")
```

This is helpful for:
- network tools
- hanging scripts
- unreliable external commands

---

## 10. Running in a Specific Directory

Use `cwd` to run a command in another folder.

```python
import subprocess

subprocess.run(["ls"], cwd="/tmp")
```

This is useful for automation tasks like:
- running `git` inside a repository
- building a project in a specific folder
- executing tools relative to a working directory

---

## 11. Passing Environment Variables

Use `env` when the subprocess needs a custom environment.

```python
import os
import subprocess

env = os.environ.copy()
env["MODE"] = "production"

subprocess.run(["python", "script.py"], env=env)
```

This is useful for:
- configs
- API keys
- feature flags
- different execution modes

---

## 12. Redirecting Output to a File

You can send command output directly into a file.

```python
import subprocess

with open("output.txt", "w", encoding="utf-8") as file:
    subprocess.run(["python", "--version"], stdout=file, text=True)
```

You can also redirect errors:

```python
import subprocess

with open("errors.txt", "w", encoding="utf-8") as file:
    subprocess.run(["some_command"], stderr=file, text=True)
```

---

## 13. Combining Standard Output and Standard Error

Sometimes you want both streams together.

```python
import subprocess

result = subprocess.run(
    ["python", "--version"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

print(result.stdout)
```

This is useful for logging or unified output capture.

---

## 14. Running Another Python Script

A very common automation task is calling another Python script.

```python
import subprocess

subprocess.run(["python", "other_script.py"])
```

Or with arguments:

```python
import subprocess

subprocess.run(["python", "report.py", "--month", "04", "--year", "2026"])
```

This is useful when one script coordinates several smaller scripts.

---

## 15. Running Shell Commands

Sometimes you may want shell features like:
- pipes
- wildcards
- shell built-ins

Example:
```python
import subprocess

subprocess.run("echo Hello", shell=True)
```

### Important
Using `shell=True` can be risky if the command includes untrusted input.

Avoid it unless you really need shell behavior.

---

## 16. Why `shell=True` Can Be Dangerous

If user input is inserted into a shell command, special characters may be interpreted by the shell.

Bad pattern:
```python
import subprocess

user_input = "some value"
subprocess.run(f"echo {user_input}", shell=True)
```

Safer approach:
```python
import subprocess

user_input = "some value"
subprocess.run(["echo", user_input])
```

### Rule of thumb
- prefer argument lists
- avoid `shell=True` unless necessary

---

## 17. `Popen` for More Control

`subprocess.run()` is enough for many tasks, but `Popen` gives more control.

Use `Popen` when you need:
- streaming output while the process runs
- interactive communication
- manual polling
- advanced process management

### Example
```python
import subprocess

process = subprocess.Popen(
    ["python", "--version"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate()

print(stdout)
print(stderr)
print(process.returncode)
```

---

## 18. Real-Time Output with `Popen`

If you want to process output line by line while the command is running:

```python
import subprocess

process = subprocess.Popen(
    ["ping", "127.0.0.1"],
    stdout=subprocess.PIPE,
    text=True
)

for line in process.stdout:
    print("OUTPUT:", line.strip())
```

This can be useful for:
- monitoring long-running commands
- showing live progress
- processing logs in real time

---

## 19. Waiting for a Process

With `Popen`, you can wait explicitly.

```python
import subprocess

process = subprocess.Popen(["python", "--version"])
return_code = process.wait()

print(return_code)
```

---

## 20. Polling a Process

You can also check whether the process is finished without blocking.

```python
import subprocess
import time

process = subprocess.Popen(["python", "--version"])

while process.poll() is None:
    print("Still running...")
    time.sleep(0.5)

print("Finished with code:", process.returncode)
```

This is useful when automation needs to do other work while waiting.

---

## 21. Automation Example: Batch File Processing

Suppose you want to convert many files with an external command-line tool.

```python
from pathlib import Path
import subprocess

input_folder = Path("input")

for file_path in input_folder.glob("*.txt"):
    output_file = file_path.with_suffix(".out")
    subprocess.run(
        ["some_tool", str(file_path), str(output_file)],
        check=True
    )
```

This is a common automation pattern:
- find files
- loop through them
- run an external command for each one

---

## 22. Automation Example: Backup Script

```python
from pathlib import Path
import subprocess
from datetime import datetime

source = Path("data")
backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

subprocess.run(
    ["zip", "-r", backup_name, str(source)],
    check=True
)
```

This shows how Python can automate external tools and add dynamic naming.

---

## 23. Automation Example: Git Commands

```python
import subprocess

subprocess.run(["git", "status"], check=True)
subprocess.run(["git", "pull"], check=True)
```

This is useful for deployment scripts, CI helpers, or repository automation.

---

## 24. Combining `subprocess` with Other Modules

`subprocess` becomes much more useful when combined with:

- `pathlib` for file paths
- `logging` for diagnostics
- `json` for structured config/output
- `datetime` for timestamps
- `shutil` for high-level file operations
- `os` for environment variables

### Example
```python
from pathlib import Path
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

script = Path("tasks") / "generate_report.py"

logger.info("Running report script")
subprocess.run(["python", str(script)], check=True)
logger.info("Done")
```

---

## 25. Using `subprocess` in Automation Pipelines

A typical automation pipeline may look like this:

1. read input files
2. validate data
3. call external tools
4. capture output
5. save logs
6. move or archive results

`subprocess` is often just one piece of a larger automation workflow.

---

## 26. Async Automation with `asyncio`

If you need to run and monitor subprocesses asynchronously, Python also has `asyncio` subprocess APIs.

### Example
```python
import asyncio

async def main():
    process = await asyncio.create_subprocess_exec(
        "python", "--version",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    print(stdout.decode().strip())

asyncio.run(main())
```

This is useful when:
- you want parallel command execution
- your program is already async
- you need non-blocking orchestration

---

## 27. Common Beginner Mistakes

### Mistake 1: Using `shell=True` unnecessarily
Less safe:
```python
subprocess.run("ls -l", shell=True)
```

Usually better:
```python
subprocess.run(["ls", "-l"])
```

### Mistake 2: Forgetting `text=True`
Without it, output may be bytes.

```python
result = subprocess.run(["python", "--version"], capture_output=True)
print(result.stdout)  # bytes
```

Better:
```python
result = subprocess.run(["python", "--version"], capture_output=True, text=True)
print(result.stdout)  # str
```

### Mistake 3: Ignoring return codes
If you never check whether the command failed, automation may continue with bad data.

Better:
```python
subprocess.run(["some_command"], check=True)
```

### Mistake 4: Not handling timeouts
Some commands can hang.

Better:
```python
subprocess.run(["some_command"], timeout=30)
```

### Mistake 5: Building commands with string concatenation
Less safe:
```python
filename = "report.txt"
subprocess.run(f"cat {filename}", shell=True)
```

Better:
```python
filename = "report.txt"
subprocess.run(["cat", filename])
```

---

## 28. Practical Recommendations

A good practical approach is:

- use `subprocess.run()` for most tasks
- pass arguments as a list
- use `check=True` in automation scripts
- use `capture_output=True` when you need output
- use `text=True` for string output
- use `timeout=` for long or unreliable commands
- avoid `shell=True` unless shell features are required
- use `Popen` only when you need more control
- combine `subprocess` with `pathlib` and `logging`

---

## 29. Summary

- `subprocess` lets Python run and control external programs
- `subprocess.run()` is the most common high-level API
- `Popen` gives lower-level control for advanced cases
- use argument lists instead of command strings when possible
- `capture_output=True` captures stdout and stderr
- `text=True` returns output as strings instead of bytes
- `check=True` raises an exception on failure
- `timeout=` prevents hanging commands
- `cwd=` changes the working directory
- `env=` passes custom environment variables
- `shell=True` should be used carefully
- `subprocess` is a key tool for automation scripts and CLI orchestration