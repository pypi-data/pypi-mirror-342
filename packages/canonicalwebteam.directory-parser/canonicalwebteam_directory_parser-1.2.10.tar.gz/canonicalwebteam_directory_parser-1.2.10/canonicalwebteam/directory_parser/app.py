import flask
import re
import subprocess
from contextlib import suppress
from pathlib import Path

BASE_TEMPLATES = [
    "base_index.html",
    "templates/base.html",
    "templates/base_no_nav.html",
    "templates/one-column.html",
    "_base/base.html",
]
MARKDOWN_TEMPLATES = [
    "legal/_base_legal_markdown.html",
    "appliance/shared/_base_appliance_index.html",
]
TEMPLATE_PREFIXES = ["base", "_base"]
TAG_MAPPING = {
    "title": ["title"],
    "description": ["meta_description", "description"],
    "link": ["meta_copydoc"],
}
ERROR_PAGES = [
    "400.html",
    "403.html",
    "404.html",
    "410.html",
    "429.html",
    "401.html",
    "500.html",
    "502.html",
]


def is_index(path):
    return path.name == "index.html" or path.name == "index.md"


def check_has_index(path):
    if (path / "index.html").exists():
        return True, "html"
    elif (path / "index.md").exists():
        return True, "md"
    else:
        return False, None


def is_template(path):
    """
    Return True if the file name starts with a template prefix.

    TODO: It is possible that valid page uris start with one of these prefixes.
    Instead, we could match the extended_path in index.html to files in the
    folder, and exclude files whose filename is in the extended path.
    """
    for prefix in TEMPLATE_PREFIXES:
        if path.name.startswith(prefix):
            return True
    return False


def append_base_path(base, path_name):
    """
    Add the base (root) to a path URI.

    In some cases, e.g with server/maas/thank-you.html, the file refers
    to a path

    """
    if str(path_name).startswith("/"):
        path_name = path_name[1:]

    new_path = Path(base) / path_name
    return new_path.absolute()


def extends_base(path, base="templates"):
    """Return true if path extends templates/base.html"""
    # TODO: Investigate whether path.read_text performs better than opening
    # a file
    with suppress(FileNotFoundError):
        with path.open("r") as f:
            for line in f.readlines():
                match = re.search("{% extends [\"'](.*?)[\"'] %}", line)
                if match:
                    if match.group(1) in BASE_TEMPLATES:
                        return True
                    else:
                        # extract absolute path from the parent path
                        absolute_path = str(path)[
                            0 : str(path).find(base) + len(base)
                        ]
                        # check if the file from which the current file
                        # extends extends from the base template
                        new_path = append_base_path(
                            absolute_path, match.group(1)
                        )
                        return extends_base(new_path, base=base)

    return False


def resolve_if_tag(text):
    """
    If there is a '{% if * %}{% endif %}' tag within the data, resolve the
    condition by taking the first branch, and return the result e.g

    "Search results{% if query %} for '{{ query }}'{% endif %}"
    -> "Search results"

    "{% if user_info %}Ubuntu Pro Dashboard{% else %}Ubuntu Pro{% endif %}"
    -> "Ubuntu Pro Dashboard"
    """
    pattern = r"{% if .*? %}(.*?){% endif %}"
    if match := re.search(pattern, text):
        inner_text = match.group(1)
        # If there is an else branch, return the first branch
        if "else" in inner_text:
            return inner_text.split("{% else")[0]
        return inner_text
    # If no match is found, return data
    return text


def extract_text_from_tag(tag, data):
    """
    Extract data from inside tags
    """
    search_string = "{{% block {0} *%}}(.*){{%( *)endblock".format(tag)
    if data and (match := re.match(search_string, data.replace("\n", "  "))):
        inner_text = match.group(1).strip()
        # If there is an if tag within the data, resolve the condition
        if "{% if" in inner_text:
            return resolve_if_tag(inner_text)
        return inner_text
    # If no match is found, return data
    return data


def get_extended_copydoc(path, base):
    """
    Get the copydoc for the extended file
    """
    if str(path).startswith("/"):
        path = path[1:]
    with base.joinpath(path).open("r") as f:
        file_data = f.read()
        if match := re.search(
            r"\{\% block meta_copydoc *\%\}(.*)\{\%( *)endblock", file_data
        ):
            return match.group(1)


def get_tags_rolling_buffer(path):
    """
    Parse an html file and return a dictionary of its tags
    """

    tags = create_node()
    available_tags = list(TAG_MAPPING.keys())

    # We create a map of the selected variants for each tag
    variants_mapping = {v: "" for v in available_tags}

    with path.open("r") as f:
        for tag in available_tags:
            buffer = []
            is_buffering = False
            tag_found = False

            variants = TAG_MAPPING[tag]

            for variant in variants:
                is_buffering = False
                # Return to start of file
                f.seek(0)

                for line in f.readlines():
                    if is_buffering:
                        buffer.append(line)

                    if not is_buffering and (
                        match := re.search(f"{{% block {variant}( *)%}}", line)
                    ):
                        # We remove line contents before the tag
                        line = line[match.start() :]  # noqa: E203

                        buffer.append(line)
                        is_buffering = True
                        variants_mapping[tag] = variant

                    # We search for the end of the tag in the existing buffer
                    buffer_string = "".join(buffer)
                    if is_buffering and re.search(
                        "(.*){%( *)endblock", buffer_string
                    ):
                        # We save the buffer contents to the tags dictionary
                        tags[tag] = buffer_string

                        # We extract the text within the tags
                        tags[tag] = extract_text_from_tag(
                            variants_mapping[tag], tags[tag]
                        )

                        # We now reset the buffer
                        buffer = []
                        is_buffering = False
                        tag_found = True
                        break

                if tag_found:
                    break

    # We add the name from the path
    raw_name = re.sub(r"(?i)(.html|/index.html|/index.md)", "", str(path))
    tags["name"] = raw_name.split("/templates", 1)[-1]

    return tags


