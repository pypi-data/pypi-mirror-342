import asyncio
from enum import Enum
from glootil import (
    Toolbox,
    ContextActionInfo,
    ResourceInfo,
    DynEnum,
    DynTagValue,
    FixedTagValue,
    FnArg,
    NoneType,
    KeyValueEnum,
    Variant,
    format_enum_data_tag,
    format_data_tag,
    make_enum_dict,
    search_result_to_response,
    match_result_to_response,
    has_class_method,
    has_static_method,
    maybe_await,
    try_cast_or,
    type_to_schema_type,
    basic_match_raw_tag_value,
    apply_arg_override,
    cast_json_type_to_fn_arg_type_or_default as cast_json,
    handler_response_to_fastapi_response,
)
from datetime import date
from fastapi import Request

import pytest

all_months = [
    ("01", "January"),
    ("02", "February"),
    ("03", "March"),
    ("04", "April"),
    ("05", "May"),
    ("06", "June"),
    ("07", "July"),
    ("08", "August"),
    ("09", "September"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December"),
]


def test_toolbox_constructor():
    t = Toolbox("math", "Math tools", "do operations on numbers")
    assert t.id == "math"
    assert t.name == "Math tools"
    assert t.docs == "do operations on numbers"


def test_tool_no_call_no_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def f():
        return None

    t = tb.tools[0]

    assert t.name == "f"
    assert t.docs is None
    assert len(t.args) == 0


def test_tool_no_call_no_annotations():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def add(a, b):
        return a + b

    t = tb.tools[0]

    assert t.name == "add"
    assert t.docs is None
    assert len(t.args) == 2

    a, b = t.args

    assert a.name == "a"
    assert a.index == 0
    assert a.type is None
    assert a.default_value is None

    assert b.name == "b"
    assert b.index == 1
    assert b.type is None
    assert b.default_value is None

    assert t.return_type is None


def test_tool_no_call():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def add(a: int, b: int = 0) -> int:
        "add two numbers together"
        return a + b

    t = tb.tools[0]

    assert t.name == "add"
    assert t.docs == "add two numbers together"
    assert len(t.args) == 2

    a, b = t.args

    assert a.name == "a"
    assert a.index == 0
    assert a.type is int
    assert a.default_value is None

    assert b.name == "b"
    assert b.index == 1
    assert b.type is int
    assert b.default_value == 0

    assert t.return_type is int


def test_tool_call_override_name_and_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool(
        name="substract",
        docs="my docs",
        args={"a": {"name": "Left", "docs": "Left operand"}, "b": "Right"},
    )
    def sub(a: int, b):
        return a - b

    t = tb.tools[0]

    assert t.name == "substract"
    assert t.docs == "my docs"
    assert len(t.args) == 2

    a, b = t.args

    assert a.label == "Left"
    assert a.docs == "Left operand"
    assert b.label == "Right"
    assert b.docs is None

    assert a.to_schema_info() == {
        "description": "Left operand",
        "type": "integer",
        "default": 0,
    }


def test_enum_class():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, FixedTagValue)
    assert e.name == "Operation"
    assert e.docs == "the operation to apply"
    assert len(e.variants) == 4

    add, sub, mul, div = e.variants

    assert add.name == "ADD"
    assert add.value == "add"

    assert sub.name == "SUB"
    assert sub.value == "sub"

    assert mul.name == "MUL"
    assert mul.value == "mul"

    assert div.name == "DIV"
    assert div.value == "div"

    assert e.to_info(tb) == {
        "id": e.id,
        "name": e.name,
        "description": e.docs,
        "icon": e.icon,
        "entries": [(v.name, v.value) for v in e.variants],
        "matchHandlerId": f"enum::{e.id}::match",
    }


def test_empty_build_tool_info():
    tb = Toolbox("mytools", "My Tools", "some tools")

    assert tb.build_tool_info() == {
        "ns": "mytools",
        "title": "My Tools",
        "description": "some tools",
        "tools": {},
        "tagValues": {},
        "handlers": [],
    }


def test_type_to_schema_type_int():
    assert type_to_schema_type(int, None) == ("integer", 0, None)
    assert type_to_schema_type(int, 42) == ("integer", 42, None)


def test_type_to_schema_type_float():
    assert type_to_schema_type(float, None) == ("number", 0.0, None)
    assert type_to_schema_type(float, 3.14) == ("number", 3.14, None)


def test_type_to_schema_type_str():
    assert type_to_schema_type(str, None) == ("string", "", None)
    assert type_to_schema_type(str, "hello") == ("string", "hello", None)


def test_type_to_schema_type_bool():
    assert type_to_schema_type(bool, None) == ("boolean", False, None)
    assert type_to_schema_type(bool, True) == ("boolean", True, None)


def test_type_to_schema_type_fallthrough():
    assert type_to_schema_type(list, None) == ("string", "", None)


