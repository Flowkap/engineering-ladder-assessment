import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from datetime import datetime

# Configuration constants
SCORE_RANGE = (1, 5)
CHART_SIZE = (10, 10)
MAX_LEVELS = 5
COLORS = {'background': 'black', 'grid': 'white', 'plot': 'yellow'}
OUTPUT_DIR = 'out'

AXES_CONFIG = {
    'Enablement': {
        'levels': ['Operates', 'Curates', 'Orchestrates', 'Architects', 'Pioneers'],
        'descriptions': [
            'Uses AI agents and tools productively, understands output quality',
            'Selects appropriate tools/agents, defines constraints and guardrails',
            'Composes complex agent workflows, multiplies throughput',
            'Designs the technical enablement strategy for teams',
            'Creates new enablement paradigms, shapes how the organization works'
        ]
    },
    'System': {
        'levels': ['Comprehends', 'Designs', 'Owns', 'Evolves', 'Leads'],
        'descriptions': [
            'Understands existing system architectures and their trade-offs',
            'Designs systems (specifies rather than implements)',
            'Owns system health, detects degradation',
            'Drives evolution under changing requirements',
            'Leads architecture across team boundaries'
        ]
    },
    'People': {
        'levels': ['Learns', 'Supports', 'Mentors', 'Coordinates', 'Manages'],
        'descriptions': [
            'Learns from team members and receives guidance',
            'Provides support and guidance to team members',
            'Actively mentors and develops other engineers',
            'Coordinates across teams and stakeholders',
            'Manages people and teams effectively'
        ]
    },
    'Process': {
        'levels': ['Follows', 'Enforces', 'Challenges', 'Adjusts', 'Defines'],
        'descriptions': [
            'Follows established processes and procedures',
            'Ensures team adherence to processes',
            'Questions and improves existing processes',
            'Adapts processes to team and project needs',
            'Creates and defines new processes'
        ]
    },
    'Impact': {
        'levels': ['Task', 'Team', 'Domain', 'Organization', 'Industry'],
        'descriptions': [
            'Reliably delivers results within own scope',
            'Elevates the effectiveness of the entire team',
            'Sustainably shapes a domain',
            'Changes how the organization works',
            'Influences the industry'
        ]
    },
    'Product\nThinking': {
        'levels': ['Understands', 'Shapes', 'Drives', 'Strategizes', 'Visions'],
        'descriptions': [
            'Understands user needs behind tickets, asks "why"',
            'Actively shapes requirements, spots gaps and contradictions',
            'Drives product decisions independently, validates hypotheses',
            'Connects technical possibilities with business strategy',
            'Defines product vision at the intersection of technology and market'
        ]
    },
    'Judgement': {
        'levels': ['Executes', 'Evaluates', 'Challenges', 'Navigates', 'Calibrates'],
        'descriptions': [
            'Makes good decisions in well-defined situations',
            'Weighs trade-offs, identifies risks, decides under uncertainty',
            'Questions assumptions, identifies systemic risks',
            'Navigates complex, multi-dimensional decision spaces',
            'Calibrates decision frameworks for the organization'
        ]
    }
}


