import json
from itertools import zip_longest
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from drfexts.renderers import CustomCSVRenderer
from drfexts.renderers import CustomXLSXRenderer

from .filtersets.filters import MultipleSelectFilter
from .utils.utils import get_nested_value


class EagerLoadingMixin:
    function_name = "setup_eager_loading"

    def get_queryset(self, *args, **kwargs):
        """
        Call setup_eager_loading function on serializer
        """
        queryset = super().get_queryset(*args, **kwargs)
        serilaizer_class = self.get_serializer_class()  # noqa
        if hasattr(serilaizer_class, "setup_eager_loading") and callable(
            serilaizer_class.setup_eager_loading
        ):
            queryset = serilaizer_class.setup_eager_loading(queryset)
            assert isinstance(queryset, QuerySet), (
                f"Expected '{self.function_name}' to return a QuerySet, "
                f"but got a {type(queryset).__name__} instead."
            )

        return queryset


class SelectOnlyMixin:
    """
    Mixin used to define select-only fields for queryset
    Cautions:
        1. The mixin is intended for performance optimization
        and you don't need it in most cases.
    """

    # If using Django filters in the API, these labels mustn't
    # conflict with any model field names.
    include_only_fields_name = "only_fields"
    expand_only_fields_name = "expand_only_fields"
    exclude_only_fields_name = "exclude_only_fields"

    def get_queryset(self):
        """
        Select only fields
        """
        queryset = super().get_queryset()
        serilaizer_class = self.get_serializer_class()  # noqa

        assert issubclass(serilaizer_class, ModelSerializer), (
            f"Class {serilaizer_class.__class__.__name__} "
            f'must inherit from "ModelSerializer"'
        )

        if getattr(queryset, "_result_cache", None):
            return queryset

        meta = getattr(serilaizer_class, "Meta", None)
        only_fields = getattr(meta, self.include_only_fields_name, None)
        expand_only_fields = set(getattr(meta, self.expand_only_fields_name, []))
        # You may need to set this attribute when fetch attrs in `SerializerMethod`
        # or in a nested serializer
        exclude_query_fields = set(getattr(meta, self.exclude_only_fields_name, []))
        if only_fields and exclude_query_fields:
            raise ImproperlyConfigured(
                "You cannot set both 'only_fields' and 'exclude_only_fields'."
            )

        if only_fields:
            return queryset.only(*only_fields)

        only_fields_name = set()
        for field in serilaizer_class()._readable_fields:
            if field.field_name in exclude_query_fields:
                continue

            # TODO: support nested serializer
            if isinstance(field, (ReadOnlyField, Serializer)):
                continue

            source = getattr(field, "source", None)
            # serliazer method class will set source to '*'
            if source == "*":
                continue

            if source:
                query_name = "__".join(source.split("."))
            else:
                query_name = field.field_name

            only_fields_name.add(query_name)

        only_fields_name |= expand_only_fields
        if only_fields_name:
            queryset = queryset.only(*only_fields_name)

        return queryset


