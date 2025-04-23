"""
SYNOPSIS
========


DESCRIPTION
===========

"""
import copy
from datetime import datetime, timezone
import logging

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

import re

import simplejson as json
from lxml import etree
from .xmldict import d2xml, xml2d, asbool

try:
    # StringResult no longer available lxml > 5
    from lxml.etree import _ElementStringResult
    etree_result_types = (etree._ElementStringResult, etree._ElementUnicodeResult)
except ImportError:
    etree_result_types = (etree._ElementUnicodeResult, )

log = logging.getLogger("bq.metadoc.formats")


# set following to True to force Metadoc everywhere
metadoc_everywhere = False


"""
Assume internal tree structure:

<RESERVED_TAGNAME uniq="00-xyz" name="..." type="image" usertype="cell image" unit="..."
 id="img1" path="..." owner="..." permission="..." storage="..." >    ...VALUE...
      <tag _id="09" name="NOT_RESERVED_TYPE" type="datetime" usertype="..." unit="..." id="..." >   ...VALUE...  </tag>
      ...
      <RESERVED_TAGNAME> ...VALUE... </RESERVED_TAGNAME>
      ...
</RESERVED_TAGNAME>


Assume external natural XML:

<VALID_XMLTAG .... >    ...value...
    <tag name="INVALID_XMLTAG" .... > ...VALUE... </tag>
    ...
    <VALID_XMLTAG .... > ...VALUE... </VALID_XMLTAG>
    ...
    <tag name="INVALID_XMLTAG" .... value="VALUE WITH SURROUNDING SPACES" />
    ...
</VALID_XMLTAG>


Assume external "tag-XML":

<RESERVED_TAGNAME ...  value="VALUE" >
    <tag name="NOT_RESERVED_TYPE" ...   value="VALUE" />
    ...
    <RESERVED_TAGNAME ...  value="VALUE" />
    ...
</RESERVED_TAGNAME>





The different converters work together as follows:

Convert from/to naturalxml:

NATURALXML str --> fromstring/deserialize --> NATURALXML etree* -->   naturalxml_to_tree  --> INTERNAL etree*
                   (resolves any empty                               (deals with leading/     (used in all internal ops;
                    string escapes)                                   trailing spaces in       ALL values in text nodes!)
                                                                      text nodes)

INTERNAL etree* -->   tree_to_naturalxml  -->  NATURALXML etree* -->  tostring/serialize  -->  NATURALXML str
                     (deals with leading/                             (escapes any empty
                      trailing spaces in                               text strings)
                      text nodes)


Convert from/to tagxml:

TAGXML str  -->  fromstring/deserialize  -->  TAGXML etree* -->  tagxml_to_tree  -->  INTERNAL etree*
                 (no special handling                            (moves values to
                  in this case)                                   text nodes)

INTERNAL etree* -->  tree_to_tagxml  -->  TAGXML etree* -->   tostring/serialize  -->  TAGXML str
                     (moves text nodes                        (no special handling
                      to value attr)                           in this case)


Convert from/to naturaljson:

NATURALJSON str  -->  json.load  -->  NATURALJSON struct  -->  d2xml  -->  NATURALXML etree*  -->  naturalxml_to_tree  -->  INTERNAL etree*
                                                              ("simulate"  (same as above ------> )
                                                               leading/
                                                               trailing space
                                                               escape)

INTERNAL etree*  -->  tree_to_naturalxml  -->  NATURALXML etree* -->  xml2d  -->  NATURALJSON struct  -->  json.dumps  -->  NATURALJSON str
                                      (<--------- same as above)     (resolve
                                                                      leading/
                                                                      trailing space
                                                                      escape)

Serialize/deserialize (for task communication):

INTERNAL etree* -->  tostring/serialize  -->  INTERNAL str
                     (escapes any empty
                      text strings)

INTERNAL str  -->  fromstring/deserialize -->  INTERNAL etree*
                   (resolves any empty
                    string escapes)


(* these etrees will be replaced with Metadoc eventually)
"""