def setup_argument_parser():
    """Setup command line argument parser."""
    parser = argparse.ArgumentParser(
        description='Engineering Ladder Assessment - Generate a radar chart visualization '
                    'of engineering skills across 7 dimensions for the AI agent era.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode - you'll be prompted for scores
  python main.py -h                 # Show this help message

Assessment Dimensions:
  Enablement:       Ability to leverage AI agents, tools, and workflows effectively
  System:           System design, architecture, and ownership
  People:           Team collaboration and mentoring skills
  Process:          Process improvement and methodology skills
  Impact:           Scope and depth of measurable outcomes
  Product Thinking: Understanding user needs, shaping requirements, driving product decisions
  Judgement:        Quality of decisions under uncertainty and complexity

Each dimension is scored from 1-5 representing different capability levels.
The output is a radar chart saved as 'out/engineering_ladder_<timestamp>.png'.
        """)

    return parser


def validate_score(score_str, axis_name):
    """Validate a single score input."""
    try:
        score = float(score_str.strip())
        if not (SCORE_RANGE[0] <= score <= SCORE_RANGE[1]):
            raise ValueError(f"Score must be between {SCORE_RANGE[0]} and {SCORE_RANGE[1]}")
        return score
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"'{score_str}' is not a valid number")
        raise


def get_user_input():
    """Collect and validate user scores for each axis."""
    print("Engineering Ladder Assessment")
    print("=" * 40)
    print(f"Enter scores from {SCORE_RANGE[0]} to {SCORE_RANGE[1]} for each dimension.")
    print()

    scores = []
    for axis, config in AXES_CONFIG.items():
        display_name = axis.replace('\n', ' ')
        print(f"\n{display_name}:")
        print("-" * 40)
        for i, (level, desc) in enumerate(zip(config['levels'], config['descriptions']), 1):
            print(f"  {i} - {level}: {desc}")
        print()

        while True:
            try:
                user_input = input(f"Enter {display_name} score ({SCORE_RANGE[0]}-{SCORE_RANGE[1]}): ")
                if not user_input.strip():
                    print("Please enter a value")
                    continue

                score = validate_score(user_input, axis)
                scores.append(score)
                break

            except ValueError as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
                sys.exit(0)

    return scores


def assess_level(scores):
    """Assess engineering level based on scores."""
    avg = sum(scores) / len(scores)

    if avg < 1.5:
        level = "Junior"
        description = "You're at the beginning of your engineering journey, focusing on learning and growth."
    elif avg < 2.5:
        level = "Junior-ish"
        description = "You're progressing beyond junior, building foundations across multiple areas."
    elif avg < 3.0:
        level = "Mid-Level"
        description = "You're a solid mid-level engineer with growing expertise and influence."
    elif avg < 3.5:
        level = "Mid-Level-ish"
        description = "You're transitioning toward senior, showing leadership in several dimensions."
    elif avg < 4.0:
        level = "Senior"
        description = "You're operating at a senior level with strong skills across the board."
    elif avg < 4.5:
        level = "Senior-ish"
        description = "You're beyond senior, approaching staff/principal level impact."
    else:
        level = "Staff/Principal"
        description = "You're operating at staff or principal level with exceptional breadth and depth."

    return level, avg, description


def print_assessment(scores):
    """Print the level assessment summary."""
    level, avg, description = assess_level(scores)

    print("\n" + "=" * 40)
    print("ASSESSMENT SUMMARY")
    print("=" * 40)
    print(f"Average Score: {avg:.1f}/5")
    print(f"Level: {level}")
    print(f"\n{description}")
    print("=" * 40)


def create_output_directory():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def generate_filename():
    """Generate timestamped filename for the output chart."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIR, f"engineering_ladder_{timestamp}.png")


def create_radar_chart(scores):
    """Create and display the radar chart visualization."""
    num_vars = len(AXES_CONFIG)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Close the plot
    plot_values = scores + [scores[0]]
    plot_angles = angles + [angles[0]]

    # Get level assessment
    eng_level, avg, description = assess_level(scores)

    # Setup figure
    fig, ax = plt.subplots(figsize=CHART_SIZE, subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])

    # Configure axes
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(list(AXES_CONFIG.keys()), color=COLORS['grid'], fontsize=12)
    ax.set_rlabel_position(0)
    ax.yaxis.grid(False)

    frame_limit = MAX_LEVELS + 1
    plt.ylim(0, frame_limit)

    # Draw spider web grid
    for level in range(1, MAX_LEVELS + 1):
        grid_values = [level] * num_vars + [level]
        ax.plot(plot_angles, grid_values, color=COLORS['grid'],
                linewidth=0.5, linestyle='dashed')

    # Draw outer frame and radial lines
    frame_values = [frame_limit] * num_vars + [frame_limit]
    ax.plot(plot_angles, frame_values, color=COLORS['grid'], linewidth=1.0)

    for angle in angles:
        ax.plot([angle, angle], [0, frame_limit], color=COLORS['grid'], linewidth=0.5)

    # Add level labels
    for i, (axis, config) in enumerate(AXES_CONFIG.items()):
        for j, level_name in enumerate(config['levels']):
            ax.text(angles[i], j + 1, level_name, color=COLORS['grid'],
                    fontsize=8, ha='center', va='center')

    # Plot user data
    ax.plot(plot_angles, plot_values, color=COLORS['plot'], linewidth=2)
    ax.fill(plot_angles, plot_values, color=COLORS['plot'], alpha=0.2)

    # Add level assessment text at the bottom
    fig.text(0.5, 0.06, f"{eng_level}", ha='center', va='bottom',
             fontsize=16, color=COLORS['plot'], fontweight='bold')
    fig.text(0.5, 0.02, f"Average: {avg:.1f}/5 — {description}", ha='center', va='bottom',
             fontsize=10, color=COLORS['grid'])

    plt.tight_layout(rect=[0, 0.08, 1, 1])

    # Create output directory and save with timestamp
    create_output_directory()
    filename = generate_filename()
    plt.savefig(filename, facecolor=fig.get_facecolor())
    print(f"\nRadar chart saved as '{filename}'")
    plt.show()


def main():
    """Main application entry point."""
    parser = setup_argument_parser()
    args = parser.parse_args()

    try:
        scores = get_user_input()
        print_assessment(scores)
        create_radar_chart(scores)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()