from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import tempfile
import pandas as pd
from nbitk.Services.Galaxy.BLASTN import BLASTNClient
from nbitk.config import Config
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq


class TaxonValidator(BLASTNClient):
    """
    Client for validating taxonomic assignments of DNA sequences using BLAST. This client
    is tailored to the use case where barcode records stored in the Core Sequence Cloud
    are validated in small batches against a reference database. The validation consists
    of a check to see whether the putative taxon (note: we assume this is the family name)
    is present in the BLAST results. The results are attached to the input records for
    further analysis.
    """

    def __init__(self, config: Config, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the TaxonValidator client. This constructor delegates to the BLASTNClient
        constructor, which in turn initializes the Galaxy connection and tool. Consult the
        BLASTNClient documentation and that of the AbstractClient for more information.
        :param config: NBITK Config object containing Galaxy connection settings
        :param logger: Optional logging.logger instance. If None, creates one using the class name
        """
        super().__init__(config, logger)

    def validate_records(self, records: List[Dict[str, Any]], params: dict = {}) -> List[Dict[str, Any]]:
        """
        Validate a list of records taxonomically by running BLAST and comparing the results.
        :param records: List of records. Each record is a dictionary with the following keys:
            - local_id: Locally unique identifier
            - identification: Expected taxon (note: we now assume this is the family name)
            - nuc: Nucleotide sequence
        :param params: Optional parameters for the BLAST analysis. The parameters are passed
            directly to the BLASTNClient.run_blast method. The parameters are tool-specific
            and can be found in the BLASTNClient documentation.
        :return: Enriched records with validation result and other analytics. Each record is a
            dictionary with the following keys:
            - local_id: Locally unique identifier
            - identification: Expected taxon
            - nuc: Nucleotide sequence
            - is_valid: Boolean indicating if the record is valid
            - blast_results: Pandas data frame with the BLAST results
            - timestamp: Timestamp of the validation
        """

        # Create SeqRecord objects and write to FASTA file
        self.logger.info(f"Going to validate {len(records)} records")
        fasta_filename = self._bcdm2fasta(records)

        # Run BLAST on the Galaxy
        self.logger.info(f"Running BLAST on {fasta_filename}")
        result = self.run_blast(fasta_filename, **params)

        # Process BLAST results
        self.logger.info(f"Processing BLAST results")
        output_file = result['blast_output_fasta']
        return self._parse_blast_output(output_file, records)

    def _parse_blast_output(self, output_file: str, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        The BLAST operation performed by Galaxy returns a tab-separated file with the results. For every input
        record, the operation can return zero or more results. This method parses the BLAST output file for each
        set of results corresponding with an input 'local_id'. If the expected taxon is found in any of the results,
        the record is marked as valid by setting the 'is_valid' field to True. If no results are found, the record
        is marked as invalid. The full results are attached to the record under the 'blast_results' key as a pandas
        data frame for further analysis. Furthermore, the 'timestamp' field is added to the record to indicate when
        the validation was performed.
        :param output_file: The BLAST output file
        :param records: List of records. The records are dictionaries with the following keys:
            - local_id: Locally unique identifier
            - identification: Expected taxon
            - nuc: Nucleotide sequence
        :return: Enriched records. The records are dictionaries with the following keys:
            - local_id: Locally unique identifier
            - identification: Expected taxon
            - nuc: Nucleotide sequence
            - is_valid: Boolean indicating if the record is valid
            - blast_results: Pandas data frame with the BLAST results
            - timestamp: Timestamp of the validation
        """
        self.logger.debug(f"Parsing BLAST output file {output_file}")
        df = pd.read_csv(output_file, sep='\t', dtype=str)

        # Iterate over the BCDM records to crossreference with BLAST results
        for seq_dict in records:
            local_id = seq_dict['local_id']
            exp_taxon = seq_dict['identification'] # TODO: let's pretend this is the family name
            seq_dict['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Get all family names for the focal query
            blast_rows = df[df['#Query ID'] == local_id]

            # Check if anything was found at all for the focal query
            if len(blast_rows) == 0:

                # No results, hence invalid
                seq_dict['is_valid'] = False
                seq_dict['blast_results'] = None
            else:
                seq_dict['is_valid'] = False

                # Have results, check if any of them match the expected family
                for lineage in blast_rows['#Taxonomy']:
                    names = lineage.split(' / ')

                    # XXX: our assumption was that the `identification` column (i.e. exp_taxon) in the input
                    # was the family name, as per the notebook POC. This is not the case now. Rather,
                    # we are getting things that are sometimes species names and sometimes None. If it
                    # is None, the record will for sure not be valid. If it is a species name, the chance
                    # that the matching record will have that exact same name is very low. So, `is_valid` will
                    # be False almost always until this is addressed. An additionl problem is that no rank
                    # information is provided, so we now do a blind test if the expected taxon is anywhere
                    # in the lineage. This is very rough and open to abuse (?), because it could be used to
                    # tunnel something in there such as `Insecta` or `Animalia`.
                    if exp_taxon is not None and exp_taxon in names:
                        seq_dict['is_valid'] = True
                    if not 'blast_results' in seq_dict:
                        seq_dict['blast_results'] = list()
                    seq_dict['blast_results'].append(blast_rows)

        return records


    def _bcdm2fasta(self, records: List[Dict[str, Any]]) -> str:
        """
        Convert a list of records to a temporary FASTA file. In this operation, the
        'nuc' key in each record is expected to contain the nucleotide sequence, and
        the 'local_id' key is expected to contain a locally unique identifier. The
        resulting FASTA file will have the local_id as the header and the nucleotide
        sequence as the body. No other keys or values are expected in the records.
        The resulting file is uploaded to Galaxy for BLAST analysis. The results
        are joined with the input by way of the local_id.
        :param records: List of records
        :return: Name of the temporary FASTA file
        """
        self.logger.debug(f"Converting {len(records)} records to FASTA")

        # Create a list of SeqRecord objects
        seq_records = []
        for seq_dict in records:
            sequence = Seq(seq_dict['nuc'])
            record = SeqRecord(
                seq=sequence,
                id=seq_dict['local_id'],
                description=""  # Empty description to keep the FASTA header clean
            )
            seq_records.append(record)

        # Create a temporary file with .fasta extension
        temp_fasta = tempfile.NamedTemporaryFile(suffix='.fasta', delete=False)

        # Write records to the temporary FASTA file
        SeqIO.write(seq_records, temp_fasta.name, "fasta")
        return temp_fasta.name



