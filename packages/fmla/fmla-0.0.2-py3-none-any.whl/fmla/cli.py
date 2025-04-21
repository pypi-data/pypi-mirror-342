"""CLI for the FMLA package."""

import argparse
from typing import List, Optional


def get_pip_info() -> str:
    """Return information about PIP (Performance Improvement Plan)."""
    return (
        "PIP: Performance Improvement Plan\n"
        "\n"
        "A PIP is a formal document given to employees who are not\n"
        "meeting expectations. Often used as the first step in the\n"
        "termination process, it outlines:\n"
        "- Areas where performance is lacking\n"
        "- Specific goals to improve performance\n"
        "- Timeline for showing improvement\n"
        "- Consequences if improvement is not achieved\n"
        "\n"
        "While officially it's meant to help you improve, unofficially\n"
        "it's often the beginning of the end of your employment journey.\n"
        "But don't despair - that's where FMLA comes in!"
    )


def get_pip_guide() -> str:
    """Return guide on dealing with PIP mentally and FMLA information."""
    return (
        "Guide to Surviving a PIP and Using FMLA\n"
        "\n"
        "MENTAL STRATEGIES:\n"
        "1. Don't panic - a PIP doesn't automatically mean termination\n"
        "2. Read between the lines - understand if this is a genuine\n"
        "   improvement plan or just documentation for eventual termination\n"
        "3. Document everything - keep records of all your work and\n"
        "   communication\n"
        "4. Consider your options:\n"
        "   - Work to meet the goals (if they're actually achievable)\n"
        "   - Start looking for a new job (always a good idea when on a PIP)\n"
        "   - Explore FMLA options (see below)\n"
        "5. Protect your mental health - a PIP is stressful, take care of\n"
        "   yourself\n"
        "6. Remember: your worth is not defined by a corporate evaluation\n"
        "   process\n"
        "\n"
        "FMLA INFORMATION:\n"
        "FMLA: Family and Medical Leave Act\n"
        "\n"
        "FMLA provides eligible employees with job-protected leave for\n"
        "qualified medical and family reasons. When facing a PIP, FMLA\n"
        "might be your strategic timeout.\n"
        "\n"
        "Steps to the FMLA Route:\n"
        "\n"
        "1. Verify eligibility - typically you need to have worked for\n"
        "   your employer for at least 12 months and 1,250 hours in the\n"
        "   past year\n"
        "2. Consult with a healthcare provider about your stress, anxiety,\n"
        "   or other medical conditions that may qualify for FMLA\n"
        "3. Request FMLA paperwork from your HR department\n"
        "4. Have your healthcare provider complete the medical certification\n"
        "5. Submit your FMLA request - give 30 days notice when possible\n"
        "6. Use your leave time to:\n"
        "   - Focus on your health and well-being\n"
        "   - Update your resume and portfolio\n"
        "   - Network and explore new opportunities\n"
        "   - Develop new skills\n"
        "7. Return with a plan - either to meet your PIP or transition to a\n"
        "   new role\n"
        "\n"
        "Remember: FMLA is a legal right for eligible employees. Using it\n"
        "legitimately for health concerns is not fraudulent, even if the\n"
        "timing is convenient."
    )


def main(args: Optional[List[str]] = None) -> int:
    """Run the FMLA CLI."""
    parser = argparse.ArgumentParser(description="FMLA CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Info command
    subparsers.add_parser("info", help="Show information about PIP")

    # Guide command
    subparsers.add_parser(
        "guide", help="Show guide on dealing with PIP mentally and FMLA information"
    )

    parsed_args = parser.parse_args(args)

    if parsed_args.command == "info":
        print(get_pip_info())
    elif parsed_args.command == "guide":
        print(get_pip_guide())
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    main()
