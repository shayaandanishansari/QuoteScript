
from ..common.models import IR, FilterIR


def optimize(ir: IR) -> IR:
    """Phase 5: Basic optimisation.

    - Trim whitespace from filter values.
    - Drop filters whose values become empty.
    """
    new_filters = []
    for f in ir.filters:
        value = f.value.strip()
        if not value:
            continue
        new_filters.append(
            FilterIR(
                field=f.field,
                value=value,
                tag=f.tag.lower(),
            )
        )
    ir.filters = new_filters
    return ir
