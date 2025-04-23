import datetime

class DBTypeObject:
    def __init__(self, *values):
        self.values = values

    def __eq__(self, other):
        if other in self.values:
            return True
        return False
        

STRING = DBTypeObject("varchar", "text", "char")
INTEGER = DBTypeObject("integer", "int", "bigint", "smallint", "tinyint")
FLOAT = DBTypeObject("float", "double", "decimal", "dec")
BOOLEAN = DBTypeObject("boolean", "bool")
DATE = DBTypeObject("date")
DATETIME = DBTypeObject("datetime", "timestamp")
NULL = DBTypeObject("null")


def convert_datatype(data: str, dtype: str = "") -> any:
    if dtype.lower() == STRING:
        if data.startswith("'") and data.endswith("'"):
            return data[1:-1]
        else:
            raise ValueError(f"Invalid string format: {data} is not a string")
    elif data.startswith("'") and data.endswith("'") and dtype.lower() != STRING:
        raise ValueError(f"Invalid {dtype.lower} format: {data} is a string, not a {dtype.lower()}")
    elif dtype.lower() == INTEGER:
        try:
            return int(data)
        except ValueError:
            raise ValueError(f"Invalid integer format: {data} is not an integer")
    elif dtype.lower() == FLOAT:
        try:
            return float(data)
        except ValueError:
            raise ValueError(f"Invalid float format: {data} is not a float")
    elif dtype.lower() == BOOLEAN:
        if data.lower() in ["true", "false"]:
            return data.lower() == "true"
        else:
            raise ValueError(f"Invalid boolean format: {data} is not a boolean value")
    elif dtype.lower() == DATE or dtype.lower() == DATETIME:
        try:
            return datetime.datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format (format %Y-%m-%d): {data}")
    elif dtype.lower() == NULL:
        if data.lower() == "null":
            return None
        else:
            raise ValueError(f"Invalid null format: {data}")
    else:
        try:
            if data.startswith("'") and data.endswith("'"):
                return data[1:-1]
            else:
                try:
                    return int(data)
                except ValueError:
                    try:
                        return float(data)
                    except ValueError:
                        return data
        except Exception as e:
            raise ValueError(f"Invalid data format: {data}") from e