"""
Requirements:

- get, set
- .raw_value


a.smart_property.raw_value
?? - wtf? should it be a.path_to_docs.raw_value?
or a new one?
anyways, should return raw path

`:type: str` or int or float or None

`:check_exists` - checks if path exists
`:abspath` - returns absolute path


"""

# import functools
import textwrap
import ast 
import os 
import warnings


class SmartDebug(Warning):
    pass


def debug(*args, **kwargs):
    s = " ".join(*args)
    warnings.warn(s, SmartDebug, stacklevel=2)


class DocParser(object):
    """Parses docstrings to the specification.
    
    Parameters
    ----------
    s_prop : list of str
        The key of key-value tags: `:key: value`
    s_bool : list of str
        The flags to check for: `:key`
    """
    
    def __init__(
        self, doc, 
        s_prop=('type', 'default'),
        s_bool=('check_exists', 'abspath')
    ):        
        self.s_prop = s_prop
        self.s_bool = s_bool
        self.doc = doc = textwrap.dedent(doc)
        
        for line in doc.splitlines():
            line = line.strip()
            ld = False

            # Check for key-value
            for p in self.s_prop:
                ps = ':' + p + ': '
                if line.startswith(ps):
                    val = line[len(ps):].strip()
                    setattr(self, p, val)
                    ld = True
                    break

            # Skip checking for the bool
            if ld:
                continue
            
            # Check for bool
            for b in self.s_bool:
                if line.startswith(':' + b):
                    setattr(self, b, True)
                    break

        # Fill in other keys with default values

        # bools are false by default (flags)
        for b in self.s_bool:
            if not hasattr(self, b):
                setattr(self, b, False)
        
        # k:v are None by default
        for p in self.s_prop:
            if not hasattr(self, p):
                setattr(self, p, None)
        
    def __str__(self):
        return "\n".join(
            ["DocParser:", "----------"] +
            [
                ":%s: %s" % (p, getattr(self, p)) 
                for p in self.s_prop 
                if hasattr(self, p)
            ] +
            [
                ":%s" % b 
                for b in self.s_bool 
                if getattr(self, b, False)
            ]
        )

    def __repr__(self):
        return "%s(%r, s_prop=%r, s_bool=%r)" % (
            self.__class__.__name__,
            self.doc,
            self.s_prop, 
            self.s_bool, 
        )


class PropParser(object):
    """Parses documentation to the task's specification.
    
    Note
    ----
    Not using inheritance because we want 'clean' properties.
    """

    def __init__(self, doc):
        s_prop = (
            'type',  # Argument type (str, bool, int, float), default None
            'default',  # Default value (overrides function return)
        )
        s_bool = (
            'readonly',  # If set, raise when trying to set
            'mandatory',  # If set, requires a non-None value
            # Relevant to paths (i.e. only str)
            'check_exists', 'create_if_not_exists', 'abspath', 
            'debug',  # If set, does debug printing everywhere.
        )
        # The DocParser set all relevant attributes
        self.raw = raw = DocParser(doc, s_prop=s_prop, s_bool=s_bool)

        # Check debugging
        self.debug = raw.debug

        # Find type
        self.type = {
            'str': str, 'bool': bool, 'int': int, 'float': float, 
            'None': None, 
        }.get(raw.type, None)

        # Check if is mandatory
        self.mandatory = raw.mandatory

        # Parse default value
        self.default = self.parse_literal(raw.default)

        # Other flags
        self.readonly = raw.readonly
        self.check_exists = raw.check_exists
        self.create_if_not_exists = raw.create_if_not_exists
        self.abspath = raw.abspath

    def parse_literal(self, value):
        """Parses value, according to our set flags."""

        if self.debug:
            debug("Passed value: %r" % value)
        
        if value is None:
            if self.mandatory:
                raise ValueError("Value is mandatory!")
            return None

        # If type isn't set, accept any value
        if self.type is None:
            return value
        elif self.type is str:
            return str(value)
        
        if isinstance(value, str):
            # Try parsing the string
            try:  # No, not going to do '2 ** 20' stuff, no time
                value = ast.literal_eval(value)
            except Exception:
                raise ValueError("Couldn't parse: %r" % value)
        
        # Check exact type
        if isinstance(value, self.type):
            return value

        # Check Safe conversions: 

        if isinstance(value, int):
            if self.type is float:
                return float(value)

        if isinstance(value, float):
            if (self.type is int) and (int(value) == value):
                return int(value)
        
        # Check again for mandatory value
        if value is None:
            return self.parse_literal(value)

        # Otherwise, fail        
        raise TypeError(
            "Passed value of the wrong type: %r (%s)" 
            % (value, type(value))
        )


class smart_property(object):
    """"""

    def __init__(self, func, doc=None):
        # Find out how to name the attribute
        func_name = getattr(func, '__name__', 'Attribute')
        self.attr_name = "_" + func_name
        self.func = func

        # Find and parse docstring
        if doc is None:
            doc = getattr(func, '__doc__', '')
        self.parsed = PropParser(doc)
        # TODO: Switch up with setting stuff

    def __get__(self, instance, owner):
        # NOTE for self:
        # instance is the parent object
        # owner is type(instance)

        if self.parsed.debug:
            debug("==| Instance: %r" % instance)
            debug("==| Owner: %r" % owner)

        # default_value = self.func(instance)
        default_value = self.parsed.default
        res = getattr(instance, self.attr_name, default_value)

        # create it if we don't have it - alt, could set every time
        if not hasattr(instance, self.attr_name):
            setattr(instance, self.attr_name, res)

        # Path-specific stuff :)
        f_abs = self.parsed.abspath
        f_ce = self.parsed.check_exists
        f_cine = self.parsed.create_if_not_exists

        # Check if we assume that it's a path
        if (self.parsed.type is str) and any((f_abs, f_ce, f_cine)):
            if self.parsed.debug:
                debug("It's a path!")
            
            if f_abs:
                res = os.path.abspath(res)
            if f_ce and f_cine:
                with open(res, 'a+'):
                    # We use append mode to create, if not exists
                    pass
            elif f_ce and not os.path.exists(res):
                raise ValueError("Path does not exist: %r" % res)

        return res

    def __set__(self, instance, value):
        # NOTE for self:
        # instance is the parent object
        # value is the RHS

        if self.parsed.debug:
            debug("==| Instance: %r" % instance)
            debug("==| Value: %r" % value)

        # Handle readonly attributes
        if self.parsed.readonly:
            raise AttributeError(
                "%s is readonly." % 
                getattr(self.func, '__name__', 'Attribute')
            )

        # Check types and such
        value = self.parsed.parse_literal(value)

        setattr(instance, self.attr_name, value)


if __name__ == "__main__":
    doc1 = """
            Property description.

            :type: str
            :default: ./docs

            :check_exists 
            :abspath 
            #:mandatory
    """

    doc2 = """
            Property description.

            :type: float
            :default: 100

            :check_exists 
            #:mandatory
    """

    for doc in (doc1, doc2):
        parsed = PropParser(doc)
        print(parsed.raw)
        print(parsed.default)
        print(type(parsed.default))
        print("==================")
#
