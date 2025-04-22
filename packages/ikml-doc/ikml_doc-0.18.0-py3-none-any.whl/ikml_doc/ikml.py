# Written by: Chaitanya S Lakkundi (chaitanya.lakkundi@gmail.com)

import re
import requests
import copy
import json
from pathlib import Path
from .utils import Node, ikml_to_anytree, dict_to_anytree, LevelOrderIter


class IKML_Document:
    def __init__(self, url=None, data=None):
        self.load(url=url, data=data)

    def mount(self, root):
        self.root = root

    def load(self, url=None, data=None):
        if url is not None:
            self.url = url
            self.raw_data = str(requests.get(self.url).content, encoding="utf-8")
            self.root = ikml_to_anytree(self.raw_data)

        if data is not None:
            self.raw_data = data
            # data is either a dict or a list of dicts
            if isinstance(self.raw_data, dict) or isinstance(self.raw_data, list):
                self.root = dict_to_anytree(self.raw_data)
            else:
                self.root = ikml_to_anytree(self.raw_data)

    def save(self, exclude_root=False, filename="out_ikml.txt"):
        Path(filename).write_text(self.to_txt(exclude_root=exclude_root), encoding="utf-8")

    def to_dict(self, max_depth=-1):
        # dot-attributes are automatically added for its parent node
        return self.root.to_dict(max_depth=max_depth)

    def to_json(self, max_depth=-1):
        d = self.to_dict(max_depth=max_depth)
        return json.dumps(d, ensure_ascii=False, indent=2)

    # TODO: implement max_depth, exclude_root in to_xml and tree_as_xml_list
    def to_xml(self, put_attrs_inside=True):
        # put_attrs_inside is only required for to_xml method.
        # to_dict and to_json check for attributes appropriately by default
        if put_attrs_inside:
            r2 = copy.deepcopy(self.root)
            r2.put_attrs_inside()
            return r2.to_xml(quoted_attr=True)
        else:
            return self.root.to_xml(quoted_attr=True)

    def to_txt(self, exclude_root=False, quoted_attr=False, max_depth=-1):
        # returns IKML text
        return self.root.to_txt(exclude_root=exclude_root, quoted_attr=quoted_attr, max_depth=max_depth)

    def find_children(
        self, tag_name, max_depth=-1, apply_fn=None
    ):
        if max_depth <= -1:
            max_depth = 9999
        for node in self.iter():
            try:
                if node.tag_name == tag_name and node.depth <= max_depth:
                    if apply_fn is not None:
                        yield apply_fn(node)
                    else:
                        yield node
            except:
                pass

    def get(self, tag_id, default=None):
        for node in self.root.iter():
            try:
                if node["id"] == tag_id:
                    return node
            except:
                pass
        return default

    def iter(self):
        for node in self.root.iter():
            yield node

    @staticmethod
    def create_node(data, *args, **kwargs):
        data = data.strip()
        if data[0] != "[":
            data = f"[{data}]"
        return Node(data, *args, **kwargs)

    def validate_schema(self, schema_doc):
        valid = True
        valid_schema = set()
        try:
            root = list(schema_doc.find_children("ikml_schema"))[0]
            root.tag_name = "root"
        except:
            pass

        for node in schema_doc.iter():
            if not node.parent:
                ptag = "root"
            else:
                ptag = node.parent.tag_name
            valid_schema.add((ptag, node.tag_name))

        for node in self.iter():
            if not node.parent:
                ptag = "root"
            else:
                ptag = node.parent.tag_name
            if (ptag, node.tag_name) not in valid_schema:
                print("Alert: Invalid tag ", node)
                valid = False
        print(valid_schema)
        return valid