def test_tool_all_types():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def all_types(
        a: int,
        b: float,
        c: bool,
        d: date,
        s: str,
        e: int = 10,
        f: float = 1.5,
        g: bool = True,
        h: str = "hi",
    ):
        pass

    t = tb.tools[0]

    expected = {
        "title": t.name,
        "description": t.docs,
        "schema": {
            "fields": {
                "a": {"type": "integer", "default": 0, "description": None},
                "b": {"type": "number", "default": 0.0, "description": None},
                "c": {"type": "boolean", "default": False, "description": None},
                "d": {
                    "type": "string",
                    "default": None,
                    "description": None,
                    "format": "date",
                },
                "s": {"type": "string", "default": "", "description": None},
                "e": {"type": "integer", "default": 10, "description": None},
                "f": {"type": "number", "default": 1.5, "description": None},
                "g": {"type": "boolean", "default": True, "description": None},
                "h": {"type": "string", "default": "hi", "description": None},
            }
        },
        "ui": {
            "prefix": t.name,
            "args": {
                "a": {"prefix": "a"},
                "b": {"prefix": "b"},
                "c": {"prefix": "c"},
                "d": {"prefix": "d"},
                "s": {"prefix": "s"},
                "e": {"prefix": "e"},
                "f": {"prefix": "f"},
                "g": {"prefix": "g"},
                "h": {"prefix": "h"},
            },
            "manualUpdate": False,
        },
        "contextActions": [],
        "examples": [t.name],
    }

    assert t.to_info(tb) == expected


def test_toolbox_info():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool(examples=["Show all types"], manual_update=True)
    def all_types(
        a: int,
        b: float,
        c: bool,
        d: str,
        e: int = 10,
        f: float = 1.5,
        g: bool = True,
        h: str = "hi",
    ):
        pass

    t = tb.tools[0]

    @tb.enum(id="CountryEnum", icon="flag")
    class Country(DynEnum):
        "A Country"

        @staticmethod
        def load():
            return [("ARG", "Argentina"), ("URU", "Uruguay")]

    e = tb.enums[0]

    assert tb.build_tool_info() == {
        "ns": "mytools",
        "title": "My Tools",
        "description": "some tools",
        "tools": {
            "all_types": {
                "title": t.name,
                "description": t.docs,
                "schema": {
                    "fields": {
                        "a": {"type": "integer", "default": 0, "description": None},
                        "b": {"type": "number", "default": 0.0, "description": None},
                        "c": {"type": "boolean", "default": False, "description": None},
                        "d": {"type": "string", "default": "", "description": None},
                        "e": {"type": "integer", "default": 10, "description": None},
                        "f": {"type": "number", "default": 1.5, "description": None},
                        "g": {"type": "boolean", "default": True, "description": None},
                        "h": {"type": "string", "default": "hi", "description": None},
                    }
                },
                "ui": {
                    "prefix": t.name,
                    "args": {
                        "a": {"prefix": "a"},
                        "b": {"prefix": "b"},
                        "c": {"prefix": "c"},
                        "d": {"prefix": "d"},
                        "e": {"prefix": "e"},
                        "f": {"prefix": "f"},
                        "g": {"prefix": "g"},
                        "h": {"prefix": "h"},
                    },
                    "manualUpdate": True,
                },
                "contextActions": [],
                "examples": ["Show all types"],
            }
        },
        "tagValues": {
            "CountryEnum": {
                "id": e.id,
                "name": e.name,
                "description": e.docs,
                "icon": e.icon,
                "matchHandlerId": "enum::CountryEnum::match",
                "loadEntriesHandlerId": "enum::CountryEnum::load_entries",
            }
        },
        "handlers": [],
    }


def test_basic_matcher_empty_pos():
    assert basic_match_raw_tag_value("", []) == (-1, None)


def test_basic_matcher_non_empty_pos_list():
    assert basic_match_raw_tag_value("a", [("b", "c")]) == (0, ("b", "c"))


def gen_one_posibility():
    yield ("b", "c")


def test_basic_matcher_non_empty_pos_gen():
    assert basic_match_raw_tag_value("a", gen_one_posibility()) == (0, ("b", "c"))


def gen_two_posibilities():
    yield ("b", "c")
    yield ("a", "a")


def test_basic_matcher_non_empty_pos_gen_2():
    assert basic_match_raw_tag_value("a", gen_two_posibilities()) == (1, ("a", "a"))


@pytest.mark.asyncio
async def test_enum_class_default_matcher():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    e = tb.enums[0]

    assert await e.find_best_match("ad") == ("ADD", "add")
    assert await e.find_best_match("mu") == ("MUL", "mul")


@pytest.mark.asyncio
async def test_enum_class_custom_matcher():
    def matcher_always_first(_word, possibilities):
        return 0, next(iter(possibilities))

    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum(matcher=matcher_always_first)
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    e = tb.enums[0]

    assert e.closest_matcher == matcher_always_first
    assert await e.find_best_match("") == ("ADD", "add")
    assert await e.find_best_match("mul") == ("ADD", "add")


@pytest.mark.asyncio
async def test_tb_setup_with_sync_state_setup():
    class State:
        def __init__(self):
            self.v = None

        def setup(self):
            self.v = 42

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())
    await tb.setup()
    assert tb.state.v == 42


@pytest.mark.asyncio
async def test_tb_setup_with_async_state_setup():
    class State:
        def __init__(self):
            self.v = None

        async def setup(self):
            await asyncio.sleep(0.010)
            self.v = 42

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())
    await tb.setup()
    assert tb.state.v == 42


