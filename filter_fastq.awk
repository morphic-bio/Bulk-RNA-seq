#!/usr/bin/awk -f
# filter_fastq.awk - Filters FASTQ reads based on whether they are in the ynames file
# 
# Usage: awk -f filter_fastq.awk -v ynamesFile="path/to/ynames.txt" -v outputFileY="path/to/chrY.output"

BEGIN {
    # Load the ynames file into an associative array
    while ((getline line < ynamesFile) > 0) {
        ynames[line] = 1;
    }
    close(ynamesFile); # Close the ynames file after reading

    # Determine how to handle output to outputFileY
    is_gzipped_y = (outputFileY ~ /\.gz$/);
    if (is_gzipped_y) {
        # Construct the command string for piping to gzip, ensuring outputFileY is quoted
        # This command will be executed by a shell invoked by awk
        y_destination_string = "gzip -c > \"" outputFileY "\"";
    } else {
        # For non-gzipped output, y_destination_string is just the filename for awk's redirection
        y_destination_string = outputFileY;
    }
}
{
    # Check if the first column is NOT in the ynames array
    # ignore the "@"
    firstColumn = substr($1, 2);
    if (!(firstColumn in ynames)) {
        # Print this line and the next three lines to standard output (non-Y reads)
        print;
        for (i = 0; i < 3; ++i) {
            if (getline <= 0) break;
            print;
        }
    } else {
        # Print this line and the next three lines to Y reads file
        if (is_gzipped_y) {
            # Pipe to the gzip command string
            print $0 | y_destination_string;
            for (i = 0; i < 3; ++i) {
                if (getline <= 0) break;
                print $0 | y_destination_string;
            }
        } else {
            # Redirect directly to the output file
            print $0 > y_destination_string;
            for (i = 0; i < 3; ++i) {
                if (getline <= 0) break;
                print $0 > y_destination_string;
            }
        }
    }
}
END {
    # Close the Y chromosome reads output (either the pipe or the file)
    # Must use the exact same string used for opening the pipe/file
    close(y_destination_string);
} 