#--------------------------------------------------
# Compiler
#--------------------------------------------------

from typing import cast, Tuple, Sequence

from relationalai.early_access.metamodel import ir, compiler as c, builtins as rel_builtins
from relationalai.early_access.metamodel import types
from relationalai.early_access.lqp import ir as lqp
from relationalai.early_access.metamodel.rewrite import Splinter
from relationalai.early_access.metamodel.util import NameCache

import hashlib

# TODO: take rewrite out of rel it doesnt belong there
from relationalai.early_access.rel import rewrite

from dataclasses import field

class Compiler(c.Compiler):
    def __init__(self):
        # TODO: are these all needed from the Rel emitter?
        # TODO: should there be a pass to remove aliases from output?
        super().__init__([
            rewrite.Flatten(),

            # Adds missing existentials + splits multi-headed rules into single rules
            Splinter(),
        ])

    # TODO: what should return value be? string according to parents?
    def do_compile(self, model: ir.Model, options:dict={}) -> str:
        lqp_ir, debugging_ctx = Model2Lqp().to_lqp(model)
        lqp_str = lqp_ir.to_llqp()

        debug_str = ""
        if len(debugging_ctx.id_to_orig_name) > 0:
            debug_str += ";; Original names\n"

        for (rid, name) in debugging_ctx.id_to_orig_name.items():
            debug_str += ";; \t " + str(rid) + " -> `" + name + "`\n"

        if debug_str != "":
            lqp_str += "\n\n"
            lqp_str += ";; Debug information\n"
            lqp_str += ";; -----------------------\n"
            lqp_str += debug_str

        return lqp_str

class DebuggingCtx:
    """ Extra information only used for debugging. """
    def __init__(self, id_to_orig_name: dict[lqp.RelationId, str]):
       self.id_to_orig_name = id_to_orig_name

