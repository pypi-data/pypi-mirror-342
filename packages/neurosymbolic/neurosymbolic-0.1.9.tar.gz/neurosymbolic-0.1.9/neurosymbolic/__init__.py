import argparse

from neurosymbolic.bashtool import BashTool
from neurosymbolic.z3tool import Z3Tool
from neurosymbolic.python_interpreter import PythonInterpreter
from langchain_community.tools import ReadFileTool, WriteFileTool

from .blocks import compute, cast

from pydantic import BaseModel, Field


class Answer(BaseModel):
    """Answer class for the neurosymbolic solver."""

    answer: int = Field(
        ...,
        description="The answer to the neurosymbolic solver's goal.",
        example="42",
    )


def main():
    """Simple neurosymbolic solver with bash/z3/read/write file capabilities."""
    parser = argparse.ArgumentParser(description="Neurosymbolic solver")
    parser.add_argument("goal", help="Goal for the neurosymbolic solver")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase output verbosity"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    user_input = args.goal
    verbose = args.verbose
    debug = args.debug

    toolbox = [
        BashTool(verbose=verbose),
        Z3Tool(verbose=verbose),
        ReadFileTool(verbose=verbose),
        WriteFileTool(verbose=verbose),
        PythonInterpreter(verbose=verbose),
    ]
    result, messages = compute(prompt=user_input, toolbox=toolbox, target_type=Answer)
    print(repr(result))
    if debug:
        for message in messages:
            print(message)


__all__ = ["main"]
