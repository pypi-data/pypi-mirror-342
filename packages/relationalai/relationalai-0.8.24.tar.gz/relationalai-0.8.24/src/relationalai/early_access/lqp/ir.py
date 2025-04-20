from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Union, Tuple, Sequence

# Tree representation of LQP. Each non-terminal (those with more than one
# option) is an "abstract" class and each terminal is its own class. All of
# which are children of LqpNode. PrimitiveType and PrimitiveValue are
# exceptions. PrimitiveType is an enum and PrimitiveValue is just a value.
# https://docs.google.com/document/d/1QXRU7zc1SUvYkyMCG0KZINZtFgzWsl9-XHxMssdXZzg/

@dataclass(frozen=True)
class LqpNode:
    # Return a string of this node in LLQP form.
    def to_llqp(self, indent_level=0):
        raise NotImplementedError(f"to_llqp not implemented for {type(self)}.")

# Declaration := Def | Loop
@dataclass(frozen=True)
class Declaration(LqpNode):
    pass

# TODO: this should probably be something else
@dataclass(frozen=True)
class LqpProgram(LqpNode):
    defs: list[Declaration]
    # name -> relation id
    outputs: list[Tuple[str, RelationId]]

    def to_llqp(self, indent_level=0):
        return Llqp.program_to_llqp(self, indent_level)

# Def(name::RelationId, body::Abstraction, attrs::Attribute[])
@dataclass(frozen=True)
class Def(Declaration):
    name: RelationId
    body: Abstraction
    attrs: Sequence[Attribute]

    def to_llqp(self, indent_level=0):
        return Llqp.def_to_llqp(self, indent_level)

# Loop(temporal_var::LoopIndex, inits::Def[], body::Declaration[])
@dataclass(frozen=True)
class Loop(Declaration):
    temporal_var: Var
    inits: Sequence[Def]
    body: Declaration

    def to_llqp(self, indent_level=0):
        return Llqp.loop_to_llqp(self, indent_level)

# Abstraction := Abstraction(vars::Var[], value::Formula)
@dataclass(frozen=True)
class Abstraction(LqpNode):
    vars: Sequence[Var]
    value: Formula

    def to_llqp(self, indent_level=0):
        return Llqp.abstraction_to_llqp(self, indent_level)

# Formula := Exists
#          | Reduce
#          | Conjunction
#          | Disjunction
#          | Not
#          | FFI
#          | Atom
#          | Pragma
#          | Primitive
#          | True
#          | False
#          | RelAtom
@dataclass(frozen=True)
class Formula(LqpNode):
    pass

# Exists(vars::Var[], value::Formula)
@dataclass(frozen=True)
class Exists(Formula):
    vars: Sequence[Var]
    value: Formula

    def to_llqp(self, indent_level=0):
        return Llqp.exists_to_llqp(self, indent_level)

# Reduce(op::Abstraction, body::Abstraction, terms::Term[])
@dataclass(frozen=True)
class Reduce(Formula):
    op: Abstraction
    body: Abstraction
    terms: Sequence[Term]

    def to_llqp(self, indent_level=0):
        return Llqp.reduce_to_llqp(self, indent_level)

# Conjunction(args::Formula[])
@dataclass(frozen=True)
class Conjunction(Formula):
    args: Sequence[Formula]

    def to_llqp(self, indent_level=0):
        return Llqp.conjunction_to_llqp(self, indent_level)

# Disjunction(args::Formula[])
@dataclass(frozen=True)
class Disjunction(Formula):
    args: Sequence[Formula]

    def to_llqp(self, indent_level=0):
        return Llqp.disjunction_to_llqp(self, indent_level)

# Not(arg::Formula)
@dataclass(frozen=True)
class Not(Formula):
    arg: Formula

    def to_llqp(self, indent_level=0):
        return Llqp.not_to_llqp(self, indent_level)

# FFI(name::Symbol, args::Abstraction[], terms::Term[])
@dataclass(frozen=True)
class Ffi(Formula):
    name: str
    args: Sequence[Abstraction]
    terms: Sequence[Term]

    def to_llqp(self, indent_level=0):
        return Llqp.ffi_to_llqp(self, indent_level)

