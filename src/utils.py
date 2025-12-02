import json
import pandas as pd
from fpdf import FPDF
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import threading

lock = threading.Lock()

class PDF(FPDF):
    def __init__(self, title=""):
        super().__init__()
        self.title_str = title

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'{self.title_str} and their Counts', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def generate_wordcloud(data):
    with lock:
        # Define dimensions to comfortably fit an A4 PDF page considering margins
        wc_width, wc_height = 520, 760  # Adjust as needed

        wc = WordCloud(
            width=wc_width, 
            height=wc_height, 
            background_color='white', 
            max_words=10,  # Reduced for better readability
            max_font_size=150  # Increased for better readability
        ).generate_from_frequencies(data)
        
        plt.figure(figsize=(wc_width / 80, wc_height / 80))  # Convert points to inches for figure size
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        image_path = "temp_wordcloud.png"
        plt.savefig(image_path, bbox_inches='tight', pad_inches=0.5)  # Added padding for aesthetics
        plt.close()
    return image_path

# def generate_wordcloud_from_text(text):
#     # Define dimensions to comfortably fit an A4 PDF page considering margins
#     wc_width, wc_height = 520, 760

#     wc = WordCloud(
#         width=wc_width,
#         height=wc_height,
#         background_color='white',
#         max_words=50,  # Reduced for better readability
#         max_font_size=150  # Increased for better readability
#     ).generate(text)
    
#     plt.figure(figsize=(wc_width / 80, wc_height / 80))
#     plt.imshow(wc, interpolation='bilinear')
#     plt.axis('off')
#     image_path = "temp_wordcloud.png"
#     plt.savefig(image_path, bbox_inches='tight', pad_inches=0.5)
#     plt.close()
#     return image_path


def data_to_pdf(df, column):
    # Get the counts of each unique value in the specified column
    value_counts = df[column].value_counts()
    # Convert the venue counts to a flat list of venues repeated by their count
    all_words = ' '.join([venue for venue, count in value_counts.items() for _ in range(count)])

    # Generate wordcloud and save the image
    # image_path = generate_wordcloud(value_counts.to_dict())
    image_path = generate_wordcloud_from_text(all_words)

    # Initialize PDF with the title set to the column name
    pdf = PDF(title=column)
    pdf.add_page()

    # Specify the path to DejaVuSans.ttf which is in the same directory as your script
    font_path = "DejaVuSans.ttf"
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Add the wordcloud image to the PDF
    pdf.image(image_path, x=0, y=0)  # Adjust x, y, w for placement and size

    # Move the cursor below the word cloud image before writing text.
    # You might need to adjust the 95 based on the height of your wordcloud and the desired space.
    pdf.add_page()

    # Add the venue counts to the PDF
    for value, count in value_counts.items():
        pdf.cell(0, 10, f"{count}: {value}", ln=True)

    # Save the PDF to a file
    pdf.output(f"{column}_counts.pdf")
    # print(f"PDF exported for {column}!")

def write_pretty_json_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    # Sample usage
    data = {
        "Venues": ["VenueA", "VenueB", "VenueA", "VenueC", "VenueB", "VenueC", "VenueC"]
    }
    df_sample = pd.DataFrame(data)
    data_to_pdf(df_sample, "Venues")
