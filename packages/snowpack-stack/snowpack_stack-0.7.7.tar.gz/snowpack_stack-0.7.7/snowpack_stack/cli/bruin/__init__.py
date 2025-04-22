"""Bruin-specific CLI commands."""


def run_all() -> int:
    """Run all Bruin commands.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    from snowpack_stack.cli.bruin.sql_generator import SqlGeneratorCommand
    from snowpack_stack.cli.bruin.yaml_generator import YamlGeneratorCommand

    commands = [
        YamlGeneratorCommand,
        SqlGeneratorCommand,
    ]

    exit_code = 0
    for cmd_class in commands:
        result = cmd_class.run()
        if result != 0:
            exit_code = result

    return exit_code