class ExtGenericViewSet(GenericViewSet):
    _default_key = "default"
    queryset_function_name = "process_queryset"
    data_permission_class = None
    # The filter backend classes to use for queryset filtering

    def get_serializer_class(self):
        """
        支持针对不同action指定不同的序列化器
        """
        assert self.serializer_class is not None, (
            f"'{self.__class__.__name__}' should either include a `serializer_class` attribute, "  # noqa
            "or override the `get_serializer_class()` method."
        )
        if isinstance(self.serializer_class, dict):  # 多个serializer_class
            assert (
                self._default_key in self.serializer_class
            ), f"多个serializer时serializer_class必须包含下列key:{self._default_key}"
            if self.serializer_class.get(self.action):
                return self.serializer_class.get(self.action)
            else:
                return self.serializer_class.get(self._default_key)

        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        支持动态设置序列化器字段
        """
        serializer_class = self.get_serializer_class()
        if hasattr(serializer_class, "get_included_fields") and callable(
            serializer_class.get_included_fields
        ):
            included_fields = serializer_class.get_included_fields(self, self.request)
            if included_fields:
                kwargs["fields"] = included_fields

        if hasattr(serializer_class, "get_excluded_fields") and callable(
            serializer_class.get_excluded_fields
        ):
            excluded_fields = serializer_class.get_excluded_fields(self, self.request)
            if excluded_fields:
                kwargs["omit"] = excluded_fields

        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def data_permissions(self, request, view, queryset):
        """
        检查数据权限
        """
        for permission in self.get_permissions():
            if hasattr(permission, "data_permission"):
                return permission.data_permission(request, view, queryset)

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'{self.__class__.__name__}' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
            # Perform optimization on queryset
            serializer_class = self.get_serializer_class()
            if hasattr(serializer_class, self.queryset_function_name):
                queryset = getattr(serializer_class, self.queryset_function_name)(
                    self.request, queryset
                )

        # add data permission
        if data_permission_cls := getattr(self, "data_permission_class", None):
            data_permission = data_permission_cls()
            if perm_fuc := getattr(data_permission, f"{self.action}_permission", None):
                queryset = perm_fuc(self.request, queryset)

        return queryset

    def get_filterset_fields_overwrite(self):
        """
        Return the filterset fields overwrite.
        """
        return getattr(self, "filterset_fields_overwrite", {})


class ExportMixin:
    """
    Export data to csv/xlsx file
    """

    export_actions = ["list"]
    default_base_filename = "export"

    def get_filterset_fields_overwrite(self):
        filterset_fields_overwrite = super().get_filterset_fields_overwrite()  # noqa
        return {
            "ids": MultipleSelectFilter(field_name="pk"),
            **filterset_fields_overwrite,
        }

    def is_export_action(self) -> bool:
        """
        Return True if the current action is an export action.
        :return:
        """
        if not hasattr(self.request, "accepted_media_type"):
            return False

        return self.request.accepted_media_type.startswith(  # noqa
            (
                "text/csv",
                "application/xlsx",
            )
        )

    def get_renderers(self):
        """
        Instantiates and returns the list of renderers that this view can use.
        """
        renderers = super().get_renderers()  # noqa
        if self.action in self.export_actions:  # noqa
            return renderers + [CustomCSVRenderer(), CustomXLSXRenderer()]

        return renderers

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        :return:
        """
        serializer_class = super().get_serializer_class()  # noqa
        if not self.is_export_action():
            return serializer_class

        fields = self.request.query_params.get("fields", "")
        column_names = self.request.query_params.get("field_names", "")
        fields_map = json.loads(self.request.query_params.get("fields_map", "{}"))
        field_names = fields.split(",") if fields else []
        field_column_names = column_names.split(",") if column_names else []
        if not fields_map:
            fields_map = dict(zip_longest(field_names, field_column_names))

        def trans_val(value):
            if isinstance(value, list):
                value = ",".join(
                    v["label"] if isinstance(v, dict) and "label" in v else str(v)
                    for v in value
                )
            elif isinstance(value, dict) and "label" in value:
                value = value["label"]
            elif isinstance(value, bool):
                value = "是" if value else "否"
            return value

        class ExportSerializer(serializer_class):
            def to_representation(self, instance):
                """
                Serialize objects -> primitive datatypes.
                """
                data = super().to_representation(instance)
                ret = {}

                for field_name in field_names:
                    val = get_nested_value(data, field_name, default="")
                    col_name = fields_map[field_name] or field_name
                    ret[col_name] = trans_val(val)

                return ret

        return ExportSerializer

    def get_renderer_context(self):
        """
        Return the renderer context to use for rendering.
        :return:
        """
        context = super().get_renderer_context()  # noqa
        export_filename = self.get_export_filename()
        if export_filename:
            context["writer_opts"] = {"filename": export_filename}

        return context

    def get_export_filename(self):
        """
        Return the filename of the export file.
        :return:
        """
        filext = ""
        if self.request.accepted_media_type.startswith("text/csv"):
            filext = ".csv"
        elif self.request.accepted_media_type.startswith("application/xlsx"):
            filext = ".xlsx"

        if "filename" in self.request.query_params:  # noqa
            fullname = Path(self.request.query_params["filename"]).stem + filext
        else:
            fullname = f"{self.default_base_filename}({timezone.now().date()}){filext}"

        return fullname
