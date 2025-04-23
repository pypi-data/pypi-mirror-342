import datetime
import gzip

from logging import Logger

from ingestion.vcf_standardization.standardize import standardize_vcf


def create_empty_vcf_zip(prefix):
    vcf_gzip_path = f"{prefix}.modified.somatic.vcf.gz"
    content = (
        """##fileformat=VCFv4.1
##filedate="""
        + datetime.datetime.now().isoformat()
        + """
##FILTER=<ID=PASS,Description="All filters passed">
##FILTER=<ID=R8,Description="IndelRepeatLength is greater than 8">
##FILTER=<ID=R8.1,Description="IndelRepeatLength of a monomer is greater than 8">
##FILTER=<ID=R8.2,Description="IndelRepeatLength of a dimer is greater than 8">
##FILTER=<ID=sb,Description="Variant strand bias high">
##FILTER=<ID=sb.s,Description="Variant strand bias significantly high (only for SNV)">
##FILTER=<ID=rs,Description="Variant with rs (dbSNP) number in a non-core gene">
##FILTER=<ID=FP,Description="Possibly false positives due to high similarity to off-target regions">
##FILTER=<ID=NC,Description="Noncoding INDELs on non-core genes">
##FILTER=<ID=lowDP,Description="low depth variant">
##FILTER=<ID=Benign,Description="Benign variant">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AF,Number=1,Type=String,Description="Variant Allele Frequency">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	"""
        + prefix
        + """
"""
    )

    with gzip.open(vcf_gzip_path, "wb") as f:
        f.write(content.encode("utf-8"))


# This is done in next step, we are just adding to yaml
def extract_sv(prefix, include_somatic: bool):
    vcfs = []

    # Hard-code genome reference for Nebula VCFs
    genome_reference = "GRCh38"

    if include_somatic:
        vcfs.append(
            {
                "fileName": f".lifeomic/nebula/{prefix}/{prefix}.modified.somatic.nrm.filtered.vcf.gz",
                "sequenceType": "somatic",
                "type": "shortVariant",  # todo: Is this always going to be shortVariant?
                "reference": genome_reference,
            }
        )

    return vcfs


def get_vendsig_dict(json_data, log: Logger):
    # Return a dicitionary of {'chr:star_pos:ref:alt' : 'vendsig'}
    vendsig_dict = {"vendor": "nebula"}

    return vendsig_dict


def map_vendsig(ci: str) -> str:
    if ci in ["Pathogenic Variant", "Pathogenic"]:
        return "Pathogenic"
    elif ci in ["Likely Pathogenic Variant", "Likely Pathogenic"]:
        return "Likely pathogenic"
    elif ci in ["Benign Variant", "Benign"]:
        return "Benign"
    elif ci in ["Likely Benign Variant", "Likely Benign"]:
        return "Likely benign"
    elif ci in ["Variant of Uncertain Significance", "VUS"]:
        return "Uncertain significance"
    else:
        return "Unknown"


def process_nebula_vcf(infile, json_data, outpath, file_name, log: Logger):
    line_count = 0
    vendsig_dict = {"vendor": "nebula"}

    outfile = f"{file_name}.modified.somatic.vcf"
    sample_name = file_name
    # Read in a dictionary of variants with VENDSIG from the JSON file for somatic only
    vendsig_dict = get_vendsig_dict(json_data, log)

    line_count = standardize_vcf(
        infile=infile,
        outfile=outfile,
        out_path=outpath,
        case_id=sample_name,
        log=log,
        vendsig_dict=vendsig_dict,
        compression=True,
    )

    return line_count