# TODO: extract 'system types' from plugins at startup
RESERVED_TAGNAMES = {
    "resource",
    "system",
    "user",
    "_user",
    "mex",
    "module",
    "build",
    "sourcecode",
    "template",
    "dataset",
    "session",
    "tag",
    "gobject",
    # the following are not reserved because we currently store all of these gobjects as
    # <gobject type="line">coord1;coord2;...</gobject>
    # 'point', 'polyline', 'polygon', 'circle', 'ellipse', 'rectangle', 'square', 'line', 'label',
    "dream3d_pipeline",
    "bisque_pipeline",
    "cellprofiler_pipeline",
    "imagej_pipeline",
    "service",
    "image",
    "connoisseur",  # ML model
    "store",
    "mount",
    "dir",
    "file",
    "table",
    "tablecontainer",
    "text",
    "pdf",
    "html",
    "html_fragment",
    "molecule",
    "preference",
    "annotation",
    "acl",
    "group",
    "value",
    "container",  # used by dirs
    "response",  # used by imgsrv for responses
    "operations",  # used by imgsrv
    "format",  # used by imgsrv
    "codec",  # used by imgsrv
    "method",  # used by imgsrv
    "result",  # for query results
    "layer",  # layer used for named image layers
    "plotly",
    "future",
    "avia_config",  # client config resource
    "avia_project",  # project to build aa AVIA model for specific virus/strain/etc
    "avia_platemap",  # platemap resource (for ingester)
    "microplate",  # microplate with wells
}


#  Setup a default parser
#
#
XML_PARSER = etree.XMLParser(remove_comments=True)
etree.set_default_parser(XML_PARSER)


if metadoc_everywhere:

    def _tree_to_metadoc(tree):
        return Metadoc(et=tree)

else:

    def _tree_to_metadoc(tree):
        return tree


def _fromstring_fix_empty(s):
    res = etree.fromstring(s)
    # fix any escaped empty strings
    for kid in res.iter(tag=etree.Element):
        if kid.attrib.get("value") == "":
            del kid.attrib["value"]
            kid.text = ""
    return res


def _tostring_fix_empty(xml, **kw):
    # escape any empty strings (XML is not round-tripable for empty strings in text nodes!)
    inplace_changes = []
    for kid in xml.iter(tag=etree.Element):
        if kid.text == "":
            kid.text = None
            kid.set("value", "")
            inplace_changes.append(kid)
    res = etree.tostring(xml, encoding="unicode")
    for kid in inplace_changes:
        kid.text = ""
        del kid.attrib["value"]
    return res


def _text_to_number(val: str):
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val

def _text_to_native(val: str | None, ntype: str):
    if not val:
        return val
    match ntype:
        case "number":
            return _text_to_number(val)
        case "datetime":
            return datetime.fromisoformat(val)
        case "boolean":
            return asbool(val)
        case "list":
            return val.split(";")
        case "list[boolean]":
            return [asbool(tok) for tok in val.split(";")]
        case "list[number]":
            return [_text_to_number(tok) for tok in val.split(";")]
        case _:
            return val

def _native_to_text(val, attr: str | None = None) -> (str, str):
    if val is None:
        res = (None, None)
    elif isinstance(val, bool):
        res = (str(val).lower(), "boolean")
    elif isinstance(val, int | float):
        res = (str(val), "number")
    elif isinstance(val, datetime):
        if val.tzinfo is None or val.tzinfo.utcoffset(val) is None:
            # no timezone => assume UTC
            val = val.replace(tzinfo=timezone.utc)
        res = (val.isoformat(), "datetime")
    elif isinstance(val, list):
        if len(val) > 0 and isinstance(val[0], bool):
            res = (";".join(str(tok).lower() for tok in val), "list[boolean]")
        elif len(val) > 0 and isinstance(val[0], int | float):
            res = (";".join(str(tok) for tok in val), "list[number]")
        else:
            res = (";".join(str(tok) for tok in val), "list")
    else:
        res = (str(val), None)
    if attr in ("ts", "created"):
        if res[1] is None:
            try:
                # got string; check if it's a datetime
                datetime.fromisoformat(val)
                # yes it is
                res = (str(val), "datetime")
            except ValueError:
                pass
        if res[1] != "datetime":
            raise AttributeError(f'Attribute "{attr}" has to be of type datetime but got "{val}"')
    return res

