from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.utils import ImageReader
from utils.time import format_singapore_time_for_filename, format_singapore_datetime_for_report
import os

def add_svg_to_pdf(pdf_canvas, svg_filename, y_position):
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
    renderPDF.draw(drawing, pdf_canvas, 100, y_position)  # Position dynamically

def wrap_text(text, max_width, font_size, canvas):
    wrapped_text = []
    words = text.split()
    line = ""

    for word in words:
        test_line = line + " " + word if line else word
        text_width = canvas.stringWidth(test_line, "Helvetica", font_size)
        if text_width <= max_width:
            line = test_line
        else:
            wrapped_text.append(line)
            line = word  # Start a new line

    wrapped_text.append(line)  # Append the last line
    return wrapped_text

def add_meme_to_pdf(pdf_canvas, meme):
    pdf_canvas.showPage()
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(50, letter[1] - 50, f"Rank: {meme['rank']}")

    pdf_canvas.setFont("Helvetica", 12)
    y_position = letter[1] - 80  # Start below the title

    # Define max text width for wrapping
    max_text_width = 500

    # Wrap and draw title
    pdf_canvas.setFont("Helvetica-Bold", 12)
    wrapped_title = wrap_text(f"Title: {meme['title']}", max_text_width, 12, pdf_canvas)
    for line in wrapped_title:
        pdf_canvas.drawString(50, y_position, line)
        y_position -= 15

    # Wrap and draw score, comments, upvote ratio
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(50, y_position, f"Score: {meme['score']}")
    y_position -= 15
    pdf_canvas.drawString(50, y_position, f"Comments: {meme['num_comments']}")
    y_position -= 15
    pdf_canvas.drawString(50, y_position, f"Upvote Ratio: {meme['upvote_ratio'] * 100:.2f}%")
    y_position -= 15

    # Wrap and draw URL
    pdf_canvas.setFont("Helvetica", 12)
    wrapped_url = wrap_text(f"URL: {meme['url']}", max_text_width, 10, pdf_canvas)
    for line in wrapped_url:
        pdf_canvas.drawString(50, y_position, line)
        y_position -= 15

    # Draw Meme Image (if available)
    if meme.get("image_url"):
        try:
            img = ImageReader(meme["image_url"])
            img_width, img_height = 300, 300
            y_position -= img_height + 20  # Leave space for the image
            pdf_canvas.drawImage(img, 50, y_position, width=img_width, height=img_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error loading meme image: {e}")
            pdf_canvas.setFont("Helvetica-Oblique", 12)  # Italic font
            pdf_canvas.drawString(50, y_position - 20, "No image available")
    else:
        pdf_canvas.setFont("Helvetica-Oblique", 12)  # Italic font
        pdf_canvas.drawString(50, y_position - 20, "No image available")

def add_graphs_to_pdf(pdf_canvas, upvotes_vs_comments_graph, upvotes_per_hour_graph, upvote_ratio_graph):
    # Add Upvotes vs Comments Graph
    if upvotes_vs_comments_graph and os.path.exists(upvotes_vs_comments_graph):
        pdf_canvas.showPage()
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(50, letter[1] - 50, "Meme Engagement Level: Upvotes vs Comments Graph")
        add_svg_to_pdf(pdf_canvas, upvotes_vs_comments_graph, 400)

    # Add Upvotes Per Hour Graph
    if upvotes_per_hour_graph and os.path.exists(upvotes_per_hour_graph):
        pdf_canvas.showPage()
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(50, letter[1] - 50, "Meme Trendiness: Upvotes Per Hour Graph")
        add_svg_to_pdf(pdf_canvas, upvotes_per_hour_graph, 400)

    # Add Upvote Ratio Graph (Meme Controversy Chart)
    if upvote_ratio_graph and os.path.exists(upvote_ratio_graph):
        pdf_canvas.showPage()
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(50, letter[1] - 50, "Meme Controversy: Upvote Ratio Graph")
        add_svg_to_pdf(pdf_canvas, upvote_ratio_graph, 400)

def generate_meme_report(memes, upvotes_vs_comments_graph, upvotes_per_hour_graph, upvote_ratio_graph):
    if not memes:
        print("No memes available to generate a report.")
        return None

    # Generate a timestamped filename
    report_filename = f"top_memes_report_{format_singapore_time_for_filename()}.pdf"
    pdf_canvas = canvas.Canvas(report_filename, pagesize=letter)

    # Add Title Page
    pdf_canvas.setFont("Helvetica-Bold", 20)
    pdf_canvas.drawString(50, letter[1] - 100, "Top 20 Trending Memes Report (Past 24 Hours)")
    pdf_canvas.setFont("Helvetica", 14)
    pdf_canvas.drawString(50, letter[1] - 140, f"Generated on: {format_singapore_datetime_for_report()}")

    # Add each meme on a new page
    for meme in memes:
        add_meme_to_pdf(pdf_canvas, meme)

    add_graphs_to_pdf(pdf_canvas, upvotes_vs_comments_graph, upvotes_per_hour_graph, upvote_ratio_graph)

    # Save the PDF
    pdf_canvas.save()

    return report_filename
