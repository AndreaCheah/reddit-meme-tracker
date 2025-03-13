import matplotlib.pyplot as plt
from datetime import datetime, timezone

def generate_meme_visualisation(memes):
    if not memes:
        print("No memes available for visualization.")
        return None

    scores = [meme["score"] for meme in memes]
    comments = [meme["num_comments"] for meme in memes]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(scores, comments, c="blue", alpha=0.5, edgecolors="black")
    ax.set_title("Upvotes vs Comments (Engagement Level)")
    ax.set_xlabel("Upvotes")
    ax.set_ylabel("Comments")
    ax.grid(True)

    image_filename = f"meme_visualization_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.png"
    plt.savefig(image_filename)
    plt.close()

    print(f"Visualization saved as: {image_filename}")
    return image_filename