class Model2Lqp:
    """ Generates LQP IR from the model IR. """
    def __init__(self):
        # TODO: comment htese fields
        # TODO: should we have a pass to rename variables instead of this?
        self.var_name_cache: NameCache = field(default_factory=NameCache)
        self.id_to_orig_name: dict[lqp.RelationId, str] = field(default_factory=dict)
        self.output_ids: list[lqp.RelationId] = field(default_factory=list)

    """ Main access point. Converts the model IR to an LQP program. """
    def to_lqp(self, model: ir.Model) -> Tuple[lqp.LqpProgram, DebuggingCtx]:
        _assert_valid_input(model)
        self._reset_state()
        program = self._translate_to_program(model)
        debugging_ctx = DebuggingCtx(self.id_to_orig_name)
        return (program, debugging_ctx)


    def _reset_state(self):
        self.var_name_cache = NameCache()
        self.id_to_orig_name = {}
        self.output_ids = []

    def _translate_to_program(self, model: ir.Model) -> lqp.LqpProgram:
        decls: list[lqp.Declaration] = []
        outputs: list[Tuple[str, lqp.RelationId]] = []

        # LQP only accepts logical tasks
        # These are asserted at init time
        root = cast(ir.Logical, model.root)
        assert len(root.body) >= 1

        for subtask in root.body:
            # TODO: when do we get more than one?
            child_l = cast(ir.Logical, subtask)
            decl = self._translate_to_decl(child_l)
            decls.append(decl)

        for output_id in self.output_ids:
            assert isinstance(output_id, lqp.RelationId)
            outputs.append(("output", output_id))

        assert len(outputs) >= 1
        return lqp.LqpProgram(decls, outputs)

    def _translate_to_decl(self, rule: ir.Logical) -> lqp.Declaration:
        outputs = []
        updates = []
        body_tasks = []
        aggregates = []

        for task in rule.body:
            if isinstance(task, ir.Output):
                outputs.append(task)
            elif isinstance(task, ir.Lookup):
                body_tasks.append(task)
            elif isinstance(task, ir.Logical):
                body_tasks.append(task)
            elif isinstance(task, ir.Exists):
                body_tasks.append(task)
            elif isinstance(task, ir.Aggregate):
                aggregates.append(task)
            elif isinstance(task, ir.Update):
                updates.append(task)
            else:
                raise NotImplementedError(f"Unknown task type: {type(task)}")

        assert len(aggregates) == 0, "unsupported aggregates yet"

        conjuncts = []
        for task in body_tasks:
            conjunct = self._translate_to_formula(task)
            conjuncts.append(conjunct)
        body = lqp.Conjunction(conjuncts) if len(conjuncts) != 1 else conjuncts[0]

        # TODO: unifying all this?
        if len(outputs) > 0:
            assert len(outputs) == 1, "only one output supported at the moment"
            output = outputs[0]
            assert isinstance(output, ir.Output)
            output_vars = []
            for _, v in output.aliases:
                # TODO: we dont yet handle aliases
                assert isinstance(v, ir.Var)
                var = self._translate_to_var(v)
                output_vars.append(var)
            abstraction = lqp.Abstraction(output_vars, body)
            # TODO: is this correct? might need attrs tooo?
            rel_id = _gen_rel_id(abstraction)
            self.output_ids.append(rel_id)
            return lqp.Def(rel_id, abstraction, [])

        assert len(updates) == 1, "only one update supported at the moment"
        update = updates[0]
        assert isinstance(update, ir.Update)
        effect = update.effect
        assert effect == ir.Effect.derive, "only derive supported at the moment"

        args = []
        for var in update.args:
            assert isinstance(var, ir.Var)
            args.append(self._translate_to_var(var))

        abstraction = lqp.Abstraction(args, body)
        # TODO: is this correct? might need attrs tooo?
        rel_id = _gen_rel_id(abstraction)
        # TODO: attrs?
        self.id_to_orig_name[rel_id] = update.relation.name
        return lqp.Def(rel_id, abstraction, [])

    def _translate_to_formula(self, task: ir.Task) -> lqp.Formula:
        if isinstance(task, ir.Logical):
            conjuncts = []
            for child in task.body:
                conjunct = self._translate_to_formula(child)
                conjuncts.append(conjunct)
            return lqp.Conjunction(conjuncts)
        elif isinstance(task, ir.Lookup):
            return self._translate_to_atom(task)
        elif isinstance(task, ir.Exists):
            lqp_vars = []
            for var in task.vars:
                lqp_vars.append(self._translate_to_var(var))
            formula = self._translate_to_formula(task.task)
            return lqp.Exists(lqp_vars, formula)
        else:
            raise NotImplementedError(f"Unknown task type (formula): {type(task)}")

    def _translate_to_var(self, var: ir.Var) -> lqp.Var:
        name = self.var_name_cache.get_name(var.id, var.name)
        t = type_from_var(var)
        return lqp.Var(name, t)

    def _translate_to_atom(self, task: ir.Lookup) -> lqp.Formula:
        # TODO: want signature not name
        rel_name = task.relation.name
        assert isinstance(rel_name, str)
        terms = []
        sig_types = []
        for arg in task.args:
            if isinstance(arg, lqp.PrimitiveValue):
                term = lqp.Constant(arg)
                terms.append(term)
                t = type_from_constant(arg)
                sig_types.append(t)
                continue
            assert isinstance(arg, ir.Var)
            var = self._translate_to_var(arg)
            terms.append(var)
            sig_types.append(var.type)

        # TODO: wrong
        if rel_builtins.is_builtin(task.relation):
            return self._translate_builtin_to_primitive(task.relation, terms)

        return lqp.RelAtom(lqp.RelationSig(rel_name, sig_types), terms)

    def _translate_builtin_to_primitive(self, relation: ir.Relation, terms: list[lqp.Term]) -> lqp.Primitive:
        lqp_name = self._name_to_lqp_name(relation.name)
        return lqp.Primitive(lqp_name, terms)

    def _name_to_lqp_name(self, name: str) -> str:
        # TODO: do these proprly
        if name == "+":
            return "rel_primitive_add"
        elif name == "-":
            return "rel_primitive_subtract"
        elif name == "*":
            return "rel_primitive_multiply"
        elif name == "=":
            return "rel_primitive_eq"
        elif name == "<=":
            return "rel_primitive_lt_eq"
        else:
            raise NotImplementedError(f"missing primitive case: {name}")

