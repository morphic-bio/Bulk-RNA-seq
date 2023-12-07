#!/bin/bash

# Accept directory path as argument
countsDir=$1
alignsDir=$2

# Check if directory exists
if [ ! -d "$countsDir" ]; then
    echo "Can't find countsDir $countsDir"
    exit 1
fi
if [ ! -d "$alignsDir" ]; then
    echo "Can't find countsDir $alignsDir"
    exit 1
fi
[ -n "$outputDir" ] || outputDir="$countsDir/../Tables"
mkdir -p "$outputDir"

# Find files named quant.genes.sf
quantGenesSfs=$(find "$countsDir" -type f -name 'quant.genes.sf')

# Initialize variables
header="Name"
# Process each file
while IFS= read -r quantGenesSf; do
    fullFilename="$quantGenesSf"
    fulltxFilename="${quantGenesSf//quant.genes.sf/quant.sf}"
    
    dir=$(dirname "$quantGenesSf")
    dir=$(basename "$dir")
    # Extract directory name up to _R1_
    if [[ $dir =~ (.*)_R1_(.*) ]]; then
        dir=${BASH_REMATCH[1]}
    fi

    # Check line count consistency of gene files
    mylines=$(wc -l "$fullFilename"| awk '{ print $1}')
    if [ -z "$nlines" ]; then
        nlines="$mylines"
    elif [ "$nlines" != "$mylines" ]; then
        echo "$fullFilename has $mylines lines instead of $nlines"
        exit 1
    fi
   # Check line count consistency of tx files
    mytxlines=$(wc -l "$fulltxFilename"| awk '{ print $1}')
    if [ -z "$ntxlines" ]; then
        ntxlines="$mytxlines"
    elif [ "$ntxlines" != "$mytxlines" ]; then
        echo "$fulltxFilename has $mytxlines lines instead of $ntxlines"
        exit 1
    fi
    # Build command
    [ -z "$cmd" ] && cmd="paste <(cut -f1 '$fullFilename')"
    cmd="$cmd <(cut -f5 '$fullFilename')"

    #build header
    header="${header}\t${dir}"
done <<< "$quantGenesSfs"

# Print raw table
newHeader=$(echo -e "$header")
eval "$cmd > $outputDir/genesRawCounts.csv"
sed -i "1s|.*|$newHeader|" "$outputDir/genesRawCounts.csv"

# Round the values and print  
echo -e "$header" > "$outputDir/genesCounts.csv"
cat "$outputDir/genesRawCounts.csv" | awk 'NR > 1 {
    printf $1; 
    for (i = 2; i <= NF; i++) {  
        printf "\t%d", $i + 0.5;  
    }
    printf "\n";  
}' >> "$outputDir/genesCounts.csv"

#change cmd to f4 for tpm
cmdtpm="${cmd//cut -f5/cut -f4}"
eval "$cmdtpm > $outputDir/genesTPM.csv"
sed -i "1s|.*|$newHeader|" "$outputDir/genesTPM.csv"

#change cmd for transcripts
cmdtx="${cmd//quant.genes.sf/quant.sf}"
eval "$cmdtx > $outputDir/txRawCounts.csv"
sed -i "1s|.*|$newHeader|" "$outputDir/txRawCounts.csv"

# Round the values and print  
echo -e "$header" > "$outputDir/txCounts.csv"
cat "$outputDir/txRawCounts.csv" | awk 'NR > 1 {
    printf $1;  # Print the first column as is
    for (i = 2; i <= NF; i++) {  
        printf "\t%d", $i + 0.5;  
    }
    printf "\n";  
}' >> "$outputDir/txCounts.csv"

#change cmd to f4 for tpm
cmdtxtpm="${cmdtx//cut -f5/cut -f4}"
eval "$cmdtxtpm > $outputDir/txTPM.csv"
sed -i "1s|.*|$newHeader|" "$outputDir/txTPM.csv"

#calculate featureCounts
header=name
cmd=""
fcFiles=$(find "$alignsDir" -type f -name 'ReadsPerGene.out.tab')
while IFS= read -r fcFile; do
    fullFilename="$fcFile"    
    dir=$(dirname "$fcFile")
    dir=$(basename "$dir")
    # Extract directory name up to _R1_
    if [[ $dir =~ (.*)_R1_(.*) ]]; then
        dir=${BASH_REMATCH[1]}
    fi

    # Check line count consistency of feature count files
    mylines=$(wc -l "$fullFilename"| awk '{ print $1}')
    if [ -z "$nfclines" ]; then
        nfclines="$mylines"
    elif [ "$nfclines" != "$mylines" ]; then
        echo "$fullFilename has $mylines lines instead of $nfclines"
        exit 1
    fi
    # Build command
    [ -z "$cmd" ] && cmd="paste <(cut -f1 '$fullFilename')"
    cmd="$cmd <(cut -f2 '$fullFilename')"
    #build header
    header="${header}\t${dir}"
done <<< "$fcFiles"
# Print featurecounts table

eval "$cmd > $outputDir/featureCounts.tmp.csv"
echo -e "$header" > "$outputDir/featureCounts.csv"
echo -e "$header" > "$outputDir/stats.csv"
head -4 "$outputDir/featureCounts.tmp.csv" >> "$outputDir/stats.csv"
tail -n +5 "$outputDir/featureCounts.tmp.csv" >> "$outputDir/featureCounts.csv"
rm "$outputDir/featureCounts.tmp.csv"
