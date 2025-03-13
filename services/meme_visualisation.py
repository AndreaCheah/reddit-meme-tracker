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
    nsfw_flags = [meme["over_18"] for meme in memes]
    ranks = [meme["rank"] for meme in memes]

    fig, ax = plt.subplots(figsize=(10, 5))

    # Color Coding: Red = NSFW, Blue = SFW
    colors = ['red' if nsfw else 'blue' for nsfw in nsfw_flags]
    sizes = np.array(upvote_ratios) * 300  

    scatter = ax.scatter(scores, comments, c=colors, s=sizes, alpha=0.7, edgecolors="black")

    # Label points with Rank Numbers
    for i, rank in enumerate(ranks):
        ax.text(scores[i], comments[i], str(rank), 
                fontsize=10, weight="bold", ha="right", color="black",
                bbox=dict(facecolor="white", edgecolor="black", alpha=0.7))

    ax.set_title("Meme Popularity: Upvotes vs Comments")
    ax.set_xlabel("Upvotes")
    ax.set_ylabel("Comments")
    ax.grid(True)

    # Log Scale for Consistency
    ax.set_xscale("log")
    ax.set_yscale("log")

    # Legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='SFW Memes', 
               markerfacecolor='blue', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='NSFW Memes', 
               markerfacecolor='red', markersize=10),
        Line2D([0], [0], linestyle='None', color='black', label='Numbers = Meme Rank')  # No marker, just text
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=10)

    # Save as SVG to preserve annotations
    svg_filename = f"meme_visualization_{format_singapore_time_for_filename()}.svg"
    plt.savefig(svg_filename, format="svg")
    plt.close()

    print(f"Visualization saved as: {svg_filename}")
    return svg_filename

def gen_fastest_rising_memes_graph(memes):
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
    ax.barh(sorted_titles, sorted_upvote_rates, color='purple', alpha=0.7)
    ax.set_xlabel("Upvotes per Hour")
    ax.set_ylabel("Meme Titles")
    ax.set_title("Fastest Rising Memes")
    ax.invert_yaxis()  # Highest upvote rate at the top
    plt.tight_layout()

    # Save as SVG
    svg_filename = f"fastest_rising_memes_{format_singapore_time_for_filename()}.svg"
    plt.savefig(svg_filename, format="svg")
    plt.close()

    print(f"Fastest rising meme visualization saved as: {svg_filename}")
    return svg_filename
