"""
    Elementary IR types.
"""
from . import ir, util
import sys
from typing import cast


#
# Basic Types
#
Null = ir.ScalarType("Null", util.frozen())
Any = ir.ScalarType("Any", util.frozen())
Hash = ir.ScalarType("Hash", util.frozen())
String = ir.ScalarType("String", util.frozen())
Number = ir.ScalarType("Number", util.frozen())
Int = ir.ScalarType("Int", util.frozen())
Float = ir.ScalarType("Float", util.frozen())
Decimal = ir.ScalarType("Decimal", util.frozen())
Bool = ir.ScalarType("Bool", util.frozen())
Binary = ir.ScalarType("Binary", util.frozen()) # 0 or 1
Symbol = ir.ScalarType("Symbol", util.frozen())
Sha1 = ir.ScalarType("SHA1", util.frozen())

AnySet = ir.SetType(Any)
NumberSet = ir.SetType(Number)
StringSet = ir.SetType(String)
IntSet = ir.SetType(Int)

AnyList = ir.ListType(Any)
SymbolList = ir.ListType(Symbol)

def is_builtin(t: ir.Type):
    return t in builtin_types

def _compute_builtin_types() -> list[ir.Type]:
    module = sys.modules[__name__]
    types = []
    for name in dir(module):
        builtin = getattr(module, name)
        if isinstance(builtin, ir.Type):
            types.append(builtin)
    return types

builtin_types = _compute_builtin_types()
builtin_scalar_types_by_name = dict((t.name, t) for t in cast(list[ir.ScalarType], util.filter_by_type(builtin_types, ir.ScalarType)))