def _adjust_attrs(attrs: dict) -> dict:
    return {k: _native_to_text(v, k)[0] for k, v in attrs.items()}

def _strip_attrs(doc):
    if isinstance(doc, dict):
        res = {k: _strip_attrs(v) for k, v in doc.items() if not k.startswith("@") or k == "@value"}
        if res == {}:
            res = None  # TODO: could be done for general d2xml/xml2d case that {}==None?
        elif set(res.keys()) == {"@value"}:
            # only @value left => make it direct value
            res = res["@value"]
    elif isinstance(doc, list):
        res = [_strip_attrs(item) for item in doc]
    else:
        res = doc
    return res

class InvalidFormat(Exception):
    pass


def _clean_tree(elem, del_uri=True):
    res = copy.deepcopy(elem)
    _clean_tree_rec(res, del_uri=del_uri)
    return res

def _clean_tree_rec(elem, del_uri=True):
    elem.attrib.pop("_id", None)
    if del_uri is True:
        elem.attrib.pop("uri", None)
    for kid in elem:
        _clean_tree_rec(kid, del_uri=del_uri)


def _tree_to_naturalxml(tree, keep_text=False):
    """WARNING: MODIFIES TREE IN PLACE!"""
    for node in tree.iter(tag=etree.Element):
        if node.tag == "tag":
            try:
                node.tag = node.get("name", "tag")
                node.attrib.pop("name", None)
            except ValueError:
                pass
        if not keep_text and node.text is not None and node.text.strip() != node.text:
            # values surrounded by spaces are "escaped" with value= to avoid ambiguities
            node.set("value", node.text)
            node.text = None
    return tree


def _naturalxml_to_tree(tree, keep_text=False):
    """WARNING: MODIFIES TREE IN PLACE!"""
    for el in tree.iter(tag=etree.Element):
        if el.tag == "tag":
            try:
                _ = etree.Element(el.get("name", ""))
                raise InvalidFormat(
                    "Invalid natural XML (name %s should be tag)" % el.get("name")
                )
            except ValueError:
                pass
        elif el.tag not in RESERVED_TAGNAMES and "name" in el.attrib:
            raise InvalidFormat(
                "Invalid natural XML (tag %s cannot have a name)" % el.tag
            )
        val = el.get("value")
        if val is not None:
            if val.strip() == val:
                raise InvalidFormat(
                    "Invalid natural XML (value attribute should be in text node, unless it has leading/trailing spaces)"
                )
            else:
                el.text = val
                el.attrib.pop("value")
        elif not keep_text and el.text is not None and el.text.strip() != el.text:
            # leading/trailing spaces are stripped from text nodes for convenience; if needed, use value= escape
            stripped = el.text.strip()
            el.text = stripped if stripped else None
        if el.tag not in RESERVED_TAGNAMES and el.tag != "tag":
            el.set("name", el.tag)
            el.tag = "tag"
    return tree


def _tree_to_tagxml(tree):
    """WARNING: MODIFIES TREE IN PLACE!"""
    for node in tree.iter(tag=etree.Element):
        if node.text is not None:
            node.set("value", node.text)
            node.text = None
    return tree


