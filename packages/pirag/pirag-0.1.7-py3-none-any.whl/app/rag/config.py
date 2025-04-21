import argparse, os, sys
from pathlib import Path
from loguru import logger

# Logger format constants
LOG_TIME_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}Z"
LOG_FILE_FORMAT = f"{LOG_TIME_FORMAT} | {{level: <8}} | {{name}}:{{function}}:{{line}} - {{message}}"
LOG_CONSOLE_FORMAT_FULL = f"<green>{LOG_TIME_FORMAT}</green> | <level>{{level: <8}}</level> | <cyan>{{name}}</cyan>:<cyan>{{function}}</cyan>:<cyan>{{line}}</cyan> - <level>{{message}}</level>\n"
LOG_CONSOLE_FORMAT_SIMPLE = f"<green>{LOG_TIME_FORMAT}</green> | <level>{{level: <8}}</level> | <level>{{message}}</level>\n"

def setup_logger(log_level: str, log_dir: str):
    """Configure logger with specified level and outputs"""
    
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True, parents=True)
    
    logger.remove()
    
    # File handler
    logger.add(
        sink = log_dir / "{time:YYYYMMDD-HHmmss!UTC}Z.log",
        level = log_level,
        rotation = "100 MB",
        retention = 0,
        format = LOG_FILE_FORMAT,
        serialize = False,
        enqueue = True,
        backtrace = True,
        diagnose = True,
        catch = True
    )
    
    # Console handler
    logger.add(
        sink = sys.stderr,
        level = log_level,
        format = lambda record: LOG_CONSOLE_FORMAT_SIMPLE if record["level"].name == "INFO" else LOG_CONSOLE_FORMAT_FULL,
        colorize = True
    )


class EnvDefault(argparse.Action):
    """Custom argparse action that uses environment variables as defaults.

    This action extends the standard argparse.Action to support reading default values
    from environment variables. If the specified environment variable exists, its value
    will be used as the default value for the argument.

    For boolean flags (store_true/store_false), the environment variable is interpreted
    as a boolean value where 'true', '1', 'yes', or 'on' (case-insensitive) are
    considered True.

    Args:
        envvar (str): Name of the environment variable to use as default
        required (bool, optional): Whether the argument is required. Defaults to True.
            Note: If a default value is found in environment variables, required is set to False.
        default (Any, optional): Default value if environment variable is not set. Defaults to None.
        **kwargs: Additional arguments passed to argparse.Action

    Example:
        ```python
        parser.add_argument(
            '--log-level',
            envvar='LOG_LEVEL',
            help='Logging level',
            default='INFO',
            action=EnvDefault
        )
        ```

    Note:
        The help text is automatically updated to include the environment variable name.
    """
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if envvar and envvar in os.environ:
            env_value = os.environ[envvar]
            # Convert string environment variable to boolean
            if kwargs.get('nargs') is None and kwargs.get('const') is not None:  # store_true/store_false case
                default = env_value.lower() in ('true', '1', 'yes', 'on')
            else:
                default = env_value
            logger.debug(f"Using {envvar}={default} from environment")
        
        if envvar:
            kwargs["help"] += f" (envvar: {envvar})"
        
        if required and default:
            required = False
            
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)
        self.envvar = envvar

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values if values is not None else self.default)


# Top-level parser with common options
top_parser = argparse.ArgumentParser(add_help=False)

top_parser.add_argument(
    '-h', '--help',
    help = 'Show help message and exit',
    default = argparse.SUPPRESS,
    action = 'help',
)

top_parser.add_argument(
    '--env-file',
    envvar = 'ENV_FILE',
    help = 'Path to environment file',
    default = '.env',
    type = str,
    action = EnvDefault,
)

top_parser.add_argument(
    '--log-level',
    envvar = 'LOG_LEVEL',
    help = 'Logging level',
    default = 'INFO',
    type = lambda x: x.upper(),
    choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    required = False,
    action = EnvDefault,
)

top_parser.add_argument(
    '--log-dir',
    envvar = 'LOG_DIR',
    help = 'Path to log directory',
    default = '.pirag/logs',
    type = str,
    required = False,
    action = EnvDefault,
)

top_parser.add_argument(
    '--log-save',
    envvar = 'LOG_SAVE',
    help = 'Save log to file. If this flag is set, the log will be saved to the file specified in the `--log-path`.',
    default = False,
    const = True,
    nargs = 0,
    type = bool,
    required = False,
    action = EnvDefault,
)

common_parser = argparse.ArgumentParser(
    add_help = False,
)
