import os
import inspect
import logging
import typing
import contextlib
import mimetypes

from datetime import date
from difflib import SequenceMatcher
from enum import Enum

from typing import BinaryIO

import uvicorn

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import (
    JSONResponse,
    Response,
    FileResponse,
    StreamingResponse,
)


logger = logging.getLogger("glootil")

UnionType = type(str | None)
NoneType = type(None)

# first level is the type of input, second is expected output type
# JSON_CASTER[from][to]
JSON_CASTERS = {
    float: {
        NoneType: lambda _v, _d: None,
        float: lambda v, _d: v,
        str: lambda v, _d: str(v),
        int: lambda v, _d: int(v),
        bool: lambda v, _d: bool(v),
        date: lambda _v, d: cast_date_default(d),
    },
    int: {
        NoneType: lambda _v, _d: None,
        int: lambda v, _d: v,
        str: lambda v, _d: str(v),
        float: lambda v, _d: float(v),
        bool: lambda v, _d: bool(v),
        date: lambda _v, d: cast_date_default(d),
    },
    str: {
        NoneType: lambda _v, _d: None,
        str: lambda v, _d: v,
        int: lambda v, d: try_cast_or(v, int, d),
        float: lambda v, d: try_cast_or(v, float, d),
        bool: lambda v, d: try_cast_or(v, bool, d),
        date: lambda v, d: try_cast_or(v, date.fromisoformat, d, cast_date_default),
    },
    bool: {
        NoneType: lambda _v, _d: None,
        bool: lambda v, _d: v,
        str: lambda v, _d: str(v),
        int: lambda v, _d: int(v),
        float: lambda v, _d: float(v),
        date: lambda _v, d: cast_date_default(d),
    },
    NoneType: {
        NoneType: lambda _v, _d: None,
        bool: lambda _v, d: d,
        str: lambda _v, d: d,
        int: lambda _v, d: d,
        float: lambda _v, d: d,
        date: lambda _v, d: cast_date_default(d),
    },
}


def cast_date_default(v):
    # TODO: handle a way to have dynamic default like "today"
    if is_date(v):
        return v
    else:
        logger.warning("Invalid default date format: %s", v)
        return None


def identity(v):
    return v


def try_cast_or(v, cast_fn, default, default_caster=identity):
    try:
        return cast_fn(v)
    except Exception as err:
        logger.warning("couldn't cast returning default: %s", err)
        return default_caster(default)


def cast_json_type_to_fn_arg_type_or_default(v, target_type, default):
    v_type = type(v)
    caster = JSON_CASTERS.get(v_type, {}).get(target_type)
    if caster:
        return caster(v, default)
    else:
        logger.warning(
            "no caster found from %s to %s, returning default", v_type, target_type
        )
        return default


def date_to_data_tag(d):
    return ["dt", d] if d else None


class FnArg:
    def __init__(self, name, index, type_, default_value):
        self.name = name
        self.index = index
        if type_ and typing.get_origin(type_) is UnionType:
            targs = typing.get_args(type_)
            ta, tb = targs
            if len(targs) == 2 and (ta is NoneType or tb is NoneType):
                self.type = ta if tb is NoneType else tb
                self._isinstance_type = targs
            else:
                raise ValueError("FnArg type Union can only be with None")
        else:
            # assert that it's a type
            assert type_ is None or isinstance(type_, type)
            self.type = type_

            if type_ is None:
                self._isinstance_type = object
            elif type_ is float:
                self._isinstance_type = (int, float)
            else:
                self._isinstance_type = type_

        self.default_value = default_value

    def cast_json_value_or_default(self, v):
        "cast a value that came from json, handles only int, float, bool, null, string"
        return cast_json_type_to_fn_arg_type_or_default(
            v, self.type, self.default_value
        )

    def __str__(self):
        return f"{self.name}[{self.index}]: {self.type} = {self.default_value}"


class ToolArg(FnArg):
    def __init__(self, name, index, type, default_value, label=None):
        super().__init__(name, index, type, default_value)
        self.docs = None
        self.label = label or name

    def __str__(self):
        return f"{self.label}[{self.index}]: {self.type} = {self.default_value}"

    def to_schema_info(self):
        type, default, format = type_to_schema_type(self.type, self.default_value)

        if not self.docs and is_any_enum(self.type):
            desc = self.type.__doc__
        else:
            desc = self.docs

        info = {
            "type": type,
            "default": default,
            "description": desc,
        }

        if format:
            info["format"] = format

        return info

    def to_ui_info(self, toolbox):
        tag_value = toolbox.enum_class_to_wrapper.get(self.type)
        if tag_value:
            return {"prefix": self.label, "dtypeName": tag_value.id}
        else:
            return {"prefix": self.label}

    def apply_overrides(self, d):
        name = d.get("name")
        docs = d.get("docs")

        if name:
            self.label = name

        if docs:
            self.docs = docs


