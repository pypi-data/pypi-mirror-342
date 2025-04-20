"""
A simple metamodel for Rel.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from io import StringIO
from typing import Optional, Tuple, Union as PyUnion
from relationalai.early_access.rel import rel_utils
from relationalai.early_access.metamodel.util import Printer as BasePrinter

@dataclass(frozen=True)
class Node:
    def __str__(self):
        return to_string(self)

    @property
    def kind(self):
        return self.__class__.__name__.lower()

#--------------------------------------------------
# Top level program and declarations
#--------------------------------------------------

@dataclass(frozen=True)
class Program(Node):
    # top-level declarations
    declarations: Tuple[PyUnion[Declare, Def], ...]

@dataclass(frozen=True)
class Declare(Node):
    """ declare $premise [requires $requires] """
    premise: Expr
    requires: Optional[Expr]
    annotations: Tuple[Annotation, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class Def(Node):
    """ def $name($params) { $body } """
    name: str
    params: Tuple[PyUnion[Var, Primitive, MetaValue], ...]
    body: Expr
    annotations: Tuple[Annotation, ...] = field(default_factory=tuple)

#--------------------------------------------------
# Primitives, Annotations
#--------------------------------------------------

Primitive = PyUnion[str, int, float, bool]

@dataclass(frozen=True)
class Annotation(Node):
    """ @$name($args) """
    name: str
    args: Tuple[PyUnion[Primitive, MetaValue], ...]


#--------------------------------------------------
# Expr
#--------------------------------------------------

@dataclass(frozen=True)
class CompositeExpr(Node):
    pass

Expr = PyUnion[Primitive, CompositeExpr]

@dataclass(frozen=True)
class MetaValue(CompositeExpr):
    """ #$value """
    value: Primitive

@dataclass(frozen=True)
class Var(CompositeExpr):
    """ $name[...] [in $type] """
    name: str
    varargs: bool = False
    type: Optional[str] = None

@dataclass(frozen=True)
class Identifier(CompositeExpr):
    """ $name

    Used to declare a relation by name or to refer to a relation (e.g. Int, String)
    """
    name: str

@dataclass(frozen=True)
class Atom(CompositeExpr):
    """ $expr($args)

    Represents atoms like identifier($name)($args) as well as literal relations
    relations like {(:a, Int, 1)}(x...)
    """
    expr: Expr
    args: Tuple[Expr, ...]

def atom(name: str, args: Tuple[Expr, ...]):
    """ Helper to create a Atom where expression is an identifier. """
    return Atom(Identifier(name), args)

@dataclass(frozen=True)
class RelationalAbstraction(CompositeExpr):
    """ ($head): $body """
    head: Tuple[Expr, ...]
    body: Expr

@dataclass(frozen=True)
class And(CompositeExpr):
    """ $body[0] and $body[1] ... and $body[n] """
    body: Tuple[Expr, ...]

@dataclass(frozen=True)
class Or(CompositeExpr):
    """ $body[0] or $body[1] ... or $body[n] """
    body: Tuple[Expr, ...]

@dataclass(frozen=True)
class Exists(CompositeExpr):
    """ exists(($vars) | $body ) """
    vars: Tuple[Var, ...]
    body: Expr

@dataclass(frozen=True)
class ForAll(CompositeExpr):
    """ forall(($vars) | $body ) """
    vars: Tuple[Var, ...]
    body: Expr

@dataclass(frozen=True)
class Not(CompositeExpr):
    """ not ( $body ) """
    body: Expr

@dataclass(frozen=True)
class BinaryExpr(CompositeExpr):
    """ $lhs $op $rhs """
    lhs: Expr
    op: str
    rhs: Expr

@dataclass(frozen=True)
class Product(CompositeExpr):
    """ ($body[0] , $body[1] ... , $body[n]) """
    body: Tuple[Expr, ...]

@dataclass(frozen=True)
class Union(CompositeExpr):
    """ {$body[0] ; $body[1] ... ; $body[n]} """
    body: Tuple[Expr, ...]



#--------------------------------------------------
# Printer
#--------------------------------------------------

infix = ["+", "-", "*", "/", "%", "=", "!=", "<", "<=", ">", ">="]

def to_string(node) -> str:
    io = StringIO()
    Printer(io).print_node(node, 0)
    return io.getvalue()