# Atom(name::RelationId, terms::Term[])
@dataclass(frozen=True)
class Atom(Formula):
    name: RelationId
    terms: Sequence[Term]

    def to_llqp(self, indent_level=0):
        return Llqp.atom_to_llqp(self, indent_level)

# Pragma(name::Symbol, terms::Term[])
@dataclass(frozen=True)
class Pragma(Formula):
    name: str
    terms: Sequence[Term]

    def to_llqp(self, indent_level=0):
        return Llqp.pragma_to_llqp(self, indent_level)

# Primitive(name::Symbol, terms::Term[])
@dataclass(frozen=True)
class Primitive(Formula):
    name: str
    terms: Sequence[Term]

    def to_llqp(self, indent_level=0):
        return Llqp.primitive_to_llqp(self, indent_level)

# True()
@dataclass(frozen=True)
class JustTrue(Formula):
    def to_llqp(self, indent_level=0):
        return Llqp.true_to_llqp(self, indent_level)

# False()
@dataclass(frozen=True)
class JustFalse(Formula):
    def to_llqp(self, indent_level=0):
        return Llqp.false_to_llqp(self, indent_level)

# RelAtom(sig::RelationSig, terms::Term[])
@dataclass(frozen=True)
class RelAtom(Formula):
    sig: RelationSig
    terms: Sequence[Term]

    def to_llqp(self, indent_level=0):
        return Llqp.rel_atom_to_llqp(self, indent_level)

# Term := Var | Constant
@dataclass(frozen=True)
class Term(LqpNode):
    pass

# Var(name::Symbol, type::PrimitiveType)
@dataclass(frozen=True)
class Var(Term):
    name: str
    type: PrimitiveType

    def to_llqp(self, indent_level=0):
        return Llqp.var_to_llqp(self, indent_level)

# Constant(value::PrimitiveValue)
@dataclass(frozen=True)
class Constant(Term):
    value: PrimitiveValue

    def to_llqp(self, indent_level=0):
        return Llqp.constant_to_llqp(self, indent_level)

# Attribute := Attribute(name::Symbol, args::Constant[])
@dataclass(frozen=True)
class Attribute(LqpNode):
    name: str
    args: Sequence[Constant]

    def to_llqp(self, indent_level=0):
        return Llqp.attribute_to_llqp(self, indent_level)

# RelationId := RelationId(id::UInt128)
@dataclass(frozen=True)
class RelationId(LqpNode):
    # We use a catchall int here to represent the uint128 as it is difficult
    # to do so in Python without external packages. We check the value in
    # __post_init__.
    id: int

    def __post_init__(self):
        if self.id < 0 or self.id > 0xffffffffffffffffffffffffffffffff:
            raise ValueError(
                "RelationId constructed with out of range (UInt128) number: {}"
                    .format(self.id)
            )

    def to_llqp(self, indent_level=0):
        return Llqp.relation_id_to_llqp(self, indent_level)

# RelationSig := RelationSig(name::Symbol, types::PrimitiveType[])
@dataclass(frozen=True)
class RelationSig(LqpNode):
    name: str
    types: Sequence[PrimitiveType]

    def to_llqp(self, indent_level=0):
        return Llqp.relation_sig_to_llqp(self, indent_level)

# PrimitiveType := STRING | DECIMAL | INT | FLOAT | HASH
# TODO: we don't know what types we're supporting yet.
class PrimitiveType(Enum):
    # TODO: get rid of this oen maybe?
    UNKNOWN = 0
    STRING = 1
    INT = 2
    FLOAT = 3

    def to_llqp(self, indent_level=0):
        return Llqp.primitive_type_to_llqp(self, indent_level)

# PrimitiveValue := string | decimal | int | float | hash
# TODO: we don't know what types we're supporting yet.
PrimitiveValue = Union[str, int, float]

