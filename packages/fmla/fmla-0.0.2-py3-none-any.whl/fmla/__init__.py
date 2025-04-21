import random
from typing import List


def get_welcome_messages() -> List[str]:
    """Return list of welcome messages."""
    return [
        "Welcome to FMLA! Your career's last-ditch life preserver!",
        "PIP got you down? FMLA's got your back!",
        "Congrats on your 'development opportunity' (PIP). Time for FMLA!",
        "Remember: It's not procrastination, it's strategic career planning!",
    ]


def welcome() -> None:
    """Display random welcome message when package is imported."""
    messages = get_welcome_messages()
    print(random.choice(messages))


welcome()