def is_valid_page(path, extended_path, is_index=True):
    """
    Determine if path is a valid page. Pages are valid if:
    - They contain the same extended path as the index html.
    - They extend from the base html.
    - Does not have "noindex" in the meta tags.
    - Does not live in a shared template directory.
    - They are markdown files with a valid wrapper template.
    - They are not error pages.
    """
    if is_template(path):
        return False

    with path.open("r") as f:
        for line in f.readlines():
            if re.search(
                r"<meta\s+"
                r'name=["\']robots["\']\s+'
                r'content=["\'].*?noindex.*?["\']',
                line,
            ):
                return False

    end_path = str(path).split("/")[-1]
    if end_path in ERROR_PAGES:
        return False

    if not is_index and extended_path:
        with path.open("r") as f:
            for line in f.readlines():
                if match := re.search("{% extends [\"'](.*?)[\"'] %}", line):
                    if match.group(1) == extended_path:
                        return True

    if "index.md" in str(path):
        with path.open("r") as f:
            for line in f.readlines():
                if match := re.search(
                    r"wrapper_template:\s*[\"']?(.*?)[\"']?$", line
                ):
                    template = match.group(1)
                    if template in MARKDOWN_TEMPLATES:
                        return True

    # If the file does not share the extended path, check if it extends the
    # base html
    return extends_base(path)


def get_extended_path(path):
    """Get the path extended by the file"""
    with path.open("r") as f:
        for line in f.readlines():
            # TODO: also match single quotes \'
            if ".html" in str(path):
                if match := re.search("{% extends [\"'](.*?)[\"'] %}", line):
                    return match.group(1)


def update_tags(tags, new_tags):
    """
    Update the old tags with new tags if they are not None
    """
    for key in new_tags:
        if new_tags[key] is not None:
            tags[key] = new_tags[key]
    return tags


def create_node():
    """Return a fresh copy of a node from a template"""
    return {
        "name": None,
        "title": None,
        "description": None,
        "link": None,
        "children": [],
        "last_modified": None,
    }


def get_git_last_modified_time(path):
    """
    Get the last modified time of a file using Git metadata.
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def scan_directory(path_name, exclude_paths=None, base=None):
    """
    We scan a given directory for valid pages and return a tree
    """
    node_path = Path(path_name)
    node = create_node()
    node["name"] = path_name.split("/templates", 1)[-1]

    # Skip scanning directory if it is in excluded paths
    if exclude_paths:
        for path in exclude_paths:
            if re.search(path, node["name"]):
                return node

    # We get the relative parent for the path
    if base is None:
        base = node_path.absolute()

    # This will be the base html file extended by the index.html
    extended_path = None
    is_index_page_valid = False

    # Check if an index.html or index.md file exists in this directory
    (has_index, index_type) = check_has_index(node_path)
    if has_index:
        index_path = node_path / ("index." + index_type)
        # Get the path extended by the index.html file
        extended_path = get_extended_path(index_path)
        # If the file is valid, add it as a child
        is_index_page_valid = is_valid_page(index_path, extended_path)
        if is_index_page_valid:
            # Get tags, add as child
            tags = get_tags_rolling_buffer(index_path)
            node = update_tags(node, tags)
            # Add last modified time for index.html
            lastmod_time = get_git_last_modified_time(index_path)
            if lastmod_time:
                node["last_modified"] = lastmod_time
    else:
        node["sitemap_exclude"] = True

    # Cycle through other files in this directory
    for child in node_path.iterdir():
        # If the child is a file, check if it is a valid page
        if child.is_file() and not is_index(child):
            # If the file is valid, add it as a child
            if (not has_index or is_index_page_valid) and is_valid_page(
                child, extended_path, is_index=False
            ):
                child_tags = get_tags_rolling_buffer(child)
                # If the child has no copydocs link, use the parent's link
                if not child_tags.get("link") and extended_path:
                    child_tags["link"] = get_extended_copydoc(
                        extended_path, base=base
                    )
                # Add last modified time for child paths
                child_lastmod_time = get_git_last_modified_time(child)
                if child_lastmod_time:
                    child_tags["last_modified"] = child_lastmod_time

                node["children"].append(child_tags)
        # If the child is a directory, scan it
        if child.is_dir():
            child_node = scan_directory(str(child), exclude_paths, base=base)
            if child_node.get("title") or child_node.get("children"):
                node["children"].append(child_node)

    return node


def generate_sitemap(directory_path, base_url, exclude_paths=None):
    """
    Generate sitemap given a directory path and a base url using
    the sitemap templates.
    """
    tree = scan_directory(directory_path, exclude_paths)
    xml_sitemap = flask.render_template(
        "sitemap_template.xml",
        tree=tree,
        base_url=base_url,
    )
    return xml_sitemap