def _tagxml_to_tree(tree):
    """WARNING: MODIFIES TREE IN PLACE!"""
    for el in tree.iter(tag=etree.Element):
        if el.tag != "tag" and el.tag not in RESERVED_TAGNAMES:
            raise InvalidFormat("Invalid tag XML (tag %s should be name)" % el.tag)
        if el.tag == "tag" and el.get("name", "") in RESERVED_TAGNAMES:
            raise InvalidFormat(
                "Invalid tag XML (name %s should be tag)" % el.get("name")
            )
        if el.text:
            if el.text.strip():
                raise InvalidFormat(
                    "Invalid tag XML (text node should be in 'value' attribute)"
                )
            # leading/trailing spaces are stripped from text nodes for convenience
            el.text = None
        val = el.attrib.pop("value", None)
        if val is not None:
            el.text = val
    return tree


def internal_to_naturaljson(xmldoc):
    xmldoc = xmldoc.node if isinstance(xmldoc, Metadoc) else xmldoc
    xmldoc = copy.deepcopy(xmldoc)  # because _tree_to_naturalxml modifies in place
    return xml2d(
        _tree_to_naturalxml(xmldoc, keep_text=True),
        attribute_prefix="@",
        keep_tags=False,
    )


def internal_to_tagjson(xmldoc):
    xmldoc = xmldoc.node if isinstance(xmldoc, Metadoc) else xmldoc
    xmldoc = copy.deepcopy(xmldoc)  # because _tree_to_naturalxml modifies in place
    return xml2d(_tree_to_tagxml(xmldoc), attribute_prefix="@", keep_tags=True)


def internal_to_naturalxml(xmldoc):
    xmldoc = xmldoc.node if isinstance(xmldoc, Metadoc) else xmldoc
    xmldoc = copy.deepcopy(xmldoc)  # because _tree_to_naturalxml modifies in place
    return _tree_to_naturalxml(xmldoc)


def internal_to_tagxml(xmldoc):
    xmldoc = xmldoc.node if isinstance(xmldoc, Metadoc) else xmldoc
    xmldoc = copy.deepcopy(xmldoc)  # because _tree_to_tagxml modifies in place
    return _tree_to_tagxml(xmldoc)


def naturaljson_to_internal(jsondoc):
    return _tree_to_metadoc(
        _naturalxml_to_tree(
            d2xml(jsondoc, attribute_prefix="@", keep_value_attr=False), keep_text=True
        )
    )


def tagjson_to_internal(jsondoc):
    return _tree_to_metadoc(
        _tagxml_to_tree(d2xml(jsondoc, attribute_prefix="@", keep_value_attr=True))
    )


def naturalxml_to_internal(xmldoc):
    if isinstance(xmldoc, str):
        xmldoc = _fromstring_fix_empty(xmldoc)
    else:
        xmldoc = copy.deepcopy(xmldoc)  # because _naturalxml_to_tree modifies in place
    return _tree_to_metadoc(_naturalxml_to_tree(xmldoc))


def tagxml_to_internal(xmldoc):
    if isinstance(xmldoc, str):
        xmldoc = _fromstring_fix_empty(xmldoc)
    else:
        xmldoc = copy.deepcopy(xmldoc)  # because _tagxml_to_tree modifies in place
    return _tree_to_metadoc(_tagxml_to_tree(xmldoc))


# ----- TODO: GET RID OF THE FOLLOWING FCT EVENTUALLY (ONLY NEEDED TO TRANSITION LEGACY CODE MORE EASILY) ------
def anyxml_to_etree(tree):
    """Convert any XML format to proper internal etree. Only needed temporarily to clean up legacy code.
    WARNING: MODIFIES TREE IN PLACE!
    """
    if isinstance(tree, str):
        tree = etree.fromstring(tree)
    elif not isinstance(tree, etree._Element):
        # must be file like
        tree = etree.parse(tree).getroot()
    for el in tree.iter(tag=etree.Element):
        if el.tag != "tag" and el.tag not in RESERVED_TAGNAMES:
            el.set("name", el.tag)
            el.tag = "tag"
        elif el.tag == "tag" and el.get("name", "") in RESERVED_TAGNAMES:
            el.tag = el.attrib.pop("name")
        val = el.attrib.pop("value", None)
        if el.text is not None and el.text.strip() != el.text:
            # leading/trailing spaces are stripped from text nodes for convenience; if needed, use value= escape
            stripped = el.text.strip()
            el.text = stripped if stripped else None
        if val is not None and not el.text:
            el.text = val
    return tree


