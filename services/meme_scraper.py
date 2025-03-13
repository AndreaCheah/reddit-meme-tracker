import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timezone

def generate_meme_visualisation(memes):
    if not memes:
        print("No memes available for visualization.")
        return None

    scores = [meme["score"] for meme in memes]
    comments = [meme["num_comments"] for meme in memes]
    upvote_ratios = [meme["upvote_ratio"] for meme in memes]
    nsfw_flags = [meme["over_18"] for meme in memes]

    fig, ax = plt.subplots(figsize=(10, 5))

    # 🔴 Better Color Coding: Red = NSFW, Blue = SFW
    colors = np.array(['red' if nsfw else 'blue' for nsfw in nsfw_flags])

    # 🔵 Increase Size Scaling for Visibility
    sizes = np.array(upvote_ratios) * 300  # Increased for effect

    # ✅ Add More Transparency for Better Visibility
    scatter = ax.scatter(scores, comments, c=colors, s=sizes, alpha=0.8, edgecolors="black")

    # ✅ Add Annotations for the Top 5 Memes
    sorted_memes = sorted(memes, key=lambda x: x["score"], reverse=True)[:5]
    for meme in sorted_memes:
        ax.annotate(meme["title"][:15],  # Display only the first 15 characters
                    (meme["score"], meme["num_comments"]),
                    fontsize=9, alpha=0.7, color="black",
                    bbox=dict(facecolor='white', alpha=0.5, edgecolor="black"))

    # ✅ Improve Readability with Log Scale for Comments
    ax.set_yscale("log")  # Log scale helps if some memes have way more comments

    ax.set_title("Meme Popularity: Upvotes vs Comments")
    ax.set_xlabel("Upvotes")
    ax.set_ylabel("Comments")
    ax.grid(True)

    # ✅ Add a Legend Manually
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='SFW', markerfacecolor='blue', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='NSFW', markerfacecolor='red', markersize=10)]
    ax.legend(handles=legend_elements, loc="upper left")

    # ✅ Save Image
    image_filename = f"meme_visualization_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.png"
    plt.savefig(image_filename)
    plt.close()

    print(f"Visualization saved as: {image_filename}")
    return image_filename
