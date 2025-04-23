from enum import Enum

__all__ = ["entity","events","messages","templates"]

_dust_logger = None

def set_logger(logger):
    global _dust_logger
    _dust_logger = logger

def logger():
    global _dust_logger
    return _dust_logger

class Datatypes(Enum):
    INT = 0
    NUMERIC = 2
    BOOL = 3
    STRING = 4
    BYTES = 5
    JSON = 9
    ENTITY = 10

class ValueTypes(Enum):
    SINGLE = 0
    SET = 1
    LIST = 2
    MAP = 3

class Modes(Enum):
    NULLABLE = 0
    REQUIRED = 1
    REPEATED = 2
    TRANSIENT = 3

class Operation(Enum):
    SET = 0
    ADD = 1
    GET = 2
    PEEK = 3
    VISIT = 4
    CHANGE = 5
    DEL = 6
    WALK = 7

class Committed(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    SAVED = 3

class MetaProps(Enum):
    @property
    def datatype(self):
        return self.value[0]

    @property
    def valuetype(self):
        return self.value[1]

    @property
    def order_value(self):
        return self.value[2]

    @property
    def id_value(self):
        return self.value[3]
    
    def to_json(self):
        return {
            "datatype": self.datatype.name,
            "valuetype": self.valuetype.name,
            "order_value": self.order_value,
            "id_value": self.id_value
        }

class FieldProps(Enum):
    @property
    def unit_name(self):
        return self.value[0]

    @property
    def type_name(self):
        return self.name

    @property
    def fields_enum(self):
        return self.value[1]

    @property
    def id_value(self):
        return self.value[2]



