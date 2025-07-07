import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from datetime import datetime

# Configuration constants
SCORE_RANGE = (1, 5)
CHART_SIZE = (8, 8)
MAX_LEVELS = 5
COLORS = {'background': 'black', 'grid': 'white', 'plot': 'yellow'}
OUTPUT_DIR = 'out'

AXES_CONFIG = {
    'Technology': ['Adopts', 'Specializes', 'Evangelizes', 'Masters', 'Creates'],
    'System': ['Enhances', 'Designs', 'Owns', 'Evolves', 'Leads'],
    'People': ['Learns', 'Supports', 'Mentors', 'Coordinates', 'Manages'],
    'Process': ['Follows', 'Enforces', 'Challenges', 'Adjusts', 'Defines'],
    'Influence': ['Subsystem', 'Team', 'Multiple Teams', 'Company', 'Community']
}


def setup_argument_parser():
    """Setup command line argument parser."""
    parser = argparse.ArgumentParser(
        description='Engineering Ladder Assessment - Generate a radar chart visualization '
                    'of technical leadership skills across 5 dimensions.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode - you'll be prompted for scores
  python main.py -h                 # Show this help message

Assessment Dimensions:
  Technology: Technical skill and knowledge depth
  System: System design and architecture abilities  
  People: Team collaboration and mentoring skills
  Process: Process improvement and methodology skills
  Influence: Scope of impact and leadership reach

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
    print(f"Enter scores from {SCORE_RANGE[0]} to {SCORE_RANGE[1]} for each dimension:")
    print()

    scores = []
    for axis in AXES_CONFIG.keys():
        while True:
            try:
                user_input = input(f"Enter {axis} score ({SCORE_RANGE[0]}-{SCORE_RANGE[1]}): ")
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

    # Setup figure
    fig, ax = plt.subplots(figsize=CHART_SIZE, subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])

    # Configure axes
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(AXES_CONFIG.keys(), color=COLORS['grid'], fontsize=12)
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
    for i, (axis, levels) in enumerate(AXES_CONFIG.items()):
        for j, level_name in enumerate(levels):
            ax.text(angles[i], j + 1, level_name, color=COLORS['grid'],
                    fontsize=8, ha='center', va='center')

    # Plot user data
    ax.plot(plot_angles, plot_values, color=COLORS['plot'], linewidth=2)
    ax.fill(plot_angles, plot_values, color=COLORS['plot'], alpha=0.2)

    plt.tight_layout()

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
        create_radar_chart(scores)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()