def is_any_enum(t):
    return isinstance(t, type) and issubclass(t, (Enum, DynEnum))


def is_enum(t):
    return isinstance(t, type) and issubclass(t, Enum)


def is_dyn_enum(t):
    return isinstance(t, type) and issubclass(t, DynEnum)


def is_str(v):
    return isinstance(v, str)


def is_int(v):
    return isinstance(v, int)


def is_dict(v):
    return isinstance(v, dict)


def is_list(v):
    return isinstance(v, list)


def is_seq(v):
    return isinstance(v, (tuple, list))


def is_date(v):
    return isinstance(v, date)


def has_static_method(Class, name):
    f = Class.__dict__.get(name, None)
    return callable(f) and isinstance(f, staticmethod)


def has_class_method(Class, name):
    m = getattr(Class, name, None)
    return inspect.ismethod(m)


def type_to_schema_type(t, default):
    if t is float:
        return "number", default if default is not None else 0.0, None
    elif t is str:
        return "string", default if default is not None else "", None
    elif t is bool:
        return "boolean", default if default is not None else False, None
    elif t is int:
        return "integer", default if default is not None else 0, None
    elif t is date:
        return "string", default, "date"
    else:
        if not is_any_enum(t):
            logger.warning("unknown type for schema %s, returning string", t)
        return "string", "", None


class FnInfo:
    def __init__(self, fn, name, docs, args, return_type=None):
        self.fn = fn
        self.name = name
        self.docs = docs
        self.args = args
        self.return_type = return_type

    def __str__(self):
        return f"def {self.name}({', '.join([str(arg) for arg in self.args])}) -> {self.return_type}:\n\t{self.docs}"

    async def call_with_args(self, args_provider, info, result_mapper=identity):
        arg_vals = []
        for arg in self.args:
            arg_val0 = args_provider.provide_arg(arg, info)
            if inspect.isawaitable(arg_val0):
                arg_val = await arg_val0
            else:
                arg_val = arg_val0

            arg_vals.append(arg_val if arg_val is not None else arg.default_value)

        result = await maybe_await(self.fn(*arg_vals))
        return result_mapper(result)

    @classmethod
    def make_arg(cls, name, i, arg_type, arg_default):
        return FnArg(name, i, arg_type, arg_default)

    @classmethod
    def from_function(cls, fn):
        fn_name = fn.__name__
        docs = fn.__doc__
        default_count = len(fn.__defaults__ or [])
        arg_names = fn.__code__.co_varnames[: fn.__code__.co_argcount]
        arg_types = {}
        arg_defaults = {}
        return_type = None

        args = []

        if fn.__defaults__:
            default_params = arg_names[-default_count:]
            for i, param in enumerate(default_params):
                arg_defaults[param] = fn.__defaults__[i]

        for param, annotation in fn.__annotations__.items():
            if param == "return":
                return_type = annotation
            else:
                arg_types[param] = annotation

        for i, name in enumerate(arg_names):
            arg_type = arg_types.get(name)
            arg_default = arg_defaults.get(name)
            args.append(cls.make_arg(name, i, arg_type, arg_default))

        return cls(fn, fn_name, docs, args, return_type)

    def apply_overrides(self, d):
        name = d.get("name")
        docs = d.get("docs")

        if name:
            self.name = name

        if docs:
            self.docs = docs


class Tool(FnInfo):
    def __init__(self, fn, name, docs, args, return_type=None, examples=None):
        super().__init__(fn, name, docs, args, return_type)
        self.id = name
        self.examples = examples if examples is not None else []
        self.ui_prefix = name
        self.manual_update = False

    @property
    def handler_id(self):
        return self.id

    @classmethod
    def make_arg(cls, name, i, arg_type, arg_default):
        return ToolArg(name, i, arg_type, arg_default)

    def to_context_actions(self, toolbox):
        r = []
        for arg in self.args:
            if is_any_enum(arg.type):
                info = toolbox.get_context_action_for_tool_enum_arg(self, arg)
                if info:
                    r.append(info)

        return r

    def to_info(self, toolbox):
        args = [arg for arg in self.args if arg.type is not toolbox.State]
        return {
            "title": self.name,
            "description": self.docs,
            "schema": {"fields": {arg.name: arg.to_schema_info() for arg in args}},
            "ui": {
                "prefix": self.ui_prefix,
                "args": {arg.name: arg.to_ui_info(toolbox) for arg in args},
                "manualUpdate": self.manual_update,
            },
            "contextActions": self.to_context_actions(toolbox),
            "examples": self.examples or [self.name],
        }

    def apply_overrides(self, d):
        id = d.get("id")
        name = d.get("name")
        docs = d.get("docs")
        args = d.get("args")
        examples = d.get("examples")
        ui_prefix = d.get("ui_prefix")
        manual_update = d.get("manual_update")

        if id:
            self.id = id

        if name:
            self.name = name

        if docs:
            self.docs = docs

        if args:
            args_by_name = {arg.name: arg for arg in self.args}
            for name, info in args.items():
                apply_arg_override(args_by_name, name, info)

        if examples:
            self.examples = examples

        if ui_prefix:
            self.ui_prefix = ui_prefix
        elif self.ui_prefix == self.id:
            self.ui_prefix = self.name

        if manual_update is not None:
            self.manual_update = manual_update


class Task(FnInfo):
    @property
    def handler_id(self):
        return f"Task::{self.name}"


class ContextActionHandler(FnInfo):
    @property
    def handler_id(self):
        return f"ContextActionHandler::{self.name}"


class ContextActionInfo:
    """
    Information related to a context action request
    Can be received as an argument to a @tb.context_action(...) handler
    """

    def __init__(self, value):
        self.value = value

    @classmethod
    def from_raw_info(cls, info):
        value = info.get("value")
        return cls(value)


class ResourceHandler(FnInfo):
    def __init__(self, fn, name, docs, args, return_type, for_type):
        super().__init__(fn, name, docs, args, return_type)
        self.for_type = for_type

    @classmethod
    def from_function_and_type(cls, fn, for_type):
        f = FnInfo.from_function(fn)
        return cls(fn, f.name, f.docs, f.args, f.return_type, for_type)


class ResourceInfo:
    def __init__(self, type, id, info={}):
        self.type = type
        self.id = id
        self.info = info


def apply_arg_override(args_by_name, name, info):
    arg = args_by_name.get(name)
    if arg:
        if is_dict(info):
            arg.apply_overrides(info)
        elif is_str(info):
            arg.apply_overrides({"name": info})
        else:
            logger.warning(
                "bad tool argument info format for argument '%s': %s", name, info
            )

    else:
        logger.warning("tool argument info for inexistent argument name '%s'", name)


def basic_match_raw_tag_value(word, possibilities):
    s = SequenceMatcher()
    s.set_seq2(word)

    best_key_index = -1
    best_key_ratio = -1
    best_key_pair = None

    best_value_index = -1
    best_value_ratio = -1
    best_value_pair = None

    for i, pair in enumerate(possibilities):
        key, value = pair

        s.set_seq1(key)
        key_ratio = s.ratio()
        if key_ratio > best_key_ratio:
            best_key_ratio = key_ratio
            best_key_index = i
            best_key_pair = pair

        s.set_seq1(value)
        value_ratio = s.ratio()
        if value_ratio > best_value_ratio:
            best_value_ratio = value_ratio
            best_value_index = i
            best_value_pair = pair

    if best_key_ratio > best_value_ratio:
        return best_key_index, best_key_pair
    else:
        return best_value_index, best_value_pair


def to_seq_of_pairs(seq):
    for k, v in seq:
        yield (k, v)


def to_list_of_pairs(seq):
    return list(to_seq_of_pairs(seq))


class KeyValue:
    def __repr__(self):
        return f"KeyValue({self.name}, {self.key}, {self.value})"

    def __str__(self):
        return self.key

    def __eq__(self, other):
        return (
            isinstance(other, KeyValue)
            and self.name == other.name
            and self.value == other.value
        )


class KeyValueEnum(KeyValue, Enum):
    def __new__(cls, key, value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.key = key
        return obj


class DynEnum:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def key(self):
        logger.warning("accessing deprecated property key in %s", repr(self))
        return self.name

    @property
    def label(self):
        logger.warning("accessing deprecated property label in %s", repr(self))
        return self.value

    def __repr__(self):
        return f"DynEnum({self.name}, {self.value})"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.name == other.name
            and self.value == other.value
        )


def is_valid_key_label(key, label):
    return (is_str(key) or is_int(key)) and is_str(label)


def is_seq_match_entry(v):
    if is_seq(v) and len(v) == 2:
        key, label = v
        return is_valid_key_label(key, label)


def get_dict_match_entry_key(v):
    return v.get("key") or v.get("id")


def get_dict_match_entry_label(v):
    return v.get("label") or v.get("name") or v.get("title")


def is_dict_match_entry(v):
    if is_dict(v):
        key = get_dict_match_entry_key(v)
        label = get_dict_match_entry_label(v)
        return is_valid_key_label(key, label)

    return False


def is_valid_match_entry(v):
    return (is_seq_match_entry(v)) or is_dict_match_entry(v)


def normalize_match_entry(entry):
    if is_seq_match_entry(entry):
        k, v = entry
        return (k, v)
    elif is_dict_match_entry(entry):
        key = get_dict_match_entry_key(entry)
        label = get_dict_match_entry_label(entry)
        return (key, label)
    else:
        raise ValueError("Invalid match entry format")


def match_result_to_response(v):
    if v is None:
        return {"entry": v}
    elif is_valid_match_entry(v):
        return {"entry": normalize_match_entry(v)}
    elif is_dict(v):
        entry = v.get("entry")
        if is_valid_match_entry(entry):
            return {"entry": normalize_match_entry(entry)}

    logger.warning(
        "bad enum match result format, expected 2 string item list or tuple or entry dict, got: %s",
        v,
    )
    return {"entry": None}


def extract_match_entry_key_and_label_or_none(m) -> tuple[str, str] | None:
    if m is None:
        return None

    if is_dict(m) and "entry" in m:
        entry = m.get("entry")
        if is_seq_match_entry(entry):
            return entry
        elif is_dict_match_entry(entry):
            key = get_dict_match_entry_key(entry)
            label = get_dict_match_entry_label(entry)
            return key, label

    if is_seq_match_entry(m):
        return m
    elif is_dict_match_entry(m):
        key = get_dict_match_entry_key(m)
        label = get_dict_match_entry_label(m)
        return key, label

    return None


def make_enum_dict(ns: str, id: str, key: str, label: str):
    return {"type": "enum", "ns": ns, "id": id, "key": key, "label": label}


def extract_key_and_label_from_enum_dict(v) -> tuple[str, str] | None:
    type = v.get("type")
    ns = v.get("ns")
    id = v.get("id")
    key = v.get("key")
    label = v.get("label")

    if type == "enum" and is_str(ns) and is_str(id) and is_valid_key_label(key, label):
        return key, label


def normalize_search_result_entries(entries):
    return [
        normalize_search_result_entry(entry)
        for entry in entries
        if is_valid_search_result_entry(entry)
    ]


def normalize_search_result_entry(entry):
    if is_seq_search_result_entry(entry):
        k, v = entry
        return k, v
    elif is_map_search_result_entry(entry):
        key = get_dict_match_entry_key(entry)
        label = get_dict_match_entry_label(entry)
        return key, label
    else:
        raise ValueError("Invalid search result entry format")


def is_valid_search_result_entry(entry):
    return is_seq_search_result_entry(entry) or is_map_search_result_entry(entry)


def is_seq_search_result_entry(entry):
    return is_seq_match_entry(entry)


def is_map_search_result_entry(entry):
    return is_dict_match_entry(entry)


def search_result_to_response(v):
    if is_list(v):
        return {"entries": normalize_search_result_entries(v)}
    elif is_dict(v):
        entries = v.get("entries")
        if isinstance(entries, list):
            return {"entries": normalize_search_result_entries(entries)}

    logger.warning(
        "bad enum search result format, expected list or entries dict, got: %s", v
    )
    return {"entries": []}