@pytest.mark.asyncio
async def test_tb_setup_with_no_state_setup():
    class State:
        def __init__(self):
            self.v = None

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())
    await tb.setup()
    assert tb.state.v is None


@pytest.mark.asyncio
async def test_enum_class_match_handler():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    e = tb.enums[0]

    assert tb.handlers[e.match_handler_id] == e.match_handler
    match_result = await e.match_handler(dict(query="ad"))
    assert match_result == ("ADD", "add")


def test_provide_arg_int():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, int, 0)
    assert tb.provide_arg(arg, {}) == 0
    assert tb.provide_arg(arg, {"a": 5}) == 5
    assert tb.provide_arg(arg, {"a": 5.5}) == 5


def test_provide_arg_float():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, float, 0)
    assert tb.provide_arg(arg, {}) == 0
    assert tb.provide_arg(arg, {"a": 5}) == 5
    assert tb.provide_arg(arg, {"a": 5.5}) == 5.5
    assert tb.provide_arg(arg, {"a": False}) == 0


def test_provide_arg_bool():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, bool, False)
    assert tb.provide_arg(arg, {}) is False
    assert tb.provide_arg(arg, {"a": True}) is True
    assert tb.provide_arg(arg, {"a": 1}) is True
    assert tb.provide_arg(arg, {"a": 0}) is False


def test_provide_arg_str():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, str, "hi")
    assert tb.provide_arg(arg, {}) == "hi"
    assert tb.provide_arg(arg, {"a": "hello"}) == "hello"
    assert tb.provide_arg(arg, {"a": ""}) == ""
    assert tb.provide_arg(arg, {"a": 0}) == "0"


def m_enum_dict(key, label, ns, id):
    return {"type": "enum", "key": key, "label": label, "ns": ns, "id": id}


@pytest.mark.asyncio
async def test_provide_arg_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Color(Enum):
        RED = "Red"
        GREEN = "Green"
        BLUE = "Blue"

    arg = FnArg("a", 0, Color, Color.RED)
    # it is None because the returned value is an awaitable that returns None
    # the default is provided in call_with_args
    assert await maybe_await(tb.provide_arg(arg, {})) is None
    assert (
        await maybe_await(
            tb.provide_arg(arg, {"a": m_enum_dict("BLUE", "Blue", tb.id, "Color")})
        )
        == Color.BLUE
    )
    assert await maybe_await(tb.provide_arg(arg, {"a": "BLUE"})) == Color.BLUE
    assert await maybe_await(tb.provide_arg(arg, {"a": "Blue"})) == Color.BLUE
    assert await maybe_await(tb.provide_arg(arg, {"a": "Bl"})) == Color.BLUE
    assert await maybe_await(tb.provide_arg(arg, {"a": "G"})) == Color.GREEN


@pytest.mark.asyncio
async def test_provide_arg_dyn_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Color(DynEnum):
        @staticmethod
        def load():
            return [
                ("RED", "Red"),
                ("GREEN", "Green"),
                ("BLUE", "Blue"),
            ]

    RED = Color("RED", "Red")
    GREEN = Color("GREEN", "Green")
    BLUE = Color("BLUE", "Blue")

    arg = FnArg("a", 0, Color, RED)
    # it is None because the returned value is an awaitable that returns None
    # the default is provided in call_with_args
    assert await maybe_await(tb.provide_arg(arg, {})) is None
    assert (
        await maybe_await(
            tb.provide_arg(arg, {"a": m_enum_dict("BLUE", "Blue", tb.id, "Color")})
        )
        == BLUE
    )
    assert await maybe_await(tb.provide_arg(arg, {"a": "BLUE"})) == BLUE
    assert await maybe_await(tb.provide_arg(arg, {"a": "Blue"})) == BLUE
    assert await maybe_await(tb.provide_arg(arg, {"a": "Bl"})) == BLUE
    assert await maybe_await(tb.provide_arg(arg, {"a": "G"})) == GREEN


def test_provide_arg_optional_str():
    tb = Toolbox("mytools", "My Tools", "some tools")
    arg = FnArg("a", 0, str | None, None)
    assert tb.provide_arg(arg, {}) is None
    assert tb.provide_arg(arg, {"a": "hello"}) == "hello"
    assert tb.provide_arg(arg, {"a": ""}) == ""
    assert tb.provide_arg(arg, {"a": 0}) == "0"


def test_provide_arg_optional_str_in_tool():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def f(a: str | None = "hi"):
        return a

    @tb.tool
    def g(a: None | str):
        return a

    t = tb.tools[0]
    arg = t.args[0]
    assert arg.type is str
    assert arg._isinstance_type == (str, type(None))

    t = tb.tools[1]
    arg = t.args[0]
    assert arg.type is str
    assert arg._isinstance_type == (type(None), str)


