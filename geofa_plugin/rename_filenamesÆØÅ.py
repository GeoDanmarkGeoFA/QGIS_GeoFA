import os
import unicodedata

def normalize_filename(filename):
    # Normalize filename to the composed form
    return unicodedata.normalize('NFC', filename)

def replace_scandinavian_characters(filename):
    # Replace Scandinavian characters (both composed and decomposed forms)
    return (filename.replace('Å', 'Å').replace('Å', 'Å')
                    .replace('Ø', 'Ø').replace('Ö', 'Ø')
                    .replace('Æ', 'Æ').replace('Ä', 'Æ'))

def main():
    # Get the directory where the script file is located
    script_directory = os.path.dirname(os.path.realpath(__file__))
    print(f"Processing directory: {script_directory}")

    # Iterate over all files in the script directory
    for filename in os.listdir(script_directory):
        normalized_filename = normalize_filename(filename)
        print(f"Checking file: {normalized_filename}")

        # Check if the file name contains Scandinavian characters
        if any(char in normalized_filename for char in ['Å', 'Ø', 'Æ', 'Å', 'Ö', 'Ä']):
            # Replace the Scandinavian characters
            new_filename = replace_scandinavian_characters(normalized_filename)
            # Rename the file
            os.rename(os.path.join(script_directory, filename), os.path.join(script_directory, new_filename))
            print(f'Renamed "{filename}" to "{new_filename}"')

    # Wait for user input before closing
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()