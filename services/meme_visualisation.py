import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timezone
from matplotlib.lines import Line2D
from utils.time import format_singapore_time_for_filename

def gen_upvotes_vs_comments_graph(memes):
    if not memes:
        print("No memes available for visualization.")
        return None

    scores = [meme["score"] for meme in memes]
    comments = [meme["num_comments"] for meme in memes]
    upvote_ratios = [meme["upvote_ratio"] for meme in memes]
    ranks = [meme["rank"] for meme in memes]

    fig, ax = plt.subplots(figsize=(10, 5))

    # Scatter plot
    sizes = np.array(upvote_ratios) * 300
    scatter = ax.scatter(scores, comments, s=sizes, alpha=0.7, edgecolors="black")

    # Label points with Rank Numbers
    for i, rank in enumerate(ranks):
        ax.text(scores[i], comments[i], str(rank), 
                fontsize=10, weight="bold", ha="right", color="black",
                bbox=dict(facecolor="white", edgecolor="black", alpha=0.7))

    ax.set_title("Meme Engagement: Upvotes vs Comments")
    ax.set_xlabel("Upvotes")
    ax.set_ylabel("Comments")
    ax.grid(True)

    # Log Scale for Consistency
    ax.set_xscale("log")
    ax.set_yscale("log")

    # Legend - Move to the right outside the plot
    legend_elements = [
        Line2D([0], [0], linestyle='None', color='black', label='Numbers = Meme Rank')
    ]
    ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1.05, 1), fontsize=10, borderaxespad=0.)

    # Adjust layout to make space for the legend
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Leave space on the right

    # Save as SVG to preserve annotations
    svg_filename = f"upvotes_vs_comments_{format_singapore_time_for_filename()}.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight")  # Ensure the full plot (including legend) is saved
    plt.close()

    return svg_filename

def gen_upvotes_per_hour_graph(memes):
    if not memes:
        print("No memes available for visualization.")
        return None

    # Calculate upvote rate (Upvotes per Hour)
    current_time = datetime.now(timezone.utc)
    upvote_rates = []
    titles = []

    for meme in memes:
        post_time = datetime.fromisoformat(meme["created_at"])  # Convert to datetime
        hours_since_post = (current_time - post_time).total_seconds() / 3600  # Convert seconds to hours
        if hours_since_post > 0:  # Avoid division by zero
            upvote_rate = meme["score"] / hours_since_post
            upvote_rates.append(upvote_rate)
            # Add rank for easy lookup for reader and limit title length for readability
            titles.append(f"{meme['rank']}. {meme['title'][:20]}")

    # Sort by upvote rate (Descending)
    sorted_indices = np.argsort(upvote_rates)[::-1]
    sorted_upvote_rates = np.array(upvote_rates)[sorted_indices]

    # Add rank numbers to labels
    sorted_titles = [f"{titles[idx]}" for rank, idx in enumerate(sorted_indices)]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(sorted_titles, sorted_upvote_rates, color='blue', alpha=0.7)
    ax.set_xlabel("Upvotes per Hour")
    ax.set_ylabel("Meme Titles")
    ax.set_title("Fastest Rising Memes")
    ax.invert_yaxis()  # Highest upvote rate at the top
    plt.tight_layout()

    # Save as SVG
    svg_filename = f"upvotes_per_hour_{format_singapore_time_for_filename()}.svg"
    plt.savefig(svg_filename, format="svg")
    plt.close()

    return svg_filename


def gen_upvote_ratio_graph(memes):
    if not memes:
        print("No memes available for visualization.")
        return None

    # Extract upvote ratios and titles with ranks
    upvote_ratios = [meme["upvote_ratio"] * 100 for meme in memes]  # Convert to percentage
    titles_with_ranks = [f"{meme['rank']}. {meme['title'][:20]}" for meme in memes]  # Shorten titles
    nsfw_flags = [meme["over_18"] for meme in memes]  # NSFW flags

    # Sort by upvote ratio (Ascending) → Most controversial memes first
    sorted_indices = np.argsort(upvote_ratios)  # Lowest ratios at the top
    sorted_upvote_ratios = np.array(upvote_ratios)[sorted_indices]
    sorted_titles = np.array(titles_with_ranks)[sorted_indices]
    sorted_nsfw_flags = np.array(nsfw_flags)[sorted_indices]

    # Assign colors: Red for NSFW, Blue for SFW
    colors = ['red' if nsfw else 'purple' for nsfw in sorted_nsfw_flags]

    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(sorted_titles, sorted_upvote_ratios, color=colors, alpha=0.7)
    ax.set_xlabel("Upvote to Downvote Ratio (%)")
    ax.set_ylabel("Meme Titles (Ranked)")
    ax.set_title("Meme Controversy: Upvote Ratio (Lower = More Disputed)")
    ax.invert_yaxis()  # Most controversial memes at the top
    plt.tight_layout()

    # Legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='SFW Memes', 
               markerfacecolor='purple', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='NSFW Memes', 
               markerfacecolor='red', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=10)

    # Save as SVG
    svg_filename = f"upvote_ratio_{format_singapore_time_for_filename()}.svg"
    plt.savefig(svg_filename, format="svg")
    plt.close()

    return svg_filename