def test_dyn_enum_decoration_no_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Country(DynEnum):
        "A Country"

        @staticmethod
        def load():
            return [("ARG", "Argentina"), ("URU", "Uruguay")]

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, DynTagValue)
    assert e.id == "Country"
    assert e.name == "Country"
    assert e.docs == "A Country"
    assert e.icon == "list"

    assert e.to_info(tb) == {
        "id": e.id,
        "name": e.name,
        "description": e.docs,
        "icon": e.icon,
        "matchHandlerId": "enum::Country::match",
        "loadEntriesHandlerId": "enum::Country::load_entries",
    }


def test_dyn_enum_decoration_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum(id="CountryEnum", icon="flag")
    class Country(DynEnum):
        "A Country"

        @staticmethod
        def load():
            return [("ARG", "Argentina"), ("URU", "Uruguay")]

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, DynTagValue)
    assert e.id == "CountryEnum"
    assert e.name == "Country"
    assert e.docs == "A Country"
    assert e.icon == "flag"

    assert e.to_info(tb) == {
        "id": e.id,
        "name": e.name,
        "description": e.docs,
        "icon": e.icon,
        "matchHandlerId": "enum::CountryEnum::match",
        "loadEntriesHandlerId": "enum::CountryEnum::load_entries",
    }


@pytest.mark.asyncio
async def test_fn_enum_default_matcher():
    def matcher_always_first(_word, possibilities):
        return 0, next(iter(possibilities))

    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Month(DynEnum):
        @staticmethod
        def load():
            return all_months

    e = tb.enums[0]

    assert await e.find_best_match("1") == ("01", "January")
    assert await e.find_best_match("2") == ("02", "February")
    assert await e.find_best_match("may") == ("05", "May")


@pytest.mark.asyncio
async def test_fn_enum_custom_matcher():
    def matcher_always_first(_word, possibilities):
        return 0, next(iter(possibilities))

    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum(matcher=matcher_always_first)
    class Month(DynEnum):
        @staticmethod
        def load():
            return all_months

    e = tb.enums[0]

    assert e.closest_matcher == matcher_always_first
    assert await e.find_best_match("") == ("01", "January")
    assert await e.find_best_match("02") == ("01", "January")
    assert await e.find_best_match("May") == ("01", "January")


@pytest.mark.asyncio
async def test_dyn_enum_arg_provider_provides_state():
    class State:
        def get_variants(self):
            return all_months

    tb = Toolbox("mytools", "My Tools", "some tools", state=State())

    @tb.enum
    class Month(DynEnum):
        @staticmethod
        def load(name="Months", state: State | None = None):
            return state.get_variants() if state else []

    e = tb.enums[0]
    en = await e.get_variants()

    assert len(en) == len(all_months)
    assert en == all_months


@pytest.mark.asyncio
async def test_async_dyn_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Month(DynEnum):
        "my enum description"

        @staticmethod
        async def load():
            await asyncio.sleep(0.010)
            return all_months

    assert len(tb.enums) == 1

    e = tb.enums[0]

    assert isinstance(e, DynTagValue)
    assert e.name == "Month"
    assert e.docs == "my enum description"
    assert e.icon == "list"
    en = await e.get_variants()
    assert len(en) == len(all_months)
    assert en == all_months


@pytest.mark.asyncio
async def test_dyn_enum_match_handler():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(DynEnum):
        @staticmethod
        def load():
            return [
                ("ADD", "add"),
                ("SUB", "sub"),
                ("MUL", "mul"),
                ("DIV", "div"),
            ]

    e = tb.enums[0]

    assert tb.handlers[e.match_handler_id] == e.match_handler
    match_result = await e.match_handler(dict(query="ad"))
    assert match_result == ("ADD", "add")


def test_cast_json_from_int():
    assert cast_json(10, int, 0) == 10
    assert cast_json(10, float, 0.0) == 10.0
    assert cast_json(10, bool, False) is True
    assert cast_json(0, bool, True) is False
    assert cast_json(5, str, "") == "5"
    assert cast_json(5, date, None) is None


def test_cast_json_from_float():
    assert cast_json(10.5, float, 0) == 10.5
    assert cast_json(10.5, int, 0) == 10
    assert cast_json(10.5, bool, False) is True
    assert cast_json(0.0, bool, True) is False
    assert cast_json(5.5, str, "") == "5.5"
    assert cast_json(5, date, None) is None


def test_cast_json_from_bool():
    assert cast_json(True, bool, None) is True
    assert cast_json(False, bool, None) is False
    assert cast_json(True, int, 0) == 1
    assert cast_json(False, int, 1) == 0
    assert cast_json(True, float, 0) == 1.0
    assert cast_json(False, float, 1) == 0.0
    assert cast_json(True, str, "") == "True"
    assert cast_json(False, str, "") == "False"
    assert cast_json(True, date, None) is None


def test_cast_json_from_none():
    assert cast_json(None, NoneType, 10) is None
    assert cast_json(None, int, 10) == 10
    assert cast_json(None, float, 5.0) == 5.0
    assert cast_json(None, bool, True) is True
    assert cast_json(None, str, "nope") == "nope"
    assert cast_json(None, date, None) is None


def test_cast_json_from_str():
    assert cast_json("10.5", float, 0.0) == 10.5
    assert cast_json("10", int, 0) == 10
    assert cast_json("", bool, True) is False
    assert cast_json("whatev", bool, False) is True
    assert cast_json("hi", str, "") == "hi"
    assert cast_json("2025-03-25", date, None) == date(2025, 3, 25)


