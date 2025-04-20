#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ozi_build import schema


def render_doc(fields_desc: str, option: str, desc: dict[str, str]):
    fields_desc += "### `%s`" % option
    if desc.get("optional"):
        fields_desc += " (Optional)"
    fields_desc += "\n\n"
    fields_desc += desc['description']
    fields_desc += "\n\n"
    return fields_desc


def generate_doc():
    fields_desc = ""
    for option, desc in schema.VALID_OPTIONS.items():
        fields_desc = render_doc(fields_desc, option, desc)
    pyc_wheel_desc = ''
    for option, desc in schema.VALID_PYC_WHEEL_OPTIONS.items():
        pyc_wheel_desc = render_doc(pyc_wheel_desc, option, desc)
    with open(sys.argv[1], 'r') as i:
        with open(sys.argv[2], 'w') as o:
            o.write(i.read().format(fields_desc=fields_desc, pyc_wheel_desc=pyc_wheel_desc))


if __name__ == "__main__":
    generate_doc()
