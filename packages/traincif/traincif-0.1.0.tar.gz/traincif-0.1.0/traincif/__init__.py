from dataclasses import dataclass
from io import BytesIO
from types import NoneType
from typing import Any, Callable, Iterator, Literal, Self, Annotated
from struct import Struct, error as StructError
import typing

@dataclass
class Field:
    length: int
    transform: Callable[[bytes], Any] | None = None
    discriminant: bool = False


class CifError(Exception):
    pass


def validate_literal_factory(literal: Any, transform: Callable[[bytes], Any] | None):
    def _inner(cmp: Any):
        if transform:
            cmp = transform(cmp)
        
        if literal != cmp:
            raise CifError(f"Expected literal {literal}, got {cmp}")
    
    return _inner


class CifMeta(type):
    """
    Metaclass for CifRecord
    """
    
    def __new__(cls, cls_name: str, bases: tuple[type], attrs: dict[str, Any]) -> object:
        print(cls_name, bases, attrs)
        cls = super(CifMeta, cls).__new__(cls, cls_name, bases, attrs)
        
        struct_names: list[str] = []
        struct_transforms: list[Callable[[bytes], Any] | None] = []
        struct_arg = ""
        current_pos = 0
        
        discriminant_range: tuple[int, int] | None = None
        discriminant_transform: Callable[[bytes], Any] | None = None
        discriminant_value: Any = None
        
        hints = typing.get_type_hints(cls, include_extras=True, globalns=globals())
        print(hints)
        
        for name, hint in hints.items():
            if name.startswith("__"):
                continue
            
            struct_names.append(name)
            assert typing.get_origin(hint) is Annotated
            (typ, field) = typing.get_args(hint)
            
            assert isinstance(field, Field)
            
            is_literal = typing.get_origin(typ) is Literal
            
            if is_literal:
                (literal_value,) = typing.get_args(typ)
                
                typ = type(literal_value)
            
            if field.transform is None:
                if typ is bytes:
                    pass
                elif typ is int:
                    field.transform = int
                elif typ is str:
                    field.transform = lambda x: x.decode().strip()
                elif typ is NoneType:
                    field.transform = lambda _: None
                else:
                    raise CifError(f"Don't know how to handle type {typ}. Please use Field(transform=...)")
            
            if field.discriminant:
                if not is_literal:
                    raise CifError(f"{name} is a discriminant, but not a literal")
                
                if discriminant_range is not None:
                    raise CifError(f"{cls_name} already has a discriminant")
                
                discriminant_range = (current_pos, field.length + current_pos)
                discriminant_value = literal_value
                discriminant_transform = field.transform
            
            if is_literal:
                field.transform = validate_literal_factory(literal_value, field.transform)
            
            struct_transforms.append(field.transform)
            
            current_pos += field.length
            struct_arg += f"{field.length}s"
        
        print(struct_arg)
        struct = Struct(struct_arg)
        
        def __init__(self: object, parse: bytes):
            try:
                unpacked = struct.unpack(parse)
            except StructError as e:
                raise CifError(f"error while unpacking bytes: {e}")
            
            for name, transform, value in zip(struct_names, struct_transforms, unpacked):
                if transform is None:
                    setattr(self, name, value)
                else:
                    setattr(self, name, transform(value))
        
        def __repr__(self: object):
            rep = f"{cls_name}("
            for attr in struct_names:
                rep += f"{attr}={repr(getattr(self, attr))}, "
            
            rep = rep[:-2] + ")"
            return rep
        
        def to_dict(self: object):
            ret = dict()
            
            for attr in struct_names:
                ret[attr] = getattr(self, attr)
            
            return ret
        
        cls.__init__ = __init__
        cls.__repr__ = __repr__
        cls.to_dict = to_dict
        cls.__discriminant_range__ = discriminant_range
        cls.__discriminant_value__ = discriminant_value
        cls.__discriminant_transform__ = discriminant_transform
        
        return cls


class CifRecord(metaclass=CifMeta):
    """
    A CifRecord 
    """
    
    __discriminant_range__: tuple[int, int] | None
    __discriminant_value__: Any
    __discriminant_transform__: Callable[[bytes], Any] | None
    
    def __init__(self, parse: bytes) -> None:
        """
        Parse some bytes into this CifRecord.
        """
        ...
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert this CifRecord into a dictionary.
        """
        ...
    
    @classmethod
    def parse_from_file(cls, file: BytesIO) -> Iterator[Self]:
        """
        Parse this CifRecord from a file, skipping over comments (/!!).
        Returns an iterator over CifRecords in the file.
        """
        
        while (line := file.readline()) != b"":
            if line.startswith(b"/!!"):
                continue
            
            if line.strip() == b"":
                continue
            
            yield cls(line[:-1])


class CifUnion[T: CifRecord]:
    members: list[type[T]]
    
    def __init__(self, *members: type[T]) -> None:
        for member in members:
            if member.__discriminant_range__ is None:
                raise CifError(f"member {member} does not have a discriminant")
        
        self.members = list(members)
    
    def __call__(self, parse: bytes) -> T:
        for member in self.members:
            rng = member.__discriminant_range__
            value = parse[rng[0]:rng[1]]
            
            if (transform := member.__discriminant_transform__) is not None:
                value = transform(value)
            
            if value == member.__discriminant_value__:
                return member(parse)
        
        raise Exception("no discriminants matched")
    
    def parse_from_file(self, file: BytesIO) -> Iterator[Self]:
        """
        Parse this CifUnion from a file, skipping over comments (/!!).
        Returns an iterator over CifRecords in the file.
        """
        
        while (line := file.readline()) != b"":
            if line.startswith(b"/!!"):
                continue
            
            if line.strip() == b"":
                continue
            
            yield self(line[:-1])
