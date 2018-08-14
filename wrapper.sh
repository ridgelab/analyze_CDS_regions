#! /bin/bash

OPTIND=1         # Reset in case getopts has been used previously in the shell.
input_file=""
output_dir=""
verbose=0
gzip=0

while getopts "zvh?:i:o:" opt; do
    case "$opt" in
    h|\?)
		echo "-i is a required input file"
		echo "-o is a required output directory"
		echo "-h shows this help message"
		echo "-v shows verbose messages of progress"
        exit 0
        ;;
    v)  verbose=1
        ;;
	i)	input_file=$OPTARG
		;;
	z)	gzip=1
		;;
    o)  output_dir=$OPTARG
		if [[ "${output_dir:-1}" != '/' ]]; then
			output_dir=${output_dir}"/"	
			mkdir -p ${output_dir}
		fi
    esac
done
shift $(( OPTIND-1 )) 

if [[ ${input_file} == "" || ${output_dir} == "" ]]; then
	echo "-i and -o are required"
	exit 1
fi

if [[ ${verbose} == 1 ]]; then
	echo "Input File - $input_file" 
	echo "Output Directory - $output_dir" 
fi

while read -r line
do
	base=${line/"cds_from_genomic.fna.gz"/""}
	species=`cut -d '/' -f 2 <<<${base}`
	assembly=`cut -d '/' -f 4 <<<${base}`
	output=${output_dir}${species}"/"${assembly}
	mkdir -p ${output_dir}${species}
	gff3=${base}"genomic.gff.gz"	
	fasta=${base}"genomic.fna.gz"	
	if [[ ${gzip} == 1 ]]; then
		python gff3_parser.py -z -g ${gff3} -f ${fasta} -o ${output} 
		if [[ ${verbose} == 1 ]]; then
			echo "Output File Created - ${output}.gz" 
		fi
	else
		python gff3_parser.py -g ${gff3} -f ${fasta} -o ${output} 
		if [[ ${verbose} == 1 ]]; then
			echo "Output File Created - $output" 
		fi
	fi
done < "$input_file"



