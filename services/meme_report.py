from datetime import datetime, timezone
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
import os

def add_svg_to_pdf(pdf_canvas, svg_filename):
    drawing = svg2rlg(svg_filename)

    # Get original SVG dimensions
    orig_width, orig_height = drawing.width, drawing.height

    # Target size (letter size)
    max_width, max_height = 400, 300  # Scale appropriately for PDF

    # Calculate the scaling factor
    scale_factor = min(max_width / orig_width, max_height / orig_height)

    # Apply scaling
    drawing.width *= scale_factor
    drawing.height *= scale_factor
    drawing.scale(scale_factor, scale_factor)

    # Position the graph correctly
    renderPDF.draw(drawing, pdf_canvas, 100, 350)  # Centered on the page

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
    c.drawString(50, height - 50, "Top 20 Trending Memes Report (Past 24 Hours) 🔥")
    c.line(50, height - 55, 550, height - 55)

    y_position = height - 80  # Start below title

    for meme in memes:
        if y_position < 120:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, f"Rank: {meme['rank']}")
        y_position -= 15

        c.setFont("Helvetica", 11)
        c.drawString(50, y_position, f"Title: {meme['title']}")
        y_position -= 15
        c.drawString(50, y_position, f"Score: {meme['score']}")
        y_position -= 15
        c.drawString(50, y_position, f"Comments: {meme['num_comments']}")
        y_position -= 15
        c.drawString(50, y_position, f"Upvote Ratio: {meme['upvote_ratio']*100:.2f}%")
        y_position -= 15
        c.drawString(50, y_position, f"URL: {meme['url']}")
        y_position -= 25

    # Add the resized SVG visualization
    if visualization_path and os.path.exists(visualization_path):
        c.showPage()  # Ensure it starts on a new page
        add_svg_to_pdf(c, visualization_path)

    c.save()
    print(f"PDF Report generated: {report_filename}")
    return report_filename, visualization_path