def _gen_rel_id(abstr: lqp.Abstraction) -> lqp.RelationId:
    return lqp.RelationId(hash_to_uint128(_lqp_hash(abstr)))

# TODO: this is NOT a good hash its just to get things working for now to get
# a stable id.
def _lqp_hash(node: lqp.LqpNode) -> int:
    if isinstance(node, lqp.Abstraction):
        h1 = _lqp_hash_list(node.vars)
        h2 = _lqp_hash(node.value)
        return _lqp_hash_fn((h1, h2))
    elif isinstance(node, lqp.Exists):
        h1 = _lqp_hash_list(node.vars)
        h2 = _lqp_hash(node.value)
        return _lqp_hash_fn((h1, h2))
    elif isinstance(node, lqp.Conjunction):
        h1 = _lqp_hash_list(node.args)
        return _lqp_hash_fn((h1,))
    elif isinstance(node, lqp.Var):
        return _lqp_hash_fn((node.name, node.type))
    elif isinstance(node, lqp.Constant):
        return _lqp_hash_fn((node.value,))
    elif isinstance(node, lqp.RelAtom):
        h1 = _lqp_hash(node.sig)
        h2 = _lqp_hash_list(node.terms)
        return _lqp_hash_fn((h1, h2))
    elif isinstance(node, lqp.RelationSig):
        return _lqp_hash_fn((node.name, tuple(node.types)))
    elif isinstance(node, lqp.Primitive):
        h1 = _lqp_hash_fn(node.name)
        h2 = _lqp_hash_list(node.terms)
        return _lqp_hash_fn((h1, h2))
    else:
        raise NotImplementedError(f"Unsupported LQP node type: {type(node)}")

# TODO: this is NOT a good hash its just to get things working for now to get
# a stable id.
def _lqp_hash_fn(node) -> int:
    return int.from_bytes(hashlib.sha256(str(node).encode()).digest(), byteorder='big', signed=False)

def _lqp_hash_list(node: Sequence[lqp.LqpNode]) -> int:
    hashes = [_lqp_hash(n) for n in node]
    return hash(tuple(hashes))

def hash_to_uint128(h: int) -> int:
    return h % (2**128)  # Ensure it's within the 128-bit range

# Preconditions
def _assert_valid_input(model: ir.Model) -> bool:
    # TODO: flesh this out more?
    _assert_root_is_logical(model.root)
    return True

def _assert_root_is_logical(task: ir.Task) -> bool:
    assert isinstance(task, ir.Logical), f"expected logical task, got {type(task)}"
    assert len(task.body) >= 1, f"expected at least one task, got {len(task.body)}"
    for subtask in task.body:
        # TODO: assert what subtasks should look like
        # TODO: where can aggregates exist? only on top level?
        assert isinstance(subtask, ir.Logical), f"expected logical task, got {type(subtask)}"

    return True

def type_from_var(arg: ir.Var) -> lqp.PrimitiveType:
    assert isinstance(arg, ir.Var)
    assert isinstance(arg.type, ir.ScalarType)
    if types.is_builtin(arg.type):
        # TODO: just ocompare to types.py
        if arg.type.name == "Int":
            return lqp.PrimitiveType.INT
        else:
            # TODO: fix this
            assert arg.type.name == "Any" or arg.type.name == "Number", f"Unknown type: {arg.type.name}"
            return lqp.PrimitiveType.UNKNOWN
    else:
        return lqp.PrimitiveType.UNKNOWN

def type_from_constant(arg: lqp.PrimitiveValue) -> lqp.PrimitiveType:
    if isinstance(arg, int):
        return lqp.PrimitiveType.INT
    elif isinstance(arg, float):
        return lqp.PrimitiveType.FLOAT
    elif isinstance(arg, str):
        return lqp.PrimitiveType.STRING
    else:
        raise NotImplementedError(f"Unknown constant type: {type(arg)}")
