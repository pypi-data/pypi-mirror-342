import logging
import os
import random
from collections import OrderedDict
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.db.transaction import atomic
from django.http import QueryDict
from django.utils import timezone
from rest_framework import exceptions
from rest_framework import serializers


class CustomEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return super().default(obj)


class MakeFileHandler(logging.FileHandler):
    def __init__(self, filename, mode="a", encoding=None, delay=0):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        super().__init__(filename, mode, encoding, delay)


@atomic
def atomic_call(*funcs):
    """
    Call function atomicly
    """
    for func in funcs:
        if not callable(func):
            raise TypeError(f"{func} must be callable!")

        func()


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"invalid truth value {val}")


def get_serial_code(prefix=""):
    """
    生成序列号
    """
    random_number = random.randint(0, 999)
    return timezone.now().strftime(f"{prefix}%y%m%d%H%M%I{random_number:03d}")


def to_table_choices(choices: OrderedDict):
    """
    转换为前端适配的options
    """
    return [{"label": label, "value": value} for value, label in choices.items()]


def get_field_info(field):
    """
    序列化器字段提取信息
    :param field:
    :return:
    """
    field_info = {"column_name": str(field.label)}
    if isinstance(field, serializers.ChoiceField) and getattr(field, "choices", None):
        field_info["choices"] = dict(field.choices)

    return field_info


def get_serializer_field(serializer, field_path):
    """
    获取序列化器中的字段
    """
    attrs = field_path.split(".")
    is_skipped = False
    source_attrs = []
    for attr in attrs:
        try:
            serializer = serializer.fields[attr]
            if serializer.source == "*":
                continue
            source_attrs.extend(serializer.source.split("."))
        except KeyError:
            is_skipped = True
            break
        except AttributeError:
            break

    return serializer, source_attrs, is_skipped


def get_error_msg(data: dict | list, default_field_key):
    if isinstance(data, dict):
        if "detail" in data:
            return str(data["detail"])
        elif default_field_key in data:
            return "\n".join(str(s) for s in data[default_field_key])

        errors = []
        for k, v in data.items():
            if isinstance(v, dict):
                errors.append(get_error_msg(v, default_field_key))
                # errors.append(f"{k}: {'\n'.join(str(s) for s in v.values())}")
            else:
                errors.append(f"{k}: " + "\n".join(str(s) for s in v))

        return "\n".join(errors)
    elif isinstance(data, exceptions.ErrorDetail):
        return str(data)
    elif isinstance(data, list):
        data = data[0]
        return get_error_msg(data, default_field_key)

    return str(data)


def get_split_query_params(query_params: QueryDict, field_name: str) -> list[str]:
    """
    获取分割后的查询参数
    注意：变量"a.b.c"只取"a"
    :param query_params:
    :param field_name:
    :return:
    """
    value = query_params.getlist(field_name)
    if not value:
        value = query_params.get(field_name + "[]")

    if value and len(value) == 1:
        return [val.split(".", 1)[0] for val in value[0].split(",")]

    return []


def get_nested_value(d, key, default=None):
    """
    函数通过将键字符串拆分成键列表，然后逐层获取嵌套字典中的值。
    如果在任何层次上键不存在，函数将返回 default
    """
    keys = key.split(".")
    value = d
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, default)
        else:
            return default
    return value