@dataclass(frozen=True)
class Printer(BasePrinter):

    def _join(self, args, sep=', ', indent=0):
        for i, s in enumerate(args):
            if i != 0:
                if indent != 0:
                    self._print(sep.rstrip())
                    self._nl()
                else:
                    self._print(sep)
            self.print_node(s, indent)

    def _print_value(self, value):
        if isinstance(value, tuple):
            for i, v in enumerate(value):
                if i != 0:
                    self._print(", ")
                self._print_value(v)
        elif isinstance(value, str):
            self._print(f"\"{value}\"")
        elif isinstance(value, bool):
            self._print(str(value).lower())
        else:
            self._print(str(value))

    def print_node(self, node, indent=0) -> None:
        #--------------------------------------------------
        # Top level program and declarations
        #--------------------------------------------------
        if isinstance(node, Program):
            for d in node.declarations:
                self.print_node(d, indent)
                self._nl()

        elif isinstance(node, Declare):
            for anno in node.annotations:
                self.print_node(anno, indent)
                self._nl()
            self._indent_print(indent, f"declare {node.premise}")
            if node.requires:
                self._print(" requires ")
                self.print_node(node.requires, 0)
            self._nl()

        elif isinstance(node, Def):
            for anno in node.annotations:
                self.print_node(anno, indent)
                self._nl()
            self._indent_print(indent, f"def {node.name}")
            if node.params:
                self._print("(")
                self._join(node.params)
                self._print("):")
                self._nl()
            self.print_node(node.body, indent+1)
            self._nl()

        #--------------------------------------------------
        # Primitives, Annotations
        #--------------------------------------------------
        elif isinstance(node, (str, int, float, bool, tuple)):
            self._print_value(node)

        elif isinstance(node, Annotation):
            self._indent_print(indent, f"@{node.name}")
            if node.args:
                self._print("(")
                self._join(node.args)
                self._print(")")


        #--------------------------------------------------
        # Expr
        #--------------------------------------------------

        elif isinstance(node, MetaValue):
            if isinstance(node.value, str):
                self._print(":")
            else:
                self._print("#")
            self._print_value(node.value)

        elif isinstance(node, Var):
            self._indent_print(indent, f"{node.name}")
            if node.varargs:
                self._print("...")
            if node.type and node.type != "Any":
                self._print(f" in {node.type}")

        elif isinstance(node, Identifier):
            self._indent_print(indent, f"{node.name}")

        elif isinstance(node, Atom):
            if isinstance(node.expr, Identifier) and node.expr.name in infix:
                # deal with the 3 kinds of infix operators
                if len(node.args) == 1:
                    self.print_node(node.expr, indent)
                    self.print_node(node.args[0])
                elif len(node.args) == 2:
                    self.print_node(node.args[0], indent)
                    self._print(" ")
                    self.print_node(node.expr)
                    self._print(" ")
                    self.print_node(node.args[1])
                elif len(node.args) == 3:
                    self.print_node(node.args[2], indent)
                    self._print(" = ")
                    self.print_node(node.args[0])
                    self._print(" ")
                    self.print_node(node.expr)
                    self._print(" ")
                    self.print_node(node.args[1])
                else:
                    raise NotImplementedError(f"emit_action: {node}")
            else:
                is_agg = False
                if isinstance(node.expr, Identifier):
                    self.print_node(node.expr, indent)
                    is_agg = node.expr.name in rel_utils.OPERATORS.values()
                else:
                    self._indent_print(indent, "{")
                    self.print_node(node.expr, indent)
                    self._print("}")
                self._print("(")
                if is_agg:
                    self._nl()
                    self._join(node.args, indent=indent+1)
                    self._nl()
                    self._indent_print(indent, ")")
                else:
                    self._join(node.args)
                    self._print(")")

        elif isinstance(node, RelationalAbstraction):
            if node.head:
                self._indent_print(indent, "{(")
                self._join(node.head)
                self._print("):")
                self._nl()
                self.print_node(node.body, indent+1)
                self._nl()
                self._indent_print(indent, "}")
            else:
                self.print_node(node.body, indent)

        elif isinstance(node, And):
            self._join(node.body, " and ", indent)

        elif isinstance(node, Or):
            self._join(node.body, " or ", indent)

        elif isinstance(node, Exists):
            self._indent_print(indent, "exists((")
            self._join(node.vars)
            self._print(") |")
            self._nl()
            self.print_node(node.body, indent+1)
            self._nl()
            self._indent_print(indent, ")")

        elif isinstance(node, ForAll):
            self._indent_print(indent, "forall((")
            self._join(node.vars)
            self._print(")| ")
            self.print_node(node.body)
            self._print(")")

        elif isinstance(node, Not):
            self._indent_print(indent, "not (")
            self.print_node(node.body)
            self._print(")")

        elif isinstance(node, BinaryExpr):
            self.print_node(node.lhs, indent)
            self._print(f" {node.op} ")
            self.print_node(node.rhs)

        elif isinstance(node, Product):
            self._indent_print(indent, "(")
            self._join(node.body, ", ")
            self._print(")")

        elif isinstance(node, Union):
            self._indent_print(indent, "{")
            self._join(node.body, " ; ")
            self._print("}")

        else:
            raise Exception(f"Missing implementation in Rel printer: {type(node)}")