class Llqp:
    # Single INDentation.
    SIND = "    "

    # String of level indentations for LLQP.
    @staticmethod
    def indentation(level: int):
        return Llqp.SIND * level

    # Call .to_llqp on all nodes, each of which with indent_level, separating them
    # by delim.
    @staticmethod
    def list_to_llqp(nodes: Sequence[LqpNode], indent_level: int, delim: str):
        return delim.join(map(lambda n: n.to_llqp(indent_level), nodes))

    # Produces "(terms term1 term2 ...)" (all on one line) indented at indent_level.
    @staticmethod
    def terms_to_llqp(terms: Sequence[Term], indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        if len(terms) == 0:
            llqp = ind + "(terms)"
        else:
            llqp = ind + "(terms " + Llqp.list_to_llqp(terms, 0, " ") + ")"

        return llqp

    ## .to_llqp implementations.

    @staticmethod
    def def_to_llqp(node: Def, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(def " + node.name.to_llqp(0) + "\n"
        llqp += node.body.to_llqp(indent_level + 1) + "\n"
        if len(node.attrs) == 0:
            llqp += ind + Llqp.SIND + "(attrs) ;; no attrs" + "\n" + ind + ")"
        else:
            llqp += ind + Llqp.SIND + "(attrs" + "\n"
            llqp += Llqp.list_to_llqp(node.attrs, indent_level + 2, "\n") + "\n"
            llqp += ind + Llqp.SIND + ")" + ")"

        return llqp

    @staticmethod
    def loop_to_llqp(node: Loop, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(loop" + node.temporal_var.to_llqp(0) + "\n"
        llqp += ind + Llqp.SIND + "(inits" + "\n"
        llqp += Llqp.list_to_llqp(node.inits, indent_level + 2, "\n") + "\n"
        llqp += ind + Llqp.SIND + ")" + "\n"
        llqp += ind + Llqp.SIND + "(body" + "\n"
        llqp += node.body.to_llqp(indent_level + 2) + "\n"
        llqp += ind + Llqp.SIND + ")" + ")"

        return llqp

    @staticmethod
    def abstraction_to_llqp(node: Abstraction, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "([" + Llqp.list_to_llqp(node.vars, 0, ", ") + "]" + "\n"
        llqp += node.value.to_llqp(indent_level + 1) + ")"

        return llqp

    @staticmethod
    def exists_to_llqp(node: Exists, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(exists [" + Llqp.list_to_llqp(node.vars, 0, ", ") + "]" + "\n"
        llqp += node.value.to_llqp(indent_level + 1) + ")"

        return llqp

    @staticmethod
    def reduce_to_llqp(node: Reduce, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(reduce" + " " + "\n"
        llqp += node.op.to_llqp(indent_level + 1) + "\n"
        llqp += node.body.to_llqp(indent_level + 1) + "\n"
        llqp += Llqp.terms_to_llqp(node.terms, indent_level + 1) + ")"

        return llqp

    @staticmethod
    def conjunction_to_llqp(node: Conjunction, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(and" + "\n"
        llqp += Llqp.list_to_llqp(node.args, indent_level + 1, "\n") + ")"

        return llqp

    @staticmethod
    def disjunction_to_llqp(node: Disjunction, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(or" + "\n"
        llqp += Llqp.list_to_llqp(node.args, indent_level + 1, "\n") + ")"

        return llqp

    @staticmethod
    def not_to_llqp(node: Not, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(not" + "\n"
        llqp += node.arg.to_llqp(indent_level + 1) + ")"

        return llqp

    @staticmethod
    def ffi_to_llqp(node: Ffi, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind + "(ffi" + " " + ":" + node.name + "\n"
        llqp += ind + Llqp.SIND + "(args" + "\n"
        llqp += Llqp.list_to_llqp(node.args, indent_level + 2, "\n") + "\n"
        llqp += ind + Llqp.SIND + ")" + "\n"
        llqp += Llqp.terms_to_llqp(node.terms, indent_level + 1) + ")"

    @staticmethod
    def atom_to_llqp(node: Atom, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return f"{ind}(atom {node.name.to_llqp(0)} {Llqp.list_to_llqp(node.terms, 0, ' ')})"

    @staticmethod
    def pragma_to_llqp(node: Pragma, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return f"{ind}(pragma :{node.name} {Llqp.terms_to_llqp(node.terms, 0)})"

    @staticmethod
    def primitive_to_llqp(node: Primitive, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return f"{ind}(primitive :{node.name} {Llqp.list_to_llqp(node.terms, 0, ' ')})"

    @staticmethod
    def true_to_llqp(node: JustTrue, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return ind + "(true)"

    @staticmethod
    def false_to_llqp(node: JustFalse, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return ind + "(false)"

    @staticmethod
    def rel_atom_to_llqp(node: RelAtom, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return f"{ind}(relatom {node.sig.to_llqp(0)} {Llqp.list_to_llqp(node.terms, 0, ' ')})"

    @staticmethod
    def var_to_llqp(node: Var, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return ind + node.name + "::" + node.type.to_llqp(0)

    @staticmethod
    def constant_to_llqp(node: Constant, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind
        if isinstance(node.value, str):
            llqp += "\"" + node.value + "\""
        else:
            # suffices to just dump the value?
            llqp += str(node.value)

        return llqp

    @staticmethod
    def attribute_to_llqp(node: Attribute, indent_level: int):
        ind = Llqp.indentation(indent_level)

        llqp = ""
        llqp += ind
        llqp += "(attribute" + " "
        llqp += ":" + node.name + " "
        if len(node.args) == 0:
            llqp += "(args)"
        else:
            llqp += "(args" + " "
            llqp += Llqp.list_to_llqp(node.args, 0, " ")
            llqp += ")"
        llqp += ")"

        return llqp

    @staticmethod
    def relation_id_to_llqp(node: RelationId, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return f"{ind}:{str(node.id)}"

    @staticmethod
    def relation_sig_to_llqp(node: RelationSig, indent_level: int):
        ind = Llqp.indentation(indent_level)
        llqp = ""
        llqp += ind
        llqp += "(sig" + " "
        llqp += ":" + node.name
        for type in node.types:
            llqp += "/" + type.to_llqp(0)
        llqp += ")"

        return llqp

    @staticmethod
    def primitive_type_to_llqp(node: PrimitiveType, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return ind + node.name

    @staticmethod
    def program_to_llqp(node: LqpProgram, indent_level: int):
        # TODO: is this true? and in general for the other things can they be missing?
        assert len(node.defs) > 0, "LqpProgram must have at least one def."
        reads_portion = ""
        if len(node.outputs) == 0:
            reads_portion += _raw_text("(reads) ;; no outputs", indent_level + 2) + "\n"
        else:
            reads_portion += _raw_text("(reads\n", indent_level + 2)

            for (name, rel_id) in node.outputs:
                reads_portion +=\
                    f"{Llqp.indentation(indent_level + 3)}" +\
                    f"({name} " +\
                    f"{Llqp.relation_id_to_llqp(rel_id, 0)}" +\
                    ")\n"

            reads_portion += _raw_text(")\n", indent_level + 2)

        delim = "\n\n"
        writes_portion = f"{Llqp.list_to_llqp(node.defs, indent_level + 5, delim)}\n"


        return\
        _raw_text("(transaction\n", indent_level) +\
        _raw_text("(epoch\n", indent_level + 1) +\
        _raw_text("(local_writes\n", indent_level + 2) +\
        _raw_text("(define\n", indent_level + 3) +\
        _raw_text("(fragment :f1\n", indent_level + 4) +\
        writes_portion +\
        _raw_text(")\n", indent_level + 4) +\
        _raw_text(")\n", indent_level + 3) +\
        _raw_text(")\n", indent_level + 2) +\
        "\n" +\
        reads_portion +\
        _raw_text(")\n", indent_level + 1) +\
        _raw_text(")\n", indent_level)

def _raw_text(txt: str, indent_level: int):
        ind = Llqp.indentation(indent_level)
        return f"{ind}{txt}"
