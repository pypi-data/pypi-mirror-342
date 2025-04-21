import logging
import sys
from typing import Annotated

# Removed torch import
import typer

# Use internal imports
from .app import Application
from .config import EnvConfig

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
        help="Random seed for reproducibility.",
    ),
]


def setup_logging(log_level_str: str):
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
        force=True,  # Override existing config
    )
    # Keep external libraries less verbose if needed
    logging.getLogger("pygame").setLevel(logging.WARNING)
    logging.info(f"Root logger level set to {logging.getLevelName(log_level)}")


def run_interactive_mode(mode: str, seed: int, log_level: str):
    """Runs the interactive application."""
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    logger.info(f"Running Triangle Engine in {mode.capitalize()} mode...")

    # --- UPDATED SEEDING (Removed Torch) ---
    try:
        import random

        import numpy as np

        random.seed(seed)
        # Use default_rng() for NumPy if available, otherwise skip NumPy seeding
        try:
            np.random.default_rng(seed)
            logger.debug("NumPy seeded using default_rng.")
        except AttributeError:
            logger.warning("np.random.default_rng not available. Skipping NumPy seed.")
        except ImportError:
            logger.warning("NumPy not found. Skipping NumPy seed.")

        # Removed torch.manual_seed(seed)
        logger.info(f"Set random seeds to {seed}")
    except ImportError:
        logger.warning("Could not import all libraries for full seeding.")
    except Exception as e:
        logger.error(f"Error setting seeds: {e}")
    # --- END UPDATED SEEDING ---

    # Validate EnvConfig
    try:
        _ = EnvConfig()
        logger.info("EnvConfig validated.")
    except Exception as e:
        logger.critical(f"EnvConfig validation failed: {e}", exc_info=True)
        sys.exit(1)

    try:
        app_instance = Application(mode=mode)
        app_instance.run()
    except ImportError as e:
        logger.error(f"Runtime ImportError: {e}")
        logger.error(
            "Please ensure all dependencies (including pygame) are installed for trianglengin."
        )
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unhandled error occurred: {e}", exc_info=True)
        sys.exit(1)

    logger.info("Exiting.")
    sys.exit(0)


@app.command()
def play(
    log_level: LogLevelOption = "INFO",
    seed: SeedOption = 42,
):
    """Run the game in interactive Play mode."""
    run_interactive_mode(mode="play", seed=seed, log_level=log_level)


@app.command()
def debug(
    log_level: LogLevelOption = "DEBUG",  # Default to DEBUG for debug mode
    seed: SeedOption = 42,
):
    """Run the game in interactive Debug mode."""
    run_interactive_mode(mode="debug", seed=seed, log_level=log_level)


if __name__ == "__main__":
    app()
