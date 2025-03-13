import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timezone
from matplotlib.lines import Line2D

def generate_meme_visualisation(memes):
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
        Line2D([0], [0], linestyle='None', color='black', label='Numbers = Meme Rank')
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=10)

    # Save as SVG to preserve annotations
    svg_filename = f"meme_visualization_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.svg"
    plt.savefig(svg_filename, format="svg")
    plt.close()

    print(f"Visualization saved as: {svg_filename}")
    return svg_filename
