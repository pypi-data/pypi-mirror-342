import sgkit as sg
from sgkit.io.vcf import vcf_to_zarr
from scipy.sparse import csr_matrix
from bed_reader import open_bed

import numpy as np
import time

def vcf_to_csr(variant_file, output_zarr, chunk_length = 10000):
    """
    Returns a sparse csr matrix with the allele dosages.
    Parameters:
        variant_file (str): Path to the input VCF file
    Returns:
        xs (scipy.sparse.csr_matrix): Sparse matrix with allele dosages.
    """
    # Convert VCF to Zarr and load with sgkit
    print("Reading VCF...")
    start_time = time.time()
    
    ds_zarr = vcf_to_zarr(variant_file, chunk_length=chunk_length,output = output_zarr)
    ds_zarr = sg.load_dataset(output_zarr)
    
    print("Fetching dosages...")
    ds = sg.convert_call_to_index(ds_zarr)["call_genotype_index"].values 
    
    # Transpose
    ds = np.transpose(ds)
    
    # Convert dosages values to sparse CSR format 
    print("Transforming into sparse CSR...")
    xs = csr_matrix(ds.astype(np.int32))
    
    print("Done:  %s seconds"  % (time.time() - start_time))
    return xs

def bed_to_csr(bed_file):
    """
    Returns a sparse csr matrix with the allele counts for bi-allelic alleles from bed file.
    Parameters:
        bed_file (str): Path to the input BED file
    Returns:
        xs (scipy.sparse.csr_matrix): Sparse matrix with allele counts.
    """
    # Read BED file
    print("Reading BED file and extracting genotype matrix")
    start_time = time.time()
    bed = open_bed(bed_file)
    geno = bed.read()
    geno = np.nan_to_num(geno, nan = -1)
    
    # Transform into CSR
    print("Transforming into sparse CSR...")
    xs = csr_matrix(geno)
    print("Done:  %s seconds"  % (time.time() - start_time))
    
    return xs