def test_try_cast_or_raise(caplog):
    r = try_cast_or("a", int, 42)
    assert r == 42
    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"


def test_cast_json_log(caplog):
    assert cast_json({}, int, None) is None
    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"
    assert (
        log.message
        == "no caster found from <class 'dict'> to <class 'int'>, returning default"
    )


def test_type_to_schema_type_log(caplog):
    t, d, f = type_to_schema_type(dict, None)
    assert t == "string"
    assert d == ""
    assert f is None
    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"
    assert log.message == "unknown type for schema <class 'dict'>, returning string"


def test_apply_arg_override_not_found_log(caplog):
    apply_arg_override({}, "foo", {})
    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"
    assert log.message == "tool argument info for inexistent argument name 'foo'"


def test_apply_arg_override_bad_info_type_log(caplog):
    apply_arg_override({"foo": {"what": "dummy arg"}}, "foo", True)
    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"
    assert log.message == "bad tool argument info format for argument 'foo': True"


def test_provide_arg_not_annotated_log(caplog):
    tb = Toolbox("mytools", "My Tools", "some tools")

    class MyEnum(Enum):
        A = "a"
        B = "b"

    @tb.tool
    def f(a: MyEnum = MyEnum.A):
        return ""

    arg = tb.tools[0].args[0]
    r = tb.provide_arg(arg, {})
    assert r == MyEnum.A

    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"
    assert log.message == "enum class argument type not annotated? " + str(arg)


def test_add_enums_same_id_log(caplog):
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    @tb.enum
    class MyEnum(Enum):
        A = "a"
        B = "b"

    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"
    assert log.message == "duplicated handler for id 'enum::MyEnum::match'"


def test_add_tools_same_id_log(caplog):
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    @tb.tool
    def f():
        pass

    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"
    assert log.message == "duplicated handler for id 'f'"


def test_response_log(caplog):
    class JSONResponse:
        def __init__(self, content=None, status_code=200):
            self.content = content
            self.status_code = status_code

    def jsonable_encoder(v):
        if v is None:
            raise ValueError("Don't return null")
        return v

    handler_response_to_fastapi_response(None, jsonable_encoder, JSONResponse)

    assert len(caplog.records) == 1
    log = caplog.records[0]
    assert log.levelname == "WARNING"


def test_gen_context_action_for_tool_enum_arg():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    @tb.tool
    def my_tool(a: int, s: str = "hi", e: Op = Op.ADD):
        pass

    t = tb.tools[0]

    assert len(tb.context_actions_by_type_and_tool) == 0
    cas = t.to_context_actions(tb)
    assert len(cas) == 1
    assert len(tb.context_actions_by_type_and_tool) == 1
    assert len(tb.context_actions_by_type_and_tool[Op]) == 1
    assert tb.context_actions_by_type_and_tool[Op][t]
    ca = cas[0]
    assert ca == {
        "target": {"name": "Op"},
        "handler": "ContextActionHandler::GenContextActionForToolAndArg-my_tool-e",
    }

    assert t.to_info(tb).get("contextActions") == cas


def test_custom_context_action_for_tool_enum_arg():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(Enum):
        ADD = "add"
        SUB = "sub"

    @tb.tool
    def my_tool(a: int, s: str = "hi", e: Op = Op.ADD):
        pass

    @tb.context_action(tool=my_tool, target=Op)
    def my_context_action():
        return {"name": None, "args": {}}

    t = tb.tools[0]

    assert len(tb.context_actions_by_type_and_tool) == 1
    assert len(tb.context_actions_by_type_and_tool[Op]) == 1
    assert tb.context_actions_by_type_and_tool[Op][t]
    cas = t.to_context_actions(tb)
    assert len(cas) == 1
    ca = cas[0]
    assert ca == {
        "target": {"name": "Op"},
        "handler": "ContextActionHandler::my_context_action",
    }


@pytest.mark.asyncio
async def test_context_action_info_provided():
    class MyState:
        pass

    tb = Toolbox("mytools", "My Tools", "some tools", state=MyState())

    @tb.enum
    class Op(Enum):
        ADD = "add"
        SUB = "sub"

    @tb.tool
    def my_tool(a: int, s: str = "hi", e: Op = Op.ADD):
        pass

    calls = []

    @tb.context_action(tool=my_tool, target=Op)
    def my_context_action(s: MyState, i: ContextActionInfo):
        calls.append((s, i))
        return {"args": {}}

    t = tb.tools[0]
    ca = t.to_context_actions(tb)[0]
    op_name = ca["handler"]
    req_value = {"ns": "ns1", "name": "tv1", "id": "foo", "label": "Foo"}
    ra = tb.handle_action_request(op_name, {"value": req_value})
    _ = await maybe_await(ra)
    assert len(calls) == 1
    s, i = calls[0]
    assert isinstance(s, MyState)
    assert isinstance(i, ContextActionInfo)
    assert i.value == req_value


@pytest.mark.asyncio
async def test_resource_info_provided():
    class MyState:
        pass

    my_state = MyState()
    tb = Toolbox("mytools", "My Tools", "some tools", state=my_state)

    calls = []

    @tb.resource(for_type="doc")
    def doc_resource(s: MyState, req: Request, r: ResourceInfo):
        calls.append((s, req, r))
        return None

    @tb.resource(for_type="cod")
    def cod_resource(r: ResourceInfo, s: MyState, req: Request):
        calls.append((s, req, r))
        return None

    req1 = Request(dict(type="http"))
    r1 = await maybe_await(tb.handle_resource_request(req1, "doc", "doc1"))
    req2 = Request(dict(type="http"))
    r2 = await maybe_await(tb.handle_resource_request(req2, "cod", "cod1"))

    assert len(calls) == 2
    call1, call2 = calls
    (s1, r1, ri1), (s2, r2, ri2) = calls
    assert s1 is my_state
    assert s2 is my_state
    assert r1 is req1
    assert r2 is req2
    assert ri1.type == "doc"
    assert ri1.id == "doc1"
    assert ri2.type == "cod"
    assert ri2.id == "cod1"


def test_has_static_method():
    class Foo:
        @staticmethod
        def m1():
            pass

        @classmethod
        def m2(cls):
            pass

        def m3(self):
            pass

    assert has_static_method(Foo, "m1")
    assert not has_static_method(Foo, "m2")
    assert not has_static_method(Foo, "m3")


def test_has_class_method():
    class Foo:
        @staticmethod
        def m1():
            pass

        @classmethod
        def m2(cls):
            pass

        def m3(self):
            pass

    assert not has_class_method(Foo, "m1")
    assert has_class_method(Foo, "m2")
    assert not has_class_method(Foo, "m3")


def test_search_result_to_response():
    f = search_result_to_response
    assert f([]) == {"entries": []}
    assert f([("A", "a")]) == {"entries": [("A", "a")]}
    assert f({"entries": [("A", "a")]}) == {"entries": [("A", "a")]}
    assert f({"entries": [["A", "a"]]}) == {"entries": [("A", "a")]}
    assert f({"entries": [dict(key="A", label="a")]}) == {"entries": [("A", "a")]}
    assert f(
        {"entries": [("A", "a"), ["B", "b"], dict(key="C", label="c"), "bad"]}
    ) == {"entries": [("A", "a"), ("B", "b"), ("C", "c")]}
    assert f({"asd": [("A", "a")]}) == {"entries": []}


@pytest.mark.asyncio
async def test_dyn_search_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Operation(DynEnum):
        @staticmethod
        def search(query: str = ""):
            all = [
                ("ADD", "add"),
                ("SUB", "sub"),
                ("MUL", "mul"),
                ("DIV", "div"),
            ]
            return [(k, v) for k, v in all if query in v]

    ADD = Operation("ADD", "add")
    SUB = Operation("SUB", "sub")

    e = tb.enums[0]

    assert tb.handlers[e.search_handler_id] == e.load_handler
    assert await e.load_handler(dict(query="a")) == {"entries": [("ADD", "add")]}
    assert await e.load_handler(dict(query="u")) == {
        "entries": [("SUB", "sub"), ("MUL", "mul")]
    }
    assert await e.load_handler(dict(query="x")) == {"entries": []}
    assert await e.match_handler(dict(value="x")) == {"entry": None}

    arg = FnArg("a", 0, Operation, SUB)
    assert (
        await maybe_await(
            tb.provide_arg(arg, {"a": m_enum_dict("ADD", "add", tb.id, "Operation")})
        )
        == ADD
    )


def test_match_result_to_response():
    f = match_result_to_response
    assert f(None) == {"entry": None}

    assert f(1) == {"entry": None}

    assert f(("a", 1)) == {"entry": None}
    assert f((1, "a")) == {"entry": (1, "a")}
    assert f(("A", "a", "other")) == {"entry": None}

    assert f(["a", 1]) == {"entry": None}
    assert f([1, "a"]) == {"entry": (1, "a")}
    assert f(["A", "a", "other"]) == {"entry": None}

    assert f(("a", "A")) == {"entry": ("a", "A")}
    assert f(["a", "A"]) == {"entry": ("a", "A")}
    assert f([["a", "A"]]) == {"entry": ("a", "A")}
    assert f([["a", "A"], None]) == {"entry": ("a", "A")}
    assert f([42]) == {"entry": None}
    assert f(dict(key="a", label="A")) == {"entry": ("a", "A")}
    assert f([dict(key="a", label="A")]) == {"entry": ("a", "A")}

    assert f({"entry": ("a", "A")}) == {"entry": ("a", "A")}
    assert f({"entry": ["a", "A"]}) == {"entry": ("a", "A")}
    assert f({"entry!": ("a", "A")}) == {"entry": None}
    assert f({"entry": ("a", "A", "other")}) == {"entry": None}