class TagValue:
    def __init__(self, id, name, docs, icon="list"):
        self.id = id
        self.name = name
        self.docs = docs
        self.icon = icon
        self.closest_matcher = basic_match_raw_tag_value

    def __repr__(self):
        return f"TagValue({self.id}, {self.name}, {self.docs})"

    def __str__(self):
        return self.id

    def to_info(self, _toolbox):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.docs,
            "icon": self.icon,
        }

    def from_key_and_label(self, key, label):
        logger.warning("TagValue from key and value not implemented: %s %s", key, label)
        return None

    async def from_raw_arg_value(self, v):
        t = None
        if is_str(v):
            m = await self.find_best_match(v)
            t = extract_match_entry_key_and_label_or_none(m)
        elif is_dict(v):
            t = extract_key_and_label_from_enum_dict(v)

        if t:
            key, label = t
            return self.from_key_and_label(key, label)
        elif t is not None:
            logger.warning("bad TagValue result format, got: %s", v)

        return None

    async def match_handler(self, info):
        query = info.get("query", "")
        return await self.find_best_match(query)

    async def load_handler(self, _info):
        entries = to_list_of_pairs(await self.get_variants())
        return dict(entries=entries)

    async def find_best_match(self, query):
        variant_pairs = to_seq_of_pairs(await self.get_variants())
        _, pair = self.closest_matcher(query, variant_pairs)
        return pair

    async def get_variants(self):
        return []

    def apply_overrides(self, d):
        id = d.get("id")
        name = d.get("name")
        docs = d.get("docs")
        icon = d.get("icon")
        matcher = d.get("matcher")

        if id:
            self.id = id

        if name:
            self.name = name

        if docs:
            self.docs = docs

        if icon:
            self.icon = icon

        if matcher:
            self.closest_matcher = matcher

    @classmethod
    def from_enum_class(cls, Class, overrides):
        id = Class.__name__
        name = id
        docs = Class.__doc__
        variants = []
        for variant in Class:
            variants.append(Variant.from_enum_variant(variant))

        e = FixedTagValue(id, name, docs, variants, Class)
        e.apply_overrides(overrides)

        return e

    @classmethod
    def from_dyn_enum_class(cls, Class, overrides, fn_arg_provider):
        id = Class.__name__
        name = id
        docs = Class.__doc__

        if has_static_method(Class, "load"):
            load_fn_info = FnInfo.from_function(Class.load)

            e = DynTagValue(
                id,
                name,
                docs,
                Class,
                lambda: load_fn_info.call_with_args(fn_arg_provider, {}),
            )
            e.apply_overrides(overrides)

            return e
        elif has_static_method(Class, "search"):
            search_fn_info = FnInfo.from_function(Class.search)
            if has_static_method(Class, "find_best_match"):
                find_best_match_fn_info = FnInfo.from_function(Class.find_best_match)
            else:
                find_best_match_fn_info = FnInfo.from_function(lambda: None)

            def search_fn(info):
                return search_fn_info.call_with_args(
                    fn_arg_provider, info, result_mapper=search_result_to_response
                )

            def find_best_match_fn(info):
                return find_best_match_fn_info.call_with_args(
                    fn_arg_provider, info, result_mapper=match_result_to_response
                )

            e = DynSearchTagValue(id, name, docs, Class, search_fn, find_best_match_fn)
            e.apply_overrides(overrides)

            return e
        else:
            raise ValueError("DynEnum must have either a load or a search classmethod")


def format_enum_data_tag(ns: str, enum_cls: type, variant):
    return format_data_tag(ns, enum_cls.__name__, variant.name, variant.value)


def format_data_tag(ns: str, id: str, key, value):
    return ["tv", [ns, id, key, value]]


def add_enum_utility_methods(Class, ns):
    def to_data_tag(self):
        return format_data_tag(ns, Class.__name__, self.name, self.value)

    setattr(Class, "to_data_tag", to_data_tag)


def make_find_best_match_from_search(search_fn):
    async def find_best_match(query: str = ""):
        rows = await maybe_await(search_fn(query))
        if rows and len(rows) > 0:
            return rows[0]
        else:
            return None

    return find_best_match


class FixedTagValue(TagValue):
    def __init__(self, id, name, docs, variants, EnumClass):
        super().__init__(id, name, docs)
        self.EnumClass = EnumClass
        self.variants = variants
        self.variants_by_key = {v.name: v for v in variants}

    def from_key_and_label(self, key, label):
        v = self.variants_by_key.get(key)
        if v:
            return v.enum_value

        return

    @property
    def match_handler_id(self):
        return f"enum::{self.id}::match"

    def to_info(self, _toolbox):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.docs,
            "icon": self.icon,
            "entries": [(v.name, v.value) for v in self.variants],
            "matchHandlerId": self.match_handler_id,
        }

    def get_handlers(self):
        return [
            (self.match_handler_id, self.match_handler),
        ]

    async def get_variants(self):
        return self.variants


class DynTagValue(TagValue):
    def __init__(self, id, name, docs, EnumClass, load_fn, cache=True):
        super().__init__(id, name, docs)
        self.EnumClass = EnumClass
        self.load_fn = load_fn
        self.cache = cache
        self._cached_variants = None

    def from_key_and_label(self, key, label):
        return self.EnumClass(key, label)

    @property
    def match_handler_id(self):
        return f"enum::{self.id}::match"

    @property
    def load_handler_id(self):
        return f"enum::{self.id}::load_entries"

    async def get_variants(self):
        if self._cached_variants:
            return self._cached_variants

        variants = await maybe_await(await self.load_fn())

        if self.cache:
            self._cached_variants = variants

        return variants

    def get_handlers(self):
        return [
            (self.match_handler_id, self.match_handler),
            (self.load_handler_id, self.load_handler),
        ]

    def to_info(self, _toolbox):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.docs,
            "icon": self.icon,
            "matchHandlerId": self.match_handler_id,
            "loadEntriesHandlerId": self.load_handler_id,
        }


class DynSearchTagValue(TagValue):
    def __init__(self, id, name, docs, EnumClass, search_fn, find_best_match_fn):
        super().__init__(id, name, docs)
        self.EnumClass = EnumClass
        self.search_fn = search_fn
        self.find_best_match_fn = find_best_match_fn

    def from_key_and_label(self, key, label):
        return self.EnumClass(key, label)

    @property
    def match_handler_id(self):
        return f"enum::{self.id}::match"

    @property
    def search_handler_id(self):
        return f"enum::{self.id}::search"

    async def get_variants(self):
        logger.warning("calling get_variants in DynSearchTagValue")
        return []

    async def load_handler(self, info):
        return await maybe_await(self.search_fn(info))

    async def find_best_match(self, query):
        r = await maybe_await(self.find_best_match_fn({"query": query}))
        if is_list(r):
            if len(r) > 0:
                return r[0]
            else:
                return None
        else:
            return r

    def get_handlers(self):
        return [
            (self.match_handler_id, self.match_handler),
            (self.search_handler_id, self.load_handler),
        ]

    def to_info(self, _toolbox):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.docs,
            "icon": self.icon,
            "matchHandlerId": self.match_handler_id,
            "searchHandlerId": self.search_handler_id,
        }


class Variant:
    def __init__(self, name, value, enum_value, docs=None):
        self.name = name
        self.value = value
        self.enum_value = enum_value
        self.docs = docs

    def __str__(self):
        return f"Variant({self.name}, {self.value}, {self.docs})"

    def __iter__(self):
        yield self.name
        yield self.value

    @classmethod
    def from_enum_variant(cls, variant):
        if isinstance(variant, KeyValue):
            name = variant.key
        else:
            name = variant.name

        value = variant.value
        docs = None

        return cls(name, value, variant, docs)


class EmptyState:
    "State class used when no state is provided"

    def setup(self):
        "method called to setup the state before start serving"
        pass


