#!/usr/bin/env python3

# Written by: Chaitanya S Lakkundi (chaitanya.lakkundi@gmail.com)

import re
from anytree import Node as NodeParent, PreOrderIter, LevelOrderIter
from anytree.util import rightsibling
from html import escape, unescape
import json

INDENT = 2

# TODO: Major Refactor: Use OrderedDict instead of Node. It says, dict is also ordered in Python 3.7+. Check.

class Node(NodeParent):

    _default_tag_prefix = {"va": "v-", "sh": "sh-", "adhyaya": "ady-", "su": "su-", "cm": "c-", "include": "inc-", "inline": "inl-"}
    tag_prefix = _default_tag_prefix.copy()
    prop_order = ["id", "rel_id"]
    INDENT = 2

    def __init__(self, raw_data, parent=None):
        super().__init__(raw_data, parent)
        if not raw_data.strip():
            raise Exception("Empty data. Cannot create node")
        self.raw_data = raw_data
        self.tag_name, core, self.content = self.parse_ikml_node(raw_data)
        # first see if key="val" this pattern exists, only then after removing all of them split by space and check
        # with quotes, wq and without quotes, woq
        props_wq = re.findall(r"([A-z]+)=[\"\'](.*?)[\"\']", core)
        props_wq = {k: v for k, v in props_wq}
        core_woq = re.sub(r"[\"\'](.*?)[\"\']", "<!!>", core)
        props_woq = re.findall(r"([A-z]+)=(.*?)[ \]]", core_woq)
        props_woq = {k: v for k, v in props_woq if v != "<!!>"}

        # print(core_woq, props_wq, props_woq)
        self.props = dict()
        self.props.update(props_wq)
        self.props.update(props_woq)

    def keys(self):
        ret = list(self.props.keys())
        for n in self.children:
            if n.tag_name and n.is_attribute:
                ret.append(n.tag_name)
        return ret

    def get(self, key, default=None):
        try:
            return self[key]
        except:
            return default

    def __getitem__(self, key):
        # remove dot in the beginning to make it searcheable in both attribute formats
        key = key.replace(".", "")
        try:
            return self.props[key]
        except:
            pass

        for n in self.children:
            if not n.is_attribute:
                break
            if n.tag_name == "." + key:
                return n.content

        raise KeyError(f"'{key}' attribute doesn't exist in node {self.raw_data}")

    def __setitem__(self, key, value):
        if key.startswith("."):
            target = None
            pos = 0
            for n in self.children:
                # all property (attribute) nodes must be defined before other nodes
                if not n.is_attribute:
                    break
                if n.tag_name == key:
                    target = n
                    break
                pos += 1
            
            if target is not None:
                n.content = value
            else:
                # insert after all old props
                node = Node(f"[{key}] {value}")
                old_children = list(self.children)
                old_children.insert(pos, node)
                self.children = old_children
        else:
            self.props[key] = value

    def __str__(self, quoted_attr=True):
        buf = [self.tag_name]
        keys = self.props.keys() - self.prop_order
        for prop_name in self.prop_order + sorted(keys):
            try:
                if quoted_attr:
                    # ESCAPING XML https://stackoverflow.com/a/46637835
                    # WARNING: keep double quotes only to support apostrophes in attrib value. eg. Opponent's View
                    buf.append(f'{prop_name}="{self.props[prop_name]}"')
                else:
                    buf.append(f"{prop_name}={self.props[prop_name]}")
            except:
                pass
        t = "[" + " ".join(buf) + "]"
        if self.content:
            t = t + " " + self.content
        return t

    def iter(self):
        for node in PreOrderIter(self):
            yield node

    @property
    def node_children(self):
        for child in self.children:
            if not child.is_attribute:
                yield child

    @property
    def is_attribute(self):
        return self.tag_name.startswith(".")

    def generate_id(self):
        # if id doesn't exist, then borrow from parent
        if self.parent != None and self.parent.get("id", None):
            try:
                self["id"] = (
                    self.parent["id"]
                    + "."
                    + self.tag_prefix.get(self.tag_name, "")
                    + str(self["rel_id"])
                )
            except:
                # if I don't have a rel_id just ignore.
                pass
        # if no parent, check for rel_id. make it the id.
        try:
            self["id"] = str(self["rel_id"])
        except:
            pass

    def generate_ids(self):
        root_prefix = self.get("root_prefix")
        rel_id = self.get("rel_id")

        if root_prefix is not None and rel_id is not None:
            self["id"] = f"{root_prefix}.{rel_id}"
        
        elif rel_id is not None:
            self["id"] = str(rel_id)

        for child_node in self.children:
            for node in child_node.iter():
                node.generate_id()

    def generate_relids(self, root_rel_id=None):
        # Logic
        # For every prefix, keep a separate rel_id count. Traverse sibling nodes and generate rel_ids
        # Now do the same for children of every sibling node
        # 0 is null tag
        # relcount is reset for every child. but kept same for siblings
        relcounts = {t: 0 for t, p in self.tag_prefix.items()}
        relcounts[0] = 0
        # ikml_out.append(str(root))
        try:
            sibl = self.children[0]
        except:
            return
        while sibl:
            if sibl.is_attribute:
                sibl = rightsibling(sibl)
                continue
            try:
                rel_id = sibl["rel_id"]
            except KeyError:
                rel_id = None
            # if rel_id is an integer, we can overwrite
            if rel_id is None or re.search(r"^[0-9]+$", str(rel_id)):
                if sibl.tag_name in self.tag_prefix.keys():
                    key = sibl.tag_name
                else:
                    key = 0
                relcounts[key] += 1
                sibl["rel_id"] = relcounts[key]
            else:
                # means, explicitly defined rel_id; skip
                pass
            sibl.generate_relids()
            sibl = rightsibling(sibl)

    def put_attrs_inside(self, dotted=False):
        # complies to xml strictly. means, attributes are not child nodes anymore. they become properties within opening node itself.
        for child in self.children:
            if child.is_attribute:
                if dotted:
                    child.parent[child.tag_name] = self.parse_ikml_node(str(child))[2]
                else:
                    child.parent[child.tag_name[1:]] = self.parse_ikml_node(str(child))[
                        2
                    ]
                child.parent = None
                continue
            child.put_attrs_inside(dotted)

    def to_xml(self, quoted_attr=True):
        root = self.__class__("[dummy_root]")
        root.children = [self]
        return "\n".join(self.__class__.tree_as_xml_list(root, quoted_attr))

    def to_dict(self, max_depth=-1):
        """
        max_depth represents the max level of recursion on children
        max_depth == 0, only the self node
        max_depth == 1, self and first level children
        max_depth == any negative value, infinite
        """
        if max_depth <= -1:
            max_depth = 9999
        dict_out = {"tag_name": self.tag_name, "content": self.content, "children": []}
        for k, v in self.props.items():
            dict_out[k] = v

        for child in self.children:
            if child.is_attribute:
                # do not remove the dot in tag_name
                # attr_name = child.tag_name[1:]
                dict_out[child.tag_name] = child.content

        if max_depth - self.depth == 0:
            return dict_out

        for child in self.children:
            if not child.is_attribute:
                dict_out["children"].append(
                    child.to_dict(max_depth=max_depth)
                )

        return dict_out

    def to_json(self, max_depth=-1):
        d = self.to_dict(max_depth=max_depth)
        return json.dumps(d, ensure_ascii=False, indent=self.INDENT)

    def to_txt(self, exclude_root=False, quoted_attr=False, max_depth=-1):
        if max_depth <= -1:
            max_depth = 9999
        d = self.tree_as_list(
            self, exclude_root=exclude_root, quoted_attr=quoted_attr, max_depth=max_depth
        )
        return "\n".join(d)

    @classmethod
    def tree_as_list(cls, root, exclude_root=False, quoted_attr=True, max_depth=-1):
        if max_depth <= -1:
            max_depth = 9999
        if exclude_root:
            ikml_out = []
            adjusted = 1
        else:
            ikml_out = [cls.__str__(root, quoted_attr)]
            adjusted = 0
        for child_node in root.children:
            for node in child_node.iter():
                if node.depth > max_depth + adjusted:
                    # do not break here. otherwise, rest of the nodes of same depth aren't displayed
                    continue
                ikml_out.append(
                    (node.depth - root.depth - adjusted) * cls.INDENT * " "
                    + cls.__str__(node, quoted_attr)
                )
        return ikml_out

    @classmethod
    def tree_as_xml_list(cls, root, quoted_attr=True):
        xmlout = []
        # only top level root children are considered
        for child in root.children:
            xmlout.append(cls.open_tag(cls.__str__(child, quoted_attr)))
            xmlout.extend(cls.tree_as_xml_list(child, quoted_attr) or [])
            xmlout.append(cls.close_tag(cls.__str__(child, quoted_attr)))
        return xmlout

    @staticmethod
    def parse_ikml_node(tagline):
        try:
            content = unescape(tagline.split("]", 1)[1].strip())
            core = re.findall(r"(\[.*?\])", tagline)[0].strip()
            tag_name = re.search(r"\[[ ]*([.A-z]+).*?\]", core).groups()[0].strip()
            return (tag_name, core, content)
        except:
            return ("", "[]", "")

    @classmethod
    def open_tag(cls, tagline):
        return tagline.strip().replace("[", "<").replace("]", ">")

    @classmethod
    def close_tag(cls, tagline):
        if not tagline.strip():
            return "</>"
        if tagline.strip()[0] != "[":
            return "</" + tagline + ">"
        tag_name, core, content = cls.parse_ikml_node(tagline)
        return "</" + tag_name + ">"

    @classmethod
    def update_tag_prefix(cls, tag_prefix):
        if tag_prefix is not None:
            cls.tag_prefix.update(cls._default_tag_prefix | tag_prefix)


