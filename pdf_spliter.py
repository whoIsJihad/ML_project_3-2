#!/usr/bin/env python3
import sys
import argparse
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf, output_pdf, start_page, end_page):
    """
    Extract pages from a PDF file and save to a new PDF.
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        start_page: Starting page number (1-indexed)
        end_page: Ending page number (1-indexed, inclusive)
    """
    try:
        # Read the input PDF
        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)
        
        # Validate page numbers
        if start_page < 1 or end_page > total_pages:
            print(f"Error: Page range must be between 1 and {total_pages}")
            sys.exit(1)
        
        if start_page > end_page:
            print("Error: Start page must be less than or equal to end page")
            sys.exit(1)
        
        # Create a PDF writer
        writer = PdfWriter()
        
        # Add pages (convert to 0-indexed)
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])
        
        # Write to output file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)
        
        pages_extracted = end_page - start_page + 1
        print(f"✅ Successfully extracted {pages_extracted} page(s) from '{input_pdf}'")
        print(f"   Pages {start_page} to {end_page} saved to '{output_pdf}'")
        
    except FileNotFoundError:
        print(f"Error: File '{input_pdf}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Split PDF by extracting specific page range",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf_spliter input.pdf output.pdf 23 25    # Extract pages 23-25
  pdf_spliter doc.pdf new.pdf 1 10          # Extract pages 1-10
        """
    )
    
    parser.add_argument("input_pdf", help="Input PDF file")
    parser.add_argument("output_pdf", help="Output PDF file")
    parser.add_argument("start_page", type=int, help="Starting page number (1-indexed)")
    parser.add_argument("end_page", type=int, help="Ending page number (1-indexed, inclusive)")
    
    args = parser.parse_args()
    
    split_pdf(args.input_pdf, args.output_pdf, args.start_page, args.end_page)

if __name__ == "__main__":
    main()
