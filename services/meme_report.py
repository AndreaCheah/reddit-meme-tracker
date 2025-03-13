from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def generate_meme_report(memes, visualization_path):
    if not memes:
        print("No memes available to generate a report.")
        return None

    report_filename = f"top_memes_report_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    
    # Create a new PDF file
    c = canvas.Canvas(report_filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Top 20 Trending Memes Report (Past 24 Hours)")
    c.line(50, height - 55, 550, height - 55)

    y_position = height - 80  # Start below title

    for meme in memes:
        # Ensures y_position >= 120 so that there's enough space for the last meme on the page 
        # If the page runs out of space, create a new page and reset y_position
        if y_position < 120:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

        # Rank as header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, f"Rank: {meme['rank']}")
        y_position -= 15

        # Meme details
        c.setFont("Helvetica", 11)
        c.drawString(50, y_position, f"Title: {meme['title']}")
        y_position -= 15
        c.drawString(50, y_position, f"Score: {meme['score']}")
        y_position -= 15
        c.drawString(50, y_position, f"Comments: {meme['num_comments']}")
        y_position -= 15
        c.drawString(50, y_position, f"Upvote Ratio: {meme['upvote_ratio']}")
        y_position -= 15
        c.drawString(50, y_position, f"URL: {meme['url']}")
        y_position -= 25

    if visualization_path and os.path.exists(visualization_path):
        c.showPage()  # Ensure the graph is on a new page
        try:
            img = ImageReader(visualization_path)
            img_width = 400
            img_height = 300
            c.drawImage(img, (width - img_width) / 2, height - img_height - 50, 
                        width=img_width, height=img_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error adding image to PDF: {e}")

    c.save()

    print(f"PDF Report generated: {report_filename}")
    return report_filename, visualization_path
