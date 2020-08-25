import pytest

from bio_embeddings.utilities.pipeline import parse_config_file_and_execute_run

ANNOTATIONS = """
identifier,label
QHN70907.1,pos
"""

FASTA = """
>QHN70907.1 spike glycoprotein [Bovine torovirus]
MFLFFCAATILCLWVNSGGAVVVSNETLVFCEPVSYPYSLQVLRSFSQRVNLRTKRAVIIDAWSFAYQIS
TNSLNVNGWYVNFTSPLGWSYPNGKPFGIVLGSDAMMRASQSIFTYDVISYVGQRPNLDCQINDLVNGGL
KNWYSTVRVDNCGNYPCHGGGKPGCSIGQPYMANGVCTRVLSTTQSPGIQYEIYSGQDYAVYQITPYTQY
TVTMPSGTSGYCQQTPLYVECGSWTPYRVHTYGCDKVTQSCKYTISSDWVVAFKSKITAVTLPSDLKVPV
VQKVTKRLGVTSPDYFWLIKQAYQYLSQATISPNYALFSALSNSLYQQSLVLTDLCYGSPFFMARECYNN
ALYLPDAVFTTLFSILFSWDYQVNYPVNNVLQSNETFLQLPTTGYLGQTVSQGRMLNLFKDAIVFLDFYD
TKFYRTNDGPGGDIFAVVVKQAPVIAYSAFRIEQQTGDYLAVKCNGVTQATLAPHSSRVVLLARHMSMWS
IAAANSTTIYCPIYTLTQFGSLDISTSWYFHTLAQPSGPIQQVSMPLLSTAAAGVYMYPMVEHWVTLLTQ
TQDVYQPSMFNMGVNKSVTLTTQLQAYAQVYTAWFLSILYTRLPESRRLTLGAQLTPFIQALLSFRQADI
DATDVDTVARYNVLSLMWGRKYAAVSYNQLPEWSYPLFKGGVGDSMWFRKEISCTTQNPSTSSHFPFIAG
YLDFLDYKYIPKYKDVACPTTMVTPTLLQVYETPQLFVIIVQCVSTTYSWYPGLRNPHTIYRSYKLGTIC
ILVPYSSPTSVYSSFGFFFQSALTIPIVQTTDDILPGCVGFVQDSVFTPCHPSGCPVRNSYDNYIICPGS
SASNYTLRNYHRTTIPVTNVPIDEVPLQLEIPTVSLTSYELKQSESVLLQDIEGGIVVDHNTGSIWYPDG
QAYDVSFYVSVIIRYAPPKLELPSTLANFTSCLDYICFGNQQCRGEAQTFCTSMDYFEQVFNKSLTSLII
ALQDLHYVLKLVLPETTLELTEDTRRRRRAVDEFSDTISLLSESFERFMSPASQAYMANMMWWDEAFDGI
SLPQRTGSILSRTPSLSSTSSWRSYSSRTPLISNVKTPKTTFNVKLSMPKLPKASTLSTIGSVLSSGLSI
ASLGLSIFSIIEDRRVTELTQQQIMALENQITILTDYTEKNFKEIQSFLNTLGQQVQDFSQQVTLSLQQL
FNGLEQITQQLDKSIYYVMAVQQYATYMSSFVNQLNELSQAVYKTQDMYITCIHSLQSGVLSPNCITPAQ
MFHLYQVAKNLSGECQPIFSEREISRFYSLPLVTDAMVHNDTYWFSWSIPITCSNILGSVYKVQPGYIVN
PHHPTSLQYDVPTHVVTSNAGALIFDEHYCDRYNQVYLCTKSAFDLAESSYLTMLYSNQTDNSSLTFHPE
PRPVPCVYLSASALYCYYSDECHQCVIAVGNCTNRTVTYENYTYSIMDPQCRGFDQVTISSPIAIGADFT
ALPSRPPLPLHLSYVNVTFNVTLPNGVNWTDLVLDYSFKDKVYEISKNITQLHEQILQVSNWASGWFQRL
RDFLYGLIPAWITWLTLGFSLFSILISGVNIILFFEMNGKVKKS
"""


@pytest.fixture(scope="session")
def test_files(tmp_path):
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    config_file = test_dir / "config.yml"
    annotations_file = test_dir / "annotation_file.csv"
    fasta_file = test_dir / "fasta.fa"

    CONFIG = f"""
    global:
        sequences_file: {str(fasta_file)}
        prefix: {str(test_dir)}
    seqvec_embeddings:
        type: embed
        protocol: seqvec
        reduce: True
    tsne_projections:
        type: project
        protocol: tsne
        depends_on: seqvec_embeddings
    plotly_visualization:
        type: visualize
        protocol: plotly
        depends_on: tsne_projections
        annotation_file: {str(annotations_file)}
"""

    config_file.write_text(CONFIG)
    annotations_file.write_text(ANNOTATIONS)
    fasta_file.write_text(FASTA)

    return config_file


def simple_behavior_test(test_files):
    """ Run the pipeline using a simple setup once """
    parse_config_file_and_execute_run(test_files, overwrite=True)