@pytest.mark.asyncio
async def test_dyn_search_enum_custom_match():
    tb = Toolbox("mytools", "My Tools", "some tools")

    all = [
        ("ADD", "add"),
        ("SUB", "sub"),
        ("MUL", "mul"),
        ("DIV", "div"),
    ]

    @tb.enum
    class Operation(DynEnum):
        @staticmethod
        def search(query: str = ""):
            return [(k, v) for k, v in all if query in v]

        @staticmethod
        def find_best_match(query: str = ""):
            for key, val in all:
                if query in val:
                    return (key, val)
            return None

    e = tb.enums[0]

    assert tb.handlers[e.match_handler_id] == e.match_handler
    assert await e.match_handler(dict(query="a")) == {"entry": ("ADD", "add")}
    assert await e.match_handler(dict(query="u")) == {"entry": ("SUB", "sub")}
    assert await e.match_handler(dict(query="x")) == {"entry": None}


@pytest.mark.asyncio
async def test_dyn_search_enum_async_handlers():
    tb = Toolbox("mytools", "My Tools", "some tools")

    all = [
        ("ADD", "add"),
        ("SUB", "sub"),
        ("MUL", "mul"),
        ("DIV", "div"),
    ]

    @tb.enum
    class Operation(DynEnum):
        @staticmethod
        async def search(query: str = ""):
            await asyncio.sleep(0.010)
            return [(k, v) for k, v in all if query in v]

        @staticmethod
        async def find_best_match(query: str = ""):
            await asyncio.sleep(0.010)
            for key, val in all:
                if query in key or query in val:
                    return (key, val)
            return None

    DEFAULT_OPERATION = Operation("ADD", "add")
    calls = []

    @tb.tool
    async def calculate(
        a: float = 0.0, op: Operation = DEFAULT_OPERATION, b: float = 1.0
    ):
        calls.append((a, op, b))
        return 0

    _ = tb.tools[0]
    e = tb.enums[0]

    assert tb.handlers[e.search_handler_id] == e.load_handler
    assert await e.load_handler(dict(query="a")) == {"entries": [("ADD", "add")]}
    assert await e.load_handler(dict(query="u")) == {
        "entries": [("SUB", "sub"), ("MUL", "mul")]
    }
    assert await e.load_handler(dict(query="x")) == {"entries": []}

    assert tb.handlers[e.match_handler_id] == e.match_handler
    assert await e.match_handler(dict(query="a")) == {"entry": ("ADD", "add")}
    assert await e.match_handler(dict(query="u")) == {"entry": ("SUB", "sub")}
    assert await e.match_handler(dict(query="x")) == {"entry": None}

    await maybe_await(
        tb.handle_action_request("calculate", dict(a=1.0, op="ADD", b=2.0))
    )
    await maybe_await(
        tb.handle_action_request("calculate", dict(a=1.0, op="sub", b=2.0))
    )
    await maybe_await(tb.handle_action_request("calculate", dict(a=1.0, op="A", b=2.0)))
    await maybe_await(tb.handle_action_request("calculate", dict(a=1.0, b=2.0)))

    assert len(calls) == 4
    print(calls)
    assert calls == [
        (1.0, Operation("ADD", "add"), 2.0),
        (1.0, Operation("SUB", "sub"), 2.0),
        (1.0, Operation("ADD", "add"), 2.0),
        (1.0, Operation("ADD", "add"), 2.0),
    ]


def test_tool_arg_date():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.tool
    def add(d: date):
        return

    t = tb.tools[0]

    assert len(t.args) == 1
    arg = t.args[0]
    assert arg.name == "d"
    assert arg.type == date
    assert arg.default_value is None

    assert t.to_info(tb) == {
        "title": "add",
        "description": None,
        "schema": {
            "fields": {
                "d": {
                    "type": "string",
                    "default": None,
                    "description": None,
                    "format": "date",
                },
            }
        },
        "ui": {
            "prefix": t.name,
            "args": {
                "d": {"prefix": "d"},
            },
            "manualUpdate": False,
        },
        "contextActions": [],
        "examples": ["add"],
    }


@pytest.mark.asyncio
async def test_optional_tool_args():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    calls = []

    @tb.tool
    def calculate(a: int | None, op: Op | None, op1: Op = Op.ADD, b: int = 0):
        calls.append((a, op, op1, b))

    _ = tb.enums[0]

    await maybe_await(
        tb.handle_action_request("calculate", dict(a=1, op="A", op1="S", b=2))
    )
    await maybe_await(tb.handle_action_request("calculate", dict(b=2)))
    await maybe_await(tb.handle_action_request("calculate", dict()))

    assert len(calls) == 3
    assert calls == [
        (1, Op.ADD, Op.SUB, 2),
        (None, None, Op.ADD, 2),
        (None, None, Op.ADD, 0),
    ]


@pytest.mark.asyncio
async def test_optional_tool_args_dyn_enum_load():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(DynEnum):
        @staticmethod
        def load():
            return [("ADD", "add"), ("SUB", "sub"), ("MUL", "mul"), ("DIV", "div")]

    calls = []

    ADD = Op("ADD", "add")
    SUB = Op("SUB", "sub")

    @tb.tool
    def calculate(a: int | None, op: Op | None, op1: Op = ADD, b: int = 0):
        calls.append((a, op, op1, b))

    _ = tb.enums[0]

    await maybe_await(
        tb.handle_action_request("calculate", dict(a=1, op="A", op1="S", b=2))
    )
    await maybe_await(tb.handle_action_request("calculate", dict(b=2)))
    await maybe_await(tb.handle_action_request("calculate", dict()))

    assert len(calls) == 3
    assert calls == [
        (1, ADD, SUB, 2),
        (None, None, ADD, 2),
        (None, None, ADD, 0),
    ]


