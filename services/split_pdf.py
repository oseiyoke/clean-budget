import PyPDF2
import os

def extract_pages(source_pdf_path, target_pdf_path, pages_to_extract):
    """
    Extracts specific pages from a PDF and saves them into a new PDF file.

    Parameters:
    - source_pdf_path: Path to the source PDF file.
    - target_pdf_path: Path where the new PDF file will be saved.
    - pages_to_extract: A list of page numbers to extract (0-indexed).
    """
    # Open the source PDF file
    with open(source_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Add specified pages to the writer object
        for page_num in pages_to_extract:
            writer.add_page(reader.pages[page_num])

        # Write out the new PDF
        with open(target_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)

def main(source_path, pages_per_pdf):
    """
    A function to split a PDF into multiple smaller PDFs based on the given number of pages per PDF.
    
    :param source_path: The path of the source PDF file to be split
    :param pages_per_pdf: The number of pages per PDF for the split
    
    :return: None
    """
    # create folder
    file_name = source_path.split('/')[-1].split('.')[0]
    folder = os.path.dirname(source_path) + '/' + file_name + '_split'
    if not os.path.exists(folder):
        print("Creating Folder to store split pdfs...")
        os.makedirs(folder)

    num_pages = len(PyPDF2.PdfReader(source_path).pages)
    chunks = (num_pages // pages_per_pdf) + (1 if num_pages % pages_per_pdf else 0)

    print(f"Found {num_pages} pages in document. Splitting into {chunks} chunks of {pages_per_pdf} pages each.")

    for i in range(chunks):
        print(f"Extracting chunk {i+1} of {chunks}")
        target_pdf  = os.path.join(folder, f"{file_name}_{i+1}.pdf")
        pages_to_extract = range(i*pages_per_pdf, (i+1)*pages_per_pdf)
        
        # When the last chunk is reached, the range should stop at the last page to prevent index error
        if i == chunks - 1:
            pages_to_extract = range(i*pages_per_pdf, num_pages)

        extract_pages(source_path, target_pdf, pages_to_extract)

        print(f"Successfully created chunk {i+1} of {chunks}\n\n")
