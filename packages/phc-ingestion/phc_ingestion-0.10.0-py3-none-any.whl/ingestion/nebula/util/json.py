import glob
import gzip
import os
import shutil

from ingestion.shared_util.tar import unpack
from ingestion.nebula.util.vcf import extract_sv
from ingestion.shared_util.ga4gh import create_yaml
from logging import Logger


def handle_tsv(file: str, file_list: list[str]) -> dict[str, str]:
    multiple_tsv = len([file for file in file_list if file.endswith("tsv")]) > 1

    if not multiple_tsv or "Transformed" in file:
        return {
            "tsv": file,
        }
    return {}


def process_nebula_json(
    infile: str, outpath: str, file_name: str, source_file_id: str, log: Logger
):
    # Unpack tarball and go into the new directory
    unpack(infile, outpath)
    os.chdir(outpath)

    file_list = glob.glob("*")
    files: dict[str, str] = {}

    for file in file_list:
        extension = ".".join(file.split(".")[1:])
        if file.endswith("vcf"):
            files["somatic.vcf"] = file
        else:
            # There should only be the vcf file
            files[extension] = file

    log.info(f"Files in tarball input: {file_list}")

    somatic_filename = None
    data = {}
    metadata = {}

    # Sometimes they don't come in gzipped
    for key in files.keys():
        if "somatic.vcf" in key:
            somatic_filename = files["somatic.vcf"].replace(".vcf", ".somatic.vcf") + ".gz"
            with open(files["somatic.vcf"], "rb") as f_in:
                with gzip.open(somatic_filename, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

    vcf_results = extract_sv(file_name, bool(somatic_filename), False, False)

    # We might not have any of these files but we need an empty json object here.
    file_genome_references = {}
    if vcf_results:
        metadata["files"] = metadata["files"] + vcf_results
        for vcf in vcf_results:
            seq_type = vcf.get("sequenceType")
            file_genome_references[f"{seq_type}_genome_reference"] = vcf["reference"]

    create_yaml(metadata, file_name)

    # Return VCF files for immediate processing, and JSON data for adding vendsig
    result = {}

    if somatic_filename is not None:
        result["somatic_vcf"] = f"{outpath}/{somatic_filename}"

    return (result, file_genome_references, data)
