#!/bin/bash
function  checkPids() {
    for pid in "${pidList[@]}"; do
        if ! kill -0 "$pid" 2>/dev/null; then
            # If PID is no longer running, remove it from the list
            pidList=(${pidList[@]/$pid})
            return 0
        fi
    done
    return 1
}

function filterSequence() {
    local pattern="$(basename $1 | sed 's/_R[12]_.*//')"
    local ynamesArray=($outputDir/${pattern}*/ynames.txt)

    # Check if ynames.txt exists
    [ -f "${ynamesArray[0]}" ] || return

    
    # Determine if input file is gzipped and set the appropriate command to read it
    local fileCmd
    local outputCmd
    local outputCmdY

    # Get the directory of the first ynames.txt file
    local ynamesDir=$(dirname "${ynamesArray[0]}")


    # Get the basename of the input file and construct the output filename
    local baseName=$(basename "$1")
    local namePart="${baseName%%.*}"
    local extension="${baseName#*.}"
    local outputFile="$ynamesDir/${namePart}.filtered.${extension}"
    # New file for Y chromosome reads
    local outputFileY="$ynamesDir/${namePart}.chrY.${extension}"
    
    # Skip if files exist and overwrite is not set
    [[ -f "$outputFile" && -f "$outputFileY" && -z "$overwrite" ]] && return 
    
    if [[ $1 == *.gz ]]; then
        fileCmd="zcat"
        outputCmd="| gzip > \"$outputFile\""
    else
        fileCmd="cat"
        outputCmd="> \"$outputFile\""
    fi

    # Get the directory of the script
    local script_dir="$(dirname "$(readlink -f "$0")")"
    local awk_script="${script_dir}/filter_fastq.awk"

    # Build and execute the command to create both filtered files
    eval "$fileCmd \"$1\" | awk -v ynamesFile=\"${ynamesArray[0]}\" -v outputFileY=\"$outputFileY\" -f \"$awk_script\" $outputCmd"
}

[ -z "$nThreads" ] && nThreads=1
pidList=()  # initialize an array to hold PIDs
[ -z "$alignedDir" ] && echo "need $alignedDir" && exit 1
[ -z "$outputDir" ] &&  echo "need $outputDir" && exit 1

trimmedNames=($(find $alignedDir -mindepth 1 -maxdepth 1 -type d))

[ -n "$sequenceDir" ] &&  sequenceFiles=($(find $sequenceDir -type f \( -name "*.fq" -o -name "*.fq.gz" -o -name "*.fastq" -o -name "*.fastq.gz" \)))

for trimmedName in "${trimmedNames[@]}"; do
    (
    echo "working on $trimmedName"
    output="$outputDir/$(basename $trimmedName)"
    ynames="$output/ynames.txt"
    genesBamIn="$trimmedName/Aligned.out.bam"
    txBamIn="$trimmedName/Aligned.toTranscriptome.out.bam"
    genesBamOut="$output/Aligned.out.bam"
    txBamOut="$output/Aligned.toTranscriptome.out.bam"
    genesBamOutY="$output/Aligned.out.chrY.bam"
    txBamOutY="$output/Aligned.toTranscriptome.chrY.bam"

    mkdir -p "$output"
    #find readnames that align to Y chromosom    
    [[ ! -f "$ynames" || -n "$overwrite" ]] && \
    echo "samtools view "$genesBamIn" | awk '\$3 == \"chrY\" { unique[\$1]++ } END { for (val in unique) print val }' > $ynames" && \
    eval "samtools view "$genesBamIn" | awk '\$3 == \"chrY\" { unique[\$1]++ } END { for (val in unique) print val }' > $ynames"
    #filter the genome alignments
    [[ ! -f "$genesBamOut" || -n "$overwrite" ]] && \
    echo "samtools view -N $ynames -U $genesBamOut  -o $genesBamOutY $genesBamIn" && \
    eval "samtools view -N $ynames -U $genesBamOut  -o $genesBamOutY $genesBamIn"
    #filter the transcript alignments
    [[ ! -f "$txBamOut" || -n "$overwrite" ]] && \
    echo "samtools view -N $ynames -U $txBamOut  -o $txBamOutY $txBamIn" && \
    eval "samtools view -N $ynames -U $txBamOut  -o $txBamOutY $txBamIn"
    ) &
    pidList+=($!)
    while (( ${#pidList[@]} >= nThreads )); do
        checkPids || sleep 1
    done
done
#wait for the bam files to be done - needed for sequences
for pid in "${pidList[@]}"; do
    wait "$pid"
done
[ -z "$sequenceDir" ] && exit 0
echo "filtering sequences"
for sequenceFile in "${sequenceFiles[@]}"; do
    ( echo "working on $sequenceFile"
    filterSequence $sequenceFile ) &    
    pidList+=($!)
    while (( ${#pidList[@]} >= nThreads )); do
        checkPids || sleep 1
    done
done
for pid in "${pidList[@]}"; do
    wait "$pid"
done

