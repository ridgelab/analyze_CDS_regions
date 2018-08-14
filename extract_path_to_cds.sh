#${1} is the taxonomic group. e.g., archaea, fungi, etc.

find genbank/${1}/*/latest_assembly_versions/  -name "*cds_from_genomic.fna.gz" > path_to_cds_${1}