@pytest.mark.asyncio
async def test_optional_tool_args_dyn_enum_search():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(DynEnum):
        @staticmethod
        def search(query: str = ""):
            all = [
                ("ADD", "add"),
                ("SUB", "sub"),
                ("MUL", "mul"),
                ("DIV", "div"),
            ]
            return [(k, v) for k, v in all if query in v]

    calls = []

    ADD = Op("ADD", "add")
    SUB = Op("SUB", "sub")

    @tb.tool
    def calculate(a: int | None, op: Op | None, op1: Op = ADD, b: int = 0):
        calls.append((a, op, op1, b))

    _ = tb.enums[0]

    op_add = make_enum_dict(tb.id, "Op", "ADD", "add")
    op_sub = make_enum_dict(tb.id, "Op", "SUB", "sub")

    await maybe_await(
        tb.handle_action_request("calculate", dict(a=1, op=op_add, op1=op_sub, b=2))
    )
    await maybe_await(tb.handle_action_request("calculate", dict(b=2)))
    await maybe_await(tb.handle_action_request("calculate", dict()))

    assert len(calls) == 3
    assert calls == [
        (1, ADD, SUB, 2),
        (None, None, ADD, 2),
        (None, None, ADD, 0),
    ]


@pytest.mark.asyncio
async def test_key_value_enum():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(KeyValueEnum):
        ADD = ("+", "add")
        SUB = ("-", "sub")
        MUL = ("*", "mul")
        DIV = ("/", "div")

    assert Op.ADD.name == "ADD"
    assert Op.ADD.key == "+"
    assert Op.ADD.value == "add"

    v = Variant.from_enum_variant(Op.ADD)
    assert v.name == "+"
    assert v.value == "add"
    assert v.enum_value == Op.ADD
    assert v.docs is None

    e = tb.enums[0]

    assert len(e.variants) == 4
    assert e.variants[0] == e.variants_by_key["+"]
    assert await e.from_raw_arg_value("+") == Op.ADD
    assert await e.from_raw_arg_value("add") == Op.ADD
    assert await e.from_raw_arg_value("-") == Op.SUB
    assert await e.from_raw_arg_value("sub") == Op.SUB
    assert await e.from_raw_arg_value("*") == Op.MUL
    assert await e.from_raw_arg_value("/") == Op.DIV
    assert await e.from_raw_arg_value("!") == Op.ADD


@pytest.mark.asyncio
async def test_key_value_enum_tool_arg():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(KeyValueEnum):
        ADD = ("+", "add")
        SUB = ("-", "sub")
        MUL = ("*", "mul")
        DIV = ("/", "div")

    calls = []

    @tb.tool
    def calculate(a: int | None, op: Op | None, op1: Op = Op.ADD, b: int = 0):
        calls.append((a, op, op1, b))

    e = tb.enums[0]

    assert e.variants[0].name == "+"
    assert e.variants[0].value == "add"

    op_add = make_enum_dict(tb.id, "Op", "+", "add")
    op_sub = make_enum_dict(tb.id, "Op", "-", "sub")
    op_mul = make_enum_dict(tb.id, "Op", "*", "mul")

    await maybe_await(
        tb.handle_action_request("calculate", dict(a=1, op=op_add, op1=op_sub, b=2))
    )
    await maybe_await(tb.handle_action_request("calculate", dict(b=2)))
    await maybe_await(tb.handle_action_request("calculate", dict()))
    await maybe_await(tb.handle_action_request("calculate", dict(op1=op_mul)))

    assert len(calls) == 4
    assert calls == [
        (1, Op.ADD, Op.SUB, 2),
        (None, None, Op.ADD, 2),
        (None, None, Op.ADD, 0),
        (None, None, Op.MUL, 0),
    ]


def test_info_tool_arg_description_is_enum_doc_if_not_set():
    tb = Toolbox("mytools", "My Tools", "some tools")

    @tb.enum
    class Op(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    @tb.tool
    def my_tool(e: Op = Op.ADD):
        pass

    t = tb.tools[0]
    assert (
        t.to_info(tb).get("schema").get("fields").get("e").get("description")
        == "the operation to apply"
    )


def test_enum_to_data_tag():
    ns = "mytools"
    tb = Toolbox(ns, "My Tools", "some tools")

    @tb.enum
    class Op(Enum):
        "the operation to apply"

        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"

    assert Op.ADD.to_data_tag() == format_enum_data_tag(ns, Op, Op.ADD)


def test_dyn_enum_to_data_tag():
    ns = "mytools"
    tb = Toolbox(ns, "My Tools", "some tools")

    @tb.enum
    class Color(DynEnum):
        @staticmethod
        def load():
            return [
                ("RED", "Red"),
                ("GREEN", "Green"),
                ("BLUE", "Blue"),
            ]

    RED = Color("RED", "Red")

    assert RED.to_data_tag() == format_data_tag(ns, "Color", "RED", "Red")
