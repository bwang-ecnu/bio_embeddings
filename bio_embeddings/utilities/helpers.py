from typing import List
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from bio_embeddings.utilities.exceptions import MissingParameterError
from hashlib import md5
from pandas import DataFrame


def check_required(params: dict, keys: List[str]):
    """
    Verify if required set of parameters is present in configuration

    Parameters
    ----------
    params : dict
        Dictionary with parameters
    keys : list-like
        Set of parameters that has to be present in params

    Raises
    ------
    MissingParameterError
    """
    missing = [k for k in keys if k not in params]

    if len(missing) > 0:
        raise MissingParameterError(
            "Missing required parameters: {} \nGiven: {}".format(
                ", ".join(missing), params
            )
        )


def _assign_hash(sequence_record: SeqRecord) -> SeqRecord:
    sequence_record.id = md5(str(sequence_record.seq).encode()).hexdigest()

    return sequence_record


def read_fasta_file(file_path: str) -> List[SeqRecord]:
    """
    Helper function to read FASTA file.

    Will assign MD5 hash as ID if no if provided for a sequence.

    :param file_path: path to a valid FASTA file
    :return: a list of SeqRecord objects.
    """
    sequence_records = list(SeqIO.parse(file_path, 'fasta'))

    return sequence_records


def reindex_sequences(sequence_records: List[SeqRecord]) -> (SeqRecord, DataFrame):
    """
    Function will re-index the sequence_records IN PLACE! (change the original list!).
    Returns a DataFrame with the mapping.

    :param sequence_records: List of sequence records
    :return: A dataframe with the mapping with key the new ids and a column "original_id" containing the previous id.
    """
    original_ids = [s.id for s in sequence_records]
    sequence_records[:] = map(_assign_hash, sequence_records)
    new_ids = [s.id for s in sequence_records]

    df = DataFrame(original_ids, columns=['original_id'], index=new_ids)

    return df


def write_fasta_file(sequence_records: List[SeqRecord], file_path: str) -> None:
    SeqIO.write(sequence_records, file_path, 'fasta')
    pass