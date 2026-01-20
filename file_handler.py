def read_sales_data(filename):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                lines = file.readlines()

            # remove empty lines
            clean_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    clean_lines.append(line)

            # skip header if present
            if clean_lines and clean_lines[0].lower().startswith("transactionid"):
                clean_lines = clean_lines[1:]

            return clean_lines

        except:
            continue

    raise FileNotFoundError("Unable to read file with supported encodings")
def read_sales_data(filename):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                lines = file.readlines()

            # remove empty lines
            clean_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    clean_lines.append(line)

            # skip header if present
            if clean_lines and clean_lines[0].lower().startswith("transactionid"):
                clean_lines = clean_lines[1:]

            return clean_lines

        except:
            continue

    raise FileNotFoundError("Unable to read file with supported encodings")
