import llm
import logging
import os

is_setup = False


def ensure_logging():
    global is_setup
    if not os.environ.get("LLM_LOGGING_DEBUG"):
        return
    if is_setup:
        return
    is_setup = True
    logging.basicConfig(
        format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )


@llm.hookimpl
def register_models():
    ensure_logging()
