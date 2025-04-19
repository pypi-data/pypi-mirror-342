from dataclasses import is_dataclass, fields, Field
from typing import Any, List, Type, get_origin, get_args, cast


def serialize_dataclass_to_list(obj: Any) -> List[Any]:
    """
        Serialize a dataclass instance into a flat list of its field values.

        This function recursively serializes fields that are themselves dataclasses,
        and also properly handles lists of dataclasses.

        Supports both regular dataclasses and dataclasses that use __slots__.

        Args:
            obj (Any): The dataclass instance to serialize.

        Returns:
            List[Any]: A list representing the serialized fields of the dataclass,
            preserving nested structures.

        Raises:
            ValueError: If the input is not a dataclass instance.

        Example:
            >>> @dataclass
            ... class Child:
            ...     x: int
            ...     y: str
            ...
            >>> @dataclass
            ... class Parent:
            ...     a: int
            ...     b: Child
            ...     c: List[Child]
            ...
            >>> p = Parent(a=1, b=Child(x=10, y="hello"), c=[Child(x=20, y="world")])
            >>> serialize_dataclass_to_list(p)
            [1, [10, 'hello'], [[20, 'world']]]
        """
    if not is_dataclass(obj):
        raise ValueError(f"Expected dataclass instance, got {type(obj)}")

    if hasattr(obj, '__slots__'):
        slots = getattr(obj, '__slots__')
        result = []
        for slot_name in slots:
            value = getattr(obj, slot_name)
            if is_dataclass(value):
                result.append(serialize_dataclass_to_list(value))
            elif isinstance(value, list) and value and is_dataclass(value[0]):
                result.append([serialize_dataclass_to_list(item) for item in value])
            else:
                result.append(value)
        return result
    else:
        result = []
        for f in fields(obj):
            value = getattr(obj, f.name)
            if is_dataclass(value):
                result.append(serialize_dataclass_to_list(value))
            elif isinstance(value, list) and value and is_dataclass(value[0]):
                result.append([serialize_dataclass_to_list(item) for item in value])
            else:
                result.append(value)
        return result


def deserialize_list_to_dataclass[T](cls: Type[T], data: List[Any]) -> T:
    """
        Deserialize a list of values into a dataclass instance.

        This function reconstructs nested dataclasses and lists of dataclasses
        if the dataclass structure requires it.

        Supports both regular dataclasses and dataclasses with __slots__.

        Args:
            cls (Type[T]): The dataclass type to instantiate.
            data (List[Any]): The list of values representing the serialized fields.

        Returns:
            T: An instance of the dataclass reconstructed from the provided list.

        Raises:
            ValueError: If cls is not a dataclass or if the number of fields and values do not match.

        Example:
            >>> @dataclass
            ... class Child:
            ...     x: int
            ...     y: str
            ...
            >>> @dataclass
            ... class Parent:
            ...     a: int
            ...     b: Child
            ...     c: List[Child]
            ...
            >>> data = [1, [10, 'hello'], [[20, 'world']]]
            >>> deserialize_list_to_dataclass(Parent, data)
            Parent(a=1, b=Child(x=10, y='hello'), c=[Child(x=20, y='world')])
        """
    if not is_dataclass(cls):
        raise ValueError(f"Expected dataclass class, got {cls}")

    cls_fields: tuple[Field[Any], ...] = fields(cls)

    if len(data) != len(cls_fields):
        raise ValueError(f"Field count mismatch: expected {len(cls_fields)}, got {len(data)}")

    init_kwargs: dict[str, Any] = {}
    for field_obj, value in zip(cls_fields, data):
        field_type = field_obj.type
        if _is_nested_dataclass(field_type):
            init_kwargs[field_obj.name] = deserialize_list_to_dataclass(cast(Type[Any], field_type), value)
        elif _is_list_of_nested_dataclass(field_type):
            inner_cls = _get_list_inner_type(field_type)
            init_kwargs[field_obj.name] = [deserialize_list_to_dataclass(cast(Type[Any], inner_cls), v) for v in value]
        else:
            init_kwargs[field_obj.name] = value

    return cast(T, cls(**init_kwargs))


def _is_nested_dataclass(typ: Any) -> bool:
    return isinstance(typ, type) and is_dataclass(typ)


def _is_list_of_nested_dataclass(typ: Any) -> bool:
    origin = get_origin(typ)
    args = get_args(typ)
    return bool(origin in (list, List) and args and isinstance(args[0], type) and is_dataclass(args[0]))


def _get_list_inner_type(typ: Any) -> Type[Any]:
    args = get_args(typ)
    if not args:
        raise ValueError(f"List type {typ} has no inner type")
    return cast(Type[Any], args[0])
