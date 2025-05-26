function filterSequence() {
    local pattern="$(basename $1 | sed 's/_R[12]_.*//')"
    local ynamesArray=($outputDir/${pattern}*/ynames.txt)

    # Check if ynames.txt exists
    [ -f "${ynamesArray[0]}" ] || return

    local ynamesDir=$(dirname "${ynamesArray[0]}")
    local baseName=$(basename "$1")
    local namePart="${baseName%%.*}"
    local extension="${baseName#*.}"

    # existing “filtered” output (reads NOT on chrY)
    local outputFile="$ynamesDir/${namePart}.filtered.${extension}"
    # new “Y-reads” output
    local yOutputFile="$ynamesDir/${namePart}.Yreads.${extension}"

    [[ -f "$outputFile" && -z "$overwrite" ]] && return

    # (re)create the Y-reads file so that >> in awk starts from empty
    : > "$yOutputFile"

    if [[ $1 == *.gz ]]; then
        fileCmd="zcat"
        outputCmd="| gzip > \"$outputFile\""
    else
        fileCmd="cat"
        outputCmd="> \"$outputFile\""
    fi

    # now run awk, printing non-Y to stdout (→ $outputFile) and Y to $yOutputFile
    eval "$fileCmd \"$1\" | awk \
        -v ynamesFile=\"${ynamesArray[0]}\" \
        -v yOutFile=\"$yOutputFile\" '
    BEGIN {
        # load all ynames into an array
        while ((getline line < ynamesFile) > 0) {
            ynames[line] = 1
        }
    }
    {
        # drop the leading "@"
        id = substr(\$1, 2)
        if (!(id in ynames)) {
            # non-Y: print this record to default stdout
            print
            for (i=0; i<3; i++) {
                if (getline <= 0) break
                print
            }
        } else {
            # Y: print this record to the Y-reads file
            print >> yOutFile
            for (i=0; i<3; i++) {
                if (getline <= 0) break
                print >> yOutFile
            }
        }
    }' $outputCmd"
}