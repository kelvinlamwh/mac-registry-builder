import sys
import logging
from datetime import datetime
from typing import Annotated, Optional
from pathlib import Path

import typer
from loguru import logger
import uvicorn

from logging_utils import LoguruInterceptHandler, LOGURU_ARGS, UVICORN_LOGGING_CONFIG
from endpoints import THE_REGISTER, api as FastAPIApp
from arp import get_hwaddr

cli = typer.Typer()

def log_setup(verbose: bool) -> None:
    logger.remove()
    logger.add(sys.stderr, backtrace = False, diagnose = False, **LOGURU_ARGS, level = 'TRACE' if verbose else 'INFO')

    logging.basicConfig(handlers = [LoguruInterceptHandler()], level = 0, )
    logging.debug('std Logging rerouted to loguru')

    if not verbose:
        del UVICORN_LOGGING_CONFIG['loggers']['uvicorn.access']['handlers'][0]

@cli.command()
def entrypoint(
    port: Annotated[int, typer.Option(help="API Port", metavar="PORT")] = 5000,
    outfile: Annotated[Optional[Path], typer.Option(help="Register output", metavar="PATH")] = None,
    verbose: Annotated[bool, typer.Option('--verbose', '-v', help="More logging")] = False,
):
    log_setup(verbose)

    logger.debug('Most probable IP Address: [<cyan>{}</>] at [<green>{}</>]', *get_hwaddr())
    logger.trace('ts=[{}], handing over to uvicorn',
        datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f %p %:z').strip()
    )

    uvicorn.run(
        FastAPIApp,
        host = '0.0.0.0', port = port,
        log_level = logging.INFO, log_config = UVICORN_LOGGING_CONFIG
    )

    register_out = ('{}\t{}\t{}'.format(*entry) for entry in THE_REGISTER)
    logger.success('Final MAC register:\n\n{}', '\n'.join(register_out))

    # Dumping
    if outfile is None:
        logger.debug('No output file specified, skipping')
        return
    try:
        with outfile.open('wx', encoding='utf-8') as dump_dst:
            dump_dst.writelines(register_out)
        logger.success('Dump complete')
    except Exception as e:
        logger.opt(exception = e).error(f'Failed to dump registry')


if __name__ == "__main__":
    cli()