class Toolbox:
    def __init__(self, id, name, docs, state=None):
        self.id = id
        self.name = name
        self.docs = docs

        self.tools = []
        self.tools_by_fn = {}
        self.tasks = []
        self.resource_handlers = {}
        self.context_actions_by_type_and_tool = {}
        self._raw_task_to_task = {}
        self.enums = []
        self.enum_class_to_wrapper = {}

        self.handlers = {}

        self.state = state if state is not None else EmptyState()
        self.State = self.state.__class__

    def __str__(self):
        if self.tools:
            tools = "\n\n" + "\n\n".join([str(tool) for tool in self.tools])
        else:
            tools = ""

        return f"Toolbox({self.id}, {self.name}, {self.docs}){tools}"

    def get_context_action_for_tool_enum_arg(self, tool, arg, generate_if_missing=True):
        tv = self.enum_class_to_wrapper.get(arg.type)

        if tv:
            cah = self.context_actions_by_type_and_tool.get(arg.type, {}).get(tool)
            if cah is None:
                if generate_if_missing:
                    cah = self.generate_context_action_for_tool_enum_arg(tool, arg)
                else:
                    return

            return {"target": {"name": tv.id}, "handler": cah.handler_id}
        else:
            logger.warning(
                "tool arg type not registered, forgot decorator? tool: %s, arg: %s",
                tool,
                arg,
            )

    def generate_context_action_for_tool_enum_arg(self, tool, arg):
        def generated_context_action_handler():
            return {"name": tool.handler_id, "args": {}}

        overrides = {
            "name": f"GenContextActionForToolAndArg-{tool.handler_id}-{arg.name}"
        }
        return self.add_context_action_handler_for_fn_tool_and_type(
            generated_context_action_handler, tool, arg.type, overrides
        )

    def provide_arg(self, arg, info):
        t = arg.type
        if t is self.State:
            return self.state
        elif t is Request:
            # only for resource handlers
            return _provide_arg_of_type(info, "request", Request)
        elif t is ResourceInfo:
            # only for resource handlers
            return _provide_arg_of_type(info, "resource", ResourceInfo)
        elif t is ContextActionInfo:
            # only for context_action handlers
            return _provide_arg_of_type(info, "info", ContextActionInfo)
        else:
            v = info.get(arg.name)
            if is_any_enum(t):
                wrapper = self.enum_class_to_wrapper.get(t)
                if wrapper:
                    # NOTE: This call is async and returns an awaitable
                    # can't always provide default if None because it must be awaited
                    r = wrapper.from_raw_arg_value(v)
                    return r if r is not None else arg.default_value
                else:
                    logger.warning("enum class argument type not annotated? %s", arg)
                    return arg.default_value
            else:
                return arg.cast_json_value_or_default(v)

    async def setup(self):
        if hasattr(self.state, "setup"):
            if inspect.iscoroutinefunction(self.state.setup):
                await self.state.setup()
            else:
                self.state.setup()

    async def dispose(self):
        if hasattr(self.state, "dispose"):
            if inspect.iscoroutinefunction(self.state.dispose):
                await self.state.dispose()
            else:
                self.state.dispose()

    def handler_id_for_task(self, fn):
        task = self._raw_task_to_task.get(fn)
        if task:
            return task.handler_id
        else:
            raise ValueError("Handler id not found for Task")

    def add_handler(self, id, handler):
        if id in self.handlers:
            logger.warning("duplicated handler for id '%s'", id)

        self.handlers[id] = handler

    def add_enum(self, v):
        for id, handler in v.get_handlers():
            self.add_handler(id, handler)

        self.enum_class_to_wrapper[v.EnumClass] = v
        self.enums.append(v)

    def add_tool(self, tool):
        def handler(info):
            return tool.call_with_args(self, info)

        self.add_handler(tool.handler_id, handler)
        self.tools.append(tool)
        self.tools_by_fn[tool.fn] = tool

    def add_task(self, v):
        def handler(info):
            return v.call_with_args(self, info)

        self.add_handler(v.handler_id, handler)
        self._raw_task_to_task[v.fn] = v

        self.tasks.append(v)

    def add_resource_handler_for_type(self, v, for_type):
        if for_type in self.resource_handlers:
            logger.warning("overriding resource handler for type: %s", for_type)

        self.resource_handlers[for_type] = v

    def add_context_action_handler_for_fn_tool_and_type(
        self, fn, tool, type, overrides
    ):
        cah = ContextActionHandler.from_function(fn)
        cah.apply_overrides(overrides)
        self.add_context_action_handler_for_tool_and_type(cah, tool, type)
        return cah

    def add_context_action_handler_for_tool_and_type(self, cah, tool, type):
        by_type = self.context_actions_by_type_and_tool.get(type)
        if by_type is None:
            by_type = {}
            self.context_actions_by_type_and_tool[type] = by_type

        if tool in by_type:
            logger.warning(
                "overriding context action handler for tool %s and type %s", tool, type
            )

        def handler(raw_info):
            ca_info = ContextActionInfo.from_raw_info(raw_info)
            return cah.call_with_args(self, {"info": ca_info})

        self.add_handler(cah.handler_id, handler)
        by_type[tool] = cah

    def enum(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            arg = args[0]
            if is_enum(arg):
                self.add_enum(TagValue.from_enum_class(arg, {}))
            elif is_dyn_enum(arg):
                self.add_enum(TagValue.from_dyn_enum_class(arg, {}, self))
            else:
                raise TypeError(
                    "The decorated class must inherit from enum.Enum or DynEnum"
                )

            add_enum_utility_methods(arg, self.id)

            return arg
        else:

            def wrapper(arg):
                if is_enum(arg):
                    self.add_enum(TagValue.from_enum_class(arg, kwargs))
                elif is_dyn_enum(arg):
                    self.add_enum(TagValue.from_dyn_enum_class(arg, kwargs, self))
                else:
                    raise TypeError(
                        "The decorated class must inherit from enum.Enum or DynEnum"
                    )

                add_enum_utility_methods(arg, self.id)

                return arg

            return wrapper

    def task(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            func = args[0]
            t = Task.from_function(func)
            self.add_task(t)
            return func
        else:

            def wrapper(func):
                t = Task.from_function(func)
                t.apply_overrides(kwargs)
                self.add_task(t)
                return func

            return wrapper

    def tool(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            func = args[0]
            t = Tool.from_function(func)
            self.add_tool(t)
            return func
        else:

            def wrapper(func):
                t = Tool.from_function(func)
                t.apply_overrides(kwargs)
                self.add_tool(t)
                return func

            return wrapper

    def resource(self, for_type):
        def wrapper(fn):
            t = ResourceHandler.from_function_and_type(fn, for_type)
            self.add_resource_handler_for_type(t, for_type)
            return fn

        return wrapper

    def context_action(self, tool, target, **kwargs):
        # here tool is the raw fn since it's provided by the developer we need to get te real one
        actual_tool = self.tools_by_fn.get(tool)

        if actual_tool is None:
            raise ValueError(
                "context_action for tool that is not registered, forgot decorator or defined after?"
            )

        def wrapper(fn):
            self.add_context_action_handler_for_fn_tool_and_type(
                fn, actual_tool, target, kwargs
            )
            return fn

        return wrapper

    def build_tool_info(self):
        return {
            "ns": self.id,
            "title": self.name,
            "description": self.docs,
            "tools": {tool.id: tool.to_info(self) for tool in self.tools},
            "tagValues": {
                tag_value.id: tag_value.to_info(self) for tag_value in self.enums
            },
            "handlers": [task.handler_id for task in self.tasks],
        }

    def handle_request(self, body):
        if not is_dict(body):
            return res_error("BadRequestBody", "Bad Request Body")

        action = body.get("action", None)
        if action == "info":
            return self.handle_action_info()
        elif action == "request":
            op_name = body.get("opName", None)
            req_info = body.get("info", {})
            return self.handle_action_request(op_name, req_info)
        else:
            return res_error("UnknownAction", "Unknown Action", {"action": action})

    def handle_action_info(self):
        return self.build_tool_info()

    def handle_action_request(self, op_name, req_info):
        handler = self.handlers.get(op_name)
        if handler:
            logger.info("handle action request: %s %s", op_name, req_info)
            return handler(req_info)
        else:
            return res_error("ToolNotFound", "Tool Not Found", {"opName": op_name})

    def handle_resource_request(self, request, res_type, res_id):
        resource_handler = self.resource_handlers.get(res_type)
        if resource_handler:
            resource = ResourceInfo(res_type, res_id)
            return resource_handler.call_with_args(
                self, {"request": request, "resource": resource}
            )
        else:
            return Response(status_code=404, content="Resource not found")

    def to_fastapi_app(self):
        tb = self

        @contextlib.asynccontextmanager
        async def lifespan(app: FastAPI):
            await tb.setup()
            yield
            await tb.dispose()

        app = FastAPI(lifespan=lifespan)

        @app.post("/")
        async def root_gd_handler(request: Request):
            body = await request.json()
            res = await maybe_await(tb.handle_request(body))
            return handler_response_to_fastapi_response(
                res, jsonable_encoder, JSONResponse
            )

        @app.get("/resource/{res_type}/{res_id}")
        async def resource_handler(request: Request, res_type: str, res_id: str):
            res = tb.handle_resource_request(request, res_type, res_id)
            if res is None:
                return Response(status_code=404, content="Resource not found")
            else:
                return await maybe_await(res)

        return app

    def serve(self, host="127.0.0.1", port=8086):
        app = self.to_fastapi_app()

        return uvicorn.run(app, host=host, port=port)


def _provide_arg_of_type(info, key, Class):
    v = info.get(key)
    if isinstance(v, Class):
        return v
    elif v is not None:
        logger.warning(
            "requested %s arg but got another type %s, %s",
            Class,
            v,
            info,
        )
    return None


def res_error(code, reason, info=None):
    return {"ok": False, "code": code, "reason": reason, "info": info}


async def maybe_await(v):
    r = v
    while inspect.isawaitable(r):
        r = await r
    return r


## resource utils


def send_bytes_range_requests(
    file_obj: BinaryIO, start: int, end: int, chunk_size: int = 10_000
):
    with file_obj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)


def get_mime_type(file_path):
    mime_type, encoding = mimetypes.guess_type(file_path)

    if mime_type is None:
        mime_type = "application/octet-stream"

    return mime_type


# fastapi utils


def serve_static_file(file_path, request):
    try:
        file_size = os.path.getsize(file_path)
    except FileNotFoundError:
        return Response(status_code=404, content="File not found")

    range_info = request.headers.get("Range")

    if range_info:
        # Example range header: bytes=0-100
        range_val = range_info.split("=")[-1]
        start_str, end_str = range_val.split("-")

        # Parse start and end bytes
        start = int(start_str) if start_str else 0
        end = int(end_str) if end_str else file_size - 1

        # Ensure range values are valid
        if start >= file_size or end >= file_size or start > end:
            return Response(
                status_code=416, headers={"Content-Range": f"bytes */{file_size}"}
            )

        content_length = end - start + 1
        content_range = f"bytes {start}-{end}/{file_size}"
        content_type = get_mime_type(file_path)
        headers = {
            "Content-Type": content_type,
            "Content-Length": str(content_length),
            "Content-Range": content_range,
            "Accept-Ranges": "bytes",
        }

        return StreamingResponse(
            send_bytes_range_requests(open(file_path, mode="rb"), start, end),
            status_code=206,
            headers=headers,
        )

    # Serve the entire file if no range is specified
    return FileResponse(file_path, headers={"Accept-Ranges": "bytes"})


def handler_response_to_fastapi_response(res, jsonable_encoder, JSONResponse):
    try:
        return JSONResponse(content=jsonable_encoder(res), status_code=200)
    except Exception as err:
        logger.warning("Error encoding response: %s (%s)", err, res)
        err_res = res_error("InternalError", "Internal Error", {})
        return JSONResponse(content=jsonable_encoder(err_res), status_code=500)
