# File: src/trianglengin/ui/cli.py
import logging
import random
import sys
from typing import Annotated

import numpy as np
import typer  # Now a required dependency

# Use absolute imports from core engine
from trianglengin.config import EnvConfig

# Import Application directly
from trianglengin.ui.app import Application

app = typer.Typer(
    name="trianglengin",
    help="Core Triangle Engine - Interactive Modes.",
    add_completion=False,
)

LogLevelOption = Annotated[
    str,
    typer.Option(
        "--log-level",
        "-l",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
        case_sensitive=False,
    ),
]

SeedOption = Annotated[
    int,
    typer.Option(
        "--seed",
        "-s",
        help="Random seed for C++ engine initialization.",
    ),
]


def setup_logging(log_level_str: str) -> None:
    """Configures root logger based on string level."""
    log_level_str = log_level_str.upper()
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = log_level_map.get(log_level_str, logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
    # Set pygame log level (pygame is now a required dependency)

    logging.getLogger("pygame").setLevel(logging.WARNING)
    logging.info(f"Root logger level set to {logging.getLevelName(log_level)}")


def run_interactive_mode(mode: str, seed: int, log_level: str) -> None:
    """Runs the interactive application."""
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    logger.info(f"Running Triangle Engine in {mode.capitalize()} mode...")

    # --- Seeding ---
    try:
        random.seed(seed)
        # Use modern NumPy seeding
        np.random.default_rng(seed)
        logger.info(
            f"Set Python random seed to {seed}. NumPy RNG initialized. C++ engine seeded separately."
        )
    except Exception as e:
        logger.error(f"Error setting Python/NumPy seeds: {e}")
    # --- End Seeding ---

    try:
        # Validate core EnvConfig
        _ = EnvConfig()
        logger.info("EnvConfig validated.")
    except Exception as e:
        logger.critical(f"EnvConfig validation failed: {e}", exc_info=True)
        sys.exit(1)

    try:
        # Application is part of the UI package
        app_instance = Application(mode=mode)
        app_instance.run()
    # Keep general exception handling
    except Exception as e:
        logger.critical(f"An unhandled error occurred: {e}", exc_info=True)
        sys.exit(1)

    logger.info("Exiting.")
    sys.exit(0)


@app.command()
def play(
    log_level: LogLevelOption = "INFO",
    seed: SeedOption = 42,
) -> None:
    """Run the game in interactive Play mode."""
    run_interactive_mode(mode="play", seed=seed, log_level=log_level)


@app.command()
def debug(
    log_level: LogLevelOption = "DEBUG",
    seed: SeedOption = 42,
) -> None:
    """Run the game in interactive Debug mode."""
    run_interactive_mode(mode="debug", seed=seed, log_level=log_level)


if __name__ == "__main__":
    app()
