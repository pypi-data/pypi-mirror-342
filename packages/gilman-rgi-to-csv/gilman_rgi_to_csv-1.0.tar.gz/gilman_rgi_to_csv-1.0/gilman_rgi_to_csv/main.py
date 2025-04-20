import pandas as pd
import argparse

# Define the version of your tool
__version__ = "1.0"

def convert_to_csv(input_file, output_file):
    try:
        # Read the tab-delimited file
        df = pd.read_csv(input_file, sep="\t")
        # Save the data to a CSV file
        df.to_csv(output_file, index=False)
        print(f"CSV file saved at: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Convert a tab-delimited RGI file to CSV file", 
                                     prog="gilman_rgi_to_csv", 
                                     epilog="This tool converts a tab-delimited RGI file to CSV.")
    
    # Add the version argument
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    # Add the other arguments
    parser.add_argument("-i", "--input", required=True, help="Input text file")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Only proceed with conversion if the input and output are provided
    if args.input and args.output:
        convert_to_csv(args.input, args.output)

if __name__ == "__main__":
    main()
