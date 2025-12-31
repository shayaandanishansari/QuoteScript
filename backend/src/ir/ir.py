
from ..common.models import ProgramNode, IR, FilterIR, SelectionIR


def to_ir(program: ProgramNode) -> IR:
    """Phase 4: Convert ProgramNode into a JSON-like IR structure."""
    filters_ir = []
    for key, flt in program.filters.items():
        filters_ir.append(
            FilterIR(
                field=key,
                value=flt.value,
                tag=flt.tag or "forgiving",
            )
        )
    sel = program.selection
    selection_ir = SelectionIR(top=sel.top, random=sel.random)
    return IR(filters=filters_ir, selection=selection_ir)
