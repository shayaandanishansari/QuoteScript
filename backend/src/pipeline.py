
from .lexer.lexer import lex
from .parser.parser import parse
from .semantic.semantic import semantic_analysis
from .ir.ir import to_ir
from .optimizer.optimizer import optimize
from .executor.executor import execute, print_output
from .common.errors import QuoteScriptError


def compile_and_run(source: str) -> None:
    """Run all phases on the given QuoteScript source and print results."""
    # Phase 1: Lexical analysis
    tokens = lex(source)

    # Phase 2: Syntax analysis
    program = parse(tokens)

    # Phase 3: Semantic analysis
    program = semantic_analysis(program)

    # Phase 4: IR generation
    ir = to_ir(program)

    # Phase 5: Optimisation
    ir = optimize(ir)

    # Phase 6: Execution / codegen
    rows = execute(ir)
    print_output(ir, rows)
