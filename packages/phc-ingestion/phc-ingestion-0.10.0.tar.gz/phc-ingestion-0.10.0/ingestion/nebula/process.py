import os

from ingestion.nebula.util.json import process_nebula_json
from ingestion.nebula.util.vcf import process_nebula_vcf
from lifeomic_logging import scoped_logger


def process_nebula(infile, outpath, file_name, source_file_id):

    with scoped_logger(__name__) as log:
        os.makedirs(f"{outpath}", exist_ok=True)
        result, file_genome_references, json_data = process_nebula_json(
            infile, outpath, file_name, source_file_id, log
        )
        somatic_vcf_line_count = process_nebula_vcf(
            result["somatic_vcf"], json_data, outpath, file_name, log
        )
        case_metadata = {
            "somatic_vcf_line_count": somatic_vcf_line_count,
        }

        if file_genome_references != {}:
            case_metadata.update(file_genome_references)

        return case_metadata