# -------------------------------------------------------------------------------------------------------------
# internal XML specific selectors... may be replaced later when switching everything to JSON


class Metadoc:
    """
    Class representing any nested metadata document.
    Interface is similar to :py:class:`xml.etree.ElementTree`.
    """
    class AttribProxy(MutableMapping):
        def __init__(self, doc):
            self.doc = doc

        def __iter__(self): #!!! also add __next__
            yield from self.doc.node.attrib

        def __getitem__(self, key):
            if isinstance(key, int):
                raise IndexError("cannot get attribute by index")
            else:
                return self.doc.get_attr(key)

        def __setitem__(self, key, val):
            if isinstance(key, int):
                raise IndexError("cannot set attribute by index")
            else:
                self.doc.set_attr(key, val)

        def __delitem__(self, key):
            if isinstance(key, int):
                raise IndexError("cannot delete attribute by index")
            else:
                self.doc.del_attr(key)

        def __len__(self):
            return len(self.doc.node.attrib)

        def __contains__(self, key):
            return key in self.doc.node.attrib

    def __init__(self, et=None, parent=None, tag=None, **attrs):
        # convert to proper "internal etree" format (tagxml with text nodes) as needed
        # this is to deal with all inconsistent etree structures across the codebase
        # NOTE: "node" is assumed to already be in proper internal etree format, if present
        if et is not None:
            tag = et.tag
            ntype = et.get("type")
            val = et.text
        else:
            # validate here that tag/attrs constitutes proper internal etree format   #!!!! different attr types
            # and correct if needed
            if tag == "tag" and attrs.get("name", "tag") in RESERVED_TAGNAMES:
                tag = attrs.pop("name", "tag")
            ntype = attrs.pop("type", None)
            val = attrs.pop("value", None)
        if tag in RESERVED_TAGNAMES or tag == "tag":
            if parent is None:
                if et is not None:
                    res = et
                else:
                    res = etree.Element(tag, **_adjust_attrs(attrs))
            else:
                if et is not None:
                    parent.append(et)
                    res = et
                else:
                    res = etree.SubElement(parent, tag, **_adjust_attrs(attrs))
        else:
            if parent is None:
                if et is not None:
                    et.tag = "tag"
                    et.set("name", tag)
                    res = et
                else:
                    attrs.pop("name", None)
                    res = etree.Element("tag", name=tag, **_adjust_attrs(attrs))
            else:
                if et is not None:
                    et.tag = "tag"
                    et.set("name", tag)
                    parent.append(et)
                    res = et
                else:
                    attrs.pop("name", None)
                    res = etree.SubElement(parent, "tag", name=tag, **_adjust_attrs(attrs))
        if et is None:
            if ntype is None:  # if type provided, don't override
                res.text, ntype = _native_to_text(val)
            else:
                res.text, _ = _native_to_text(val)
            # previously set types are never overwritten
            if ntype is not None and "type" not in res.attrib:
                res.set("type", ntype)
        self.node = res

    def __getstate__(self):
        return self.serialize()

    def __setstate__(self, s):
        self.node = self.deserialize(s).node

    @staticmethod
    def convert(internal):
        if isinstance(internal, Metadoc):
            return internal
        if isinstance(internal, etree._Element):
            return Metadoc(et=internal)
        elif isinstance(internal, etree._ElementTree):
            return Metadoc(et=internal.getroot())
        elif isinstance(
                #internal, (etree._ElementUnicodeResult, etree._ElementStringResult)
                # StringResult no longer available lxml > 5
            internal, etree_result_types
        ):
            return str(internal)
        elif isinstance(internal, list):
            return [Metadoc.convert(it) for it in internal]
        elif not internal:  # None, empty string ,or  empty list
            return None
        else:
            return (Metadoc.convert(it) for it in internal)

    @staticmethod
    def convert_back(metadoc):
        if metadoc_everywhere:
            return metadoc
        else:
            return metadoc.node

    @staticmethod
    def convert_to_etree(metadoc):
        return Metadoc.convert_back(metadoc)

    @staticmethod
    def from_tagxml(xmldoc: str) -> "Metadoc":
        """
        Create metadoc from "tag" XML string.

        Args:
            xmldoc: "tag" XML string

        Returns:
            created metadoc
        """
        try:
            xmldoc = _fromstring_fix_empty(xmldoc)
        except etree.ParseError as e:
            raise InvalidFormat(e)
        return Metadoc.from_tagxml_etree(xmldoc)

    @staticmethod
    def from_tagxml_etree(xmldoc):
        return Metadoc(et=tagxml_to_internal(xmldoc))

    def to_tagxml(self) -> str:
        """
        Convert this metadoc to "tag" XML string.

        Returns:
            "tag" XML string
        """
        return _tostring_fix_empty(self.to_tagxml_etree(), encoding="unicode")

    def to_tagxml_etree(self):
        return internal_to_tagxml(self.node)

    @staticmethod
    def from_naturalxml(xmldoc: str) -> "Metadoc":
        """
        Create metadoc from "natural" XML string.

        Args:
            xmldoc: "natural" XML string

        Returns:
            created metadoc
        """
        try:
            xmldoc = _fromstring_fix_empty(xmldoc)
        except etree.ParseError as e:
            raise InvalidFormat(e)
        return Metadoc.from_naturalxml_etree(xmldoc)

    @staticmethod
    def from_naturalxml_etree(xmldoc):
        return Metadoc(et=naturalxml_to_internal(xmldoc))

    def to_naturalxml(self) -> str:
        """
        Convert this metadoc to "natural" XML string.

        Returns:
            "natural" XML string
        """
        return _tostring_fix_empty(self.to_naturalxml_etree(), encoding="unicode")

    def to_naturalxml_etree(self):
        return internal_to_naturalxml(self.node)

    @staticmethod
    def from_json(jsondoc) -> "Metadoc":
        """
        Create metadoc from JSON-like Python structure.

        Args:
            jsondoc: JSON-like Python structure

        Returns:
            created metadoc
        """
        return Metadoc(et=naturaljson_to_internal(jsondoc))

    def to_json(self) -> dict:
        """
        Convert this metadoc to JSON-like Python structure

        Returns:
            JSON-like Python structure of dicts and lists
        """
        return internal_to_naturaljson(self.node)

    def as_xml(self) -> str:
        """
        Get tags in metadoc as "natural" XML string.
        This is NOT round-tripable through from_naturalxml!

        Returns:
            "natural" XML string
        """
        res = internal_to_naturalxml(_clean_tree(self.node))
        return _tostring_fix_empty(res, encoding="unicode")

    def as_dict(self, strip_attributes: bool = False) -> dict:
        """
        Get all tags in metadoc as a dictionary.
        This is NOT round-tripable through from_json!

        Args:
            strip_attributes: if True, removes all attributes (keys starting with "@")

        Returns:
            dict
        """
        res = internal_to_naturaljson(_clean_tree(self.node))
        if len(res.keys()) == 1:
            res = res[list(res.keys())[0]]
        if strip_attributes:
            res = _strip_attrs(res)
        return res

    def clean(self) -> "Metadoc":
        """
        Return a "cleaned" version of the doc (i.e., stripped URIs and IDs).

        Returns:
            cleaned doc
        """
        return Metadoc(et=_clean_tree(self.node))

    def __iter__(self): #!!! also add __next__
        for kid in self.node:
            yield Metadoc(et=kid)

    def __getitem__(self, ix):
        return Metadoc(et=self.node[ix])

    def __len__(self):
        return len(self.node)

    def __getattr__(self, name):
        if name == "node":
            return self.__dict__[name]
        if name == "text":
            return self.get_value_str()
        if name == "value":
            return self.get_value()
        if name == "tag":
            return self.get_tag()
        if name == "type":
            return self.get_attr("type")
        if name == "name":
            return self.get_attr("name")
        if name == "attrib":
            return self.AttribProxy(self)
        raise AttributeError(f'\'unknown Metadoc attribute "{name}"')

    def __setattr__(self, name, val):
        if name == "node":
            self.__dict__[name] = val
            return
        if name == "text" or name == "value":
            self.set_value(val)
            return
        if name == "type":
            self.set_attr("type", val)
            return
        if name == "name":
            self.set_attr("name", val)
            return
        if name == "tag":
            self.node.tag = val
            return
        raise AttributeError(f'unknown Metadoc attribute "{name}"')

    def get_tag(self):
        if self.node.tag == "tag":
            return self.node.get("name", "tag")
        else:
            return self.node.tag

    def get_value(self):  #!!! also add get_path()
        return _text_to_native(self.node.text, self.node.get("type"))

    def get_value_str(self):
        return self.node.text

    def set_value(self, val):
        txt, ntype = _native_to_text(val)
        self.node.text = txt
        if ntype is not None and "type" not in self.node.attrib:
            self.node.set("type", ntype)

    def get_attr(self, attr, default=None):
        if attr == "value":
            res = self.get_value()
            return res if res is not None else default
        else:
            if attr in ("created", "ts"):
                ntype = "datetime"
            else:
                ntype = None
            res = self.node.get(attr)
            return _text_to_native(res, ntype) if res is not None else default

    def get_attr_str(self, attr, default=None):
        if attr == "value":
            res = self.get_value_str()
            return res if res is not None else default
        else:
            res = self.node.get(attr)
            return res if res is not None else default

    get = get_attr_str  # alias for etree legacy

    def del_attr(self, attr):
        if attr == "value":
            self.node.text = None
        else:
            del self.node.attrib[attr]

    def set_attr(self, attr, val):
        if attr == "value":
            self.set_value(val)
        else:
            txt, _ = _native_to_text(val, attr)
            self.node.set(attr, txt)

    set = set_attr  # alias for etree legacy

    def keys(self):
        return self.node.keys()

    def get_docid(self):
        return self.node.get("resource_uniq")

    def get_parent(self):
        parent = self.node.getparent()
        return Metadoc(et=parent) if parent is not None else None

    @staticmethod
    def create_doc(tag, **attrs):
        return Metadoc(tag=tag, **attrs)

    def add_sibling(self, tag, **attrs):
        return Metadoc(parent=self.node.getparent(), tag=tag, **attrs)

    def add_tag(self, tag, **attrs):
        return Metadoc(parent=self.node, tag=tag, **attrs)

    def replace_with(self, doc):
        if self.node.getparent() is not None:
            self.node.getparent().replace(self.node, doc.node)

    def delete(self):
        if self.node.getparent() is not None:
            self.node.getparent().remove(self.node)

    def add_child(self, newchild):
        self.node.append(newchild.node)
        return newchild

    append = add_child  # alias for etree legacy

    def extend(self, newchildren):
        self.node.extend(kid.node for kid in newchildren)

    def iter(self, tag=None):
        for node in self.node.iter(tag=tag):
            yield Metadoc(et=node)

    @staticmethod
    def from_etree_like_string(s):
        res = anyxml_to_etree(s)
        # fix any escaped empty strings
        for kid in res.iter(tag=etree.Element):
            if kid.attrib.get("value") == "":
                del kid.attrib["value"]
                kid.text = ""
        return Metadoc(et=res)

    def to_etree_like_string(self):
        # escape any empty strings (XML is not round-tripable for empty strings in text nodes!)
        return _tostring_fix_empty(self.node, encoding="unicode")

    deserialize = from_tagxml
    serialize = to_tagxml

    def __str__(self):
        return self.to_etree_like_string()
        # TODO: better return as JSON

    def __repr__(self):
        return f"metadoc:{self.to_etree_like_string()}"
        # TODO: better return as JSON

    def _path_to_xpath(self, path):
        path = path.strip()
        if re.match(
            r"""^[\w"']""", path
        ):  # TODO: right now every tag has to start with '/' otherwise the regex below won't work
            path = "./" + path

        # split into quoted and non-quoted parts
        QUOTED_STRING = re.compile("(\\\\?[\"']).*?\\1")  # a pattern to match strings between quotes
        result = []  # a store for the result pieces
        head = 0  # a search head reference
        for match in QUOTED_STRING.finditer(path):
            # process everything until the current quoted match and add it to the result
            unquoted_part = path[head:match.start()]
            quoted_part = match[0]
            if unquoted_part.endswith("/"):
                # slash followed by quoted is escaped tag name, include it
                unquoted_part = unquoted_part + quoted_part
                quoted_part = ""
            result.append(self._path_to_xpath_single(unquoted_part))
            result.append(quoted_part)  # add the quoted match verbatim to the result
            head = match.end()  # move the search head to the end of the quoted match
        if head < len(path):  # if the search head is not at the end of the string
            # process the rest of the string and add it to the result
            result.append(self._path_to_xpath_single(path[head:]))
        return "".join(result)  # join back the result pieces and return them

    def _path_to_xpath_single(self, path):
        res = ""
        path_pos = 0
        p = re.compile(
            r"""@[\w -]+|/[^"'/.*@[\]]+|/"[^"]+"|/'[^']+'"""
        )  # allow to escape tag names with " or '
        for m in p.finditer(path):
            pos = m.start()
            end = m.end()
            tok = m.group().strip()
            if tok == "@value":
                new_tok = " text()"
            elif tok[0] == "@":
                new_tok = " " + tok
            elif tok[0] == "/":
                newname = tok[1:].strip()
                if newname.startswith('"') or newname.startswith("'"):
                    newname = newname[1:-1]
                if newname not in RESERVED_TAGNAMES:
                    new_tok = f'/tag[@name="{newname}"]'
                else:
                    new_tok = tok
            res += path[path_pos:pos] + new_tok
            path_pos = end
        res += path[path_pos:]
        return res

    def path_query(self, path: str) -> list["Metadoc"]:
        """
        Select nodes in this metadoc based on a path selector.

        Args:
            path: path query (e.g., ``'//my tag/another tag with spaces[@attr = "...."]'``)
        """

        # generic path query (Xpath/JSONpath compatible)
        # e.g.: '//my tag/another tag with spaces[@attr = "...."]'
        # becomes '//tag[@name="my tag"]/tag[@name="another tag with spaces"][@attr = "...."]' for Xpath
        # becomes '$..['my tag']['another tag with spaces'][?(@.attr = "....")]' for JSONpath
        xpath = self._path_to_xpath(path)
        log.debug(f"path_query {path} -> {xpath}")
        return Metadoc.convert(self.node.xpath(xpath))

    def xpath(self, xpath):
        # legacy... these are likely using "tag[@name='xxx']", so should work as is
        return Metadoc.convert(self.node.xpath(xpath))

    findall = xpath  # alias for etree legacy

    def find(self, xpath):
        # legacy... these are likely using "tag[@name='xxx']", so should work as is
        res = self.node.find(xpath)
        return Metadoc(et=res) if res is not None else None


# -------------------------------------------------------------------------------------------------------------
