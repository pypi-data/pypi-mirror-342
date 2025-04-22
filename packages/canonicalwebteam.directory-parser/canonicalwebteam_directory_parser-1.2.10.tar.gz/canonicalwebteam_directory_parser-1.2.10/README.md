# canonicalwebteam.directory-parser
Flask extension to parse websites and extract structured data to build sitemaps.

## Install
Install the project with pip: `pip install canonicalwebteam.directory-parser`


## Using the directory parser

### Sitemap templates
Include sitemap templates in your Flask app. Copy the following codeblock to where your application is instantiated e.g `app.py`. The template loader should be placed right after the app is instantiated.

```
from jinja2 import ChoiceLoader, FileSystemLoader
from pathlib import Path
import canonicalwebteam.directory_parser as directory_parser


# Set up Flask application
app = FlaskBase(...)


# Include directory parser templates
directory_parser_templates = (
    Path(directory_parser.__file__).parent / "templates"
)

loader = ChoiceLoader(
    [
        FileSystemLoader(str(directory_parser_templates)),
    ]
)

app.jinja_loader = loader
```

### Generate sitemaps
The `generate_sitemap` function will generate a sitemap given directory path and base url using the sitemap templates.

```
# Dynamic sitemaps that do not need to be included in the sitemap tree.
# Differ from project to project, can be checked on /sitemap.xml
DYNAMIC_SITEMAPS = [
    "tutorials",
    "engage",
    "ceph/docs",
    "blog",
    "security/notices",
    "security/cves",
    "security/livepatch/docs",
    "robotics/docs",
]

directory_path = os.getcwd() + "/templates"
base_url = "https://ubuntu.com"

xml_sitemap = directory_parser.generate_sitemap(
                directory_path, 
                base_url, 
                exclude_paths=DYNAMIC_SITEMAPS
              )

if xml_sitemap:
    with open(sitemap_path, "w") as f:
        f.write(xml_sitemap)

# Serve the existing sitemap
with open(sitemap_path, "r") as f:
    xml_sitemap = f.read()

response = flask.make_response(xml_sitemap)
response.headers["Content-Type"] = "application/xml"
return response
```

### Parse project directory tree
If you'd like to get the parsed tree of a given directory, you can use the `scan_directory` function. 

```
directory_path = os.getcwd() + "/templates"
tree = directory_parser.scan_directory(
            directory_path, exclude_paths=DYNAMIC_SITEMAPS
        )
```
`tree` will return a tree of all the templates given in the `directory_path`


## Local development
### Running the project
This guide assumes that you are using [dotrun](https://github.com/canonical/dotrun/) to run your Flask app.

#### Include a relative path to the project
This example assumes both project exist in the same directory

In `requirements.txt`:
```
# Comment out package import
# canonicalwebteam.directory-parser==1.2.6

-e ../directory-parser
```

#### Run project with a mounted additor
`dotrun -m /path/to/canonicalwebteam.directory-parser:../directory-parser`


### Linting and formatting

To follow the standard linting rules of this project, we are using [Tox](https://tox.wiki/en/latest/)
```
pip3 install tox  # Install tox
tox -e lint       # Check the format of Python code
tox -e format     # Reformat the Python code
```
