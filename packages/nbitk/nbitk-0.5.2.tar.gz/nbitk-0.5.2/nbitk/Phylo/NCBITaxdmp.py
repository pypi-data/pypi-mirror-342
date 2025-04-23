import ete3.ncbi_taxonomy.ncbiquery as nt
from Bio.Phylo import BaseTree
from nbitk.Taxon import Taxon
import sys
import logging
from io import StringIO
from contextlib import contextmanager


def _recurse_tree(bp_parent, ete3_parent):

    # iterate over children in ete3 node
    for ete3_child in ete3_parent.children:

        # create a Taxon object for each child
        bp_child = Taxon(
            name=ete3_child.taxname,
            taxonomic_rank=ete3_child.rank,
            guids={"taxon": ete3_child.name},
        )
        bp_parent.clades.append(bp_child)
        _recurse_tree(bp_child, ete3_child)


class LoggerWriter:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.buffer = StringIO()

    def write(self, message):
        self.buffer.write(message)
        if message.endswith("\n"):
            self.flush()

    def flush(self):
        self.logger.log(self.level, self.buffer.getvalue().strip())
        self.buffer.truncate(0)
        self.buffer.seek(0)


@contextmanager
def stdout_to_logger(logger, level=logging.INFO):
    original_stdout = sys.stdout
    try:
        sys.stdout = LoggerWriter(logger, level)
        yield
    finally:
        sys.stdout = original_stdout


class Parser:
    def __init__(self, file):
        self.file = file

    def parse(self):

        # Load nodes.dmp and names.dmp via ETE3, capture output to logger
        logger = logging.getLogger(__name__)
        with stdout_to_logger(logger):
            tree, synonyms = nt.load_ncbi_tree_from_dump(self.file)

        # Create a new base tree and root node
        root = Taxon(name=tree.taxname, taxonomic_rank=tree.rank, guids={"taxon": tree.name})
        bt = BaseTree.Tree(root)

        # Recursively traverse the tree and create Taxon objects
        _recurse_tree(root, tree)

        # Done.
        return bt