def fix_root_prefix(root, root_prefix):
    # change is inplace for anytree Node
    if root_prefix:
        try:
            root["id"] = root_prefix + "." + root["rel_id"]
        except:
            root["id"] = root_prefix
        root["root_prefix"] = root_prefix


def ikml_to_anytree(ikml_data, root_prefix=None, tag_prefix=dict()):
    Node.update_tag_prefix(tag_prefix)
    root = Node(f"[root]")
    parents_stack = []
    prev_nd = root
    lvl = -1

    if isinstance(ikml_data, str):
        ikml_data = ikml_data.splitlines()

    for line in ikml_data:
        if not line.split("#")[0].strip():
            continue
        tindent = line.find("[")
        cur_lvl = int(tindent / INDENT)
        if cur_lvl > lvl:
            parents_stack.append(prev_nd)
        elif cur_lvl < lvl:
            try:
                while lvl != cur_lvl:
                    parents_stack.pop()
                    lvl -= 1
            except Exception as e:
                msg = "error in ikml_to_anytree. this or prev tag: " + line
                print(msg)
                break
        try:
            nd = Node(line.strip(), parent=parents_stack[-1])
            prev_nd = nd
        except Exception as e:
            msg = "error in ikml_to_anytree. this or prev tag: " + line
            print(msg)
            # raise e
            break
        lvl = cur_lvl

    fix_root_prefix(root, root_prefix)

    return root


