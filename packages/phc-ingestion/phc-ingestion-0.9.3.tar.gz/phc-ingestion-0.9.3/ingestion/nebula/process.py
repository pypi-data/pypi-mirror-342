import os
from pathlib import Path
from ingestion.vcf_standardization.standardize import standardize_vcf
from lifeomic_logging import scoped_logger


def process(vcf_file: str, source_file_id: str, out_path: str, case_id: str) -> dict:
    with scoped_logger(__name__) as log:
        # TODO: do we need to take in + process the manifest file here?

        # Process VCF
        base_vcf_file = os.path.basename(vcf_file)
        vcf_out = base_vcf_file.replace(".vcf", ".modified.vcf")
        vcf_final = base_vcf_file.replace(".vcf", ".modified.nrm.filtered.vcf")
        if not vcf_final.endswith(".gz"):
            vcf_final = vcf_final + ".gz"

        # Assuming Nebula VCFs are germline
        sample_name = f"germline_{case_id}"
        vcf_line_count = standardize_vcf(
            vcf_file, vcf_out, out_path, sample_name, log, compression=True
        )

        # Create a basic manifest for the Nebula VCF
        manifest = {
            "testType": "Nebula",
            "sourceFileId": source_file_id,
            "reference": "GRCh38",  # Assuming GRCh38, adjust as needed
            "resources": [{"fileName": f".lifeomic/nebula/{case_id}/{base_vcf_file}"}],
            "files": [
                {
                    "fileName": f".lifeomic/nebula/{case_id}/{vcf_final}",
                    "sequenceType": "germline",
                    "type": "shortVariant",
                }
            ],
        }

        case_metadata = {
            "test_type": "Nebula",
            "vcf_line_count": vcf_line_count,
            "case_id": case_id,
            "germline_genome_reference": manifest["reference"],
        }

        return case_metadata, manifest
