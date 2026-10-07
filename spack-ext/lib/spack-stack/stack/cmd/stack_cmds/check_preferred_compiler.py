from spack.extensions.stack.compiler_utils import check_preferred_compiler

description = "Check preferred compiler"
section = "spack-stack"
level = "long"


# Add potential arguments to check-preferred-compiler
def setup_preferred_compiler_parser(subparser):
    pass


def stack_check_preferred_compiler(parser, args):
    check_preferred_compiler()