def dict_to_anytree(ikml_dicts, root_prefix=None, tag_prefix=dict()):
    # ikml_dicts is a list of dict items
    if isinstance(ikml_dicts, dict):
        ikml_dicts = [ikml_dicts]

    Node.update_tag_prefix(tag_prefix)
    root = Node(f"[root]")

    # set the root props
    # root content must always be empty
    if ikml_dicts[0]["tag_name"] == "root":
        props = set(ikml_dicts[0].keys()) - set(("tag_name", "children", "content"))
        for p in props:
            root[p] = ikml_dicts[0][p]
        iterate_over_children = ikml_dicts[0]["children"]
    else:
        iterate_over_children = ikml_dicts

    def _dict_to_anytree(parent, children):
        if children is not None:
            for child in children:
                props = set(child.keys()) - set(("tag_name", "children", "content"))
                node = Node(f"[{child['tag_name']}]", parent=parent)
                node.content = child.get("content", "")
                for p in props:
                    if p.startswith("."):
                        Node(f"[{p}] {child[p]}", parent=node)
                    else:
                        node[p] = child[p]
                _dict_to_anytree(node, child.get("children"))

    _dict_to_anytree(root, iterate_over_children)

    fix_root_prefix(root, root_prefix)

    return root


if __name__ == "__main__":
    from sys import argv
    from pprint import pprint

    try:
        input_file = argv[1]
        ikml_data = open(input_file, encoding="utf-8").read().splitlines()
        root = ikml_to_anytree(ikml_data)
        pprint(root.to_txt())
    except IndexError:
        print(f"Usage: {argv[0]} input_ikml_file.txt")
