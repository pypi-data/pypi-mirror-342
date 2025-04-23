import os
from xldg.data import Path, MeroX, CrossLink, ProteinStructure, ProteinChain, Domain, Fasta
from xldg.graphics import VennConfig, Venn2, Venn3

if __name__ == "__main__":
    # Circos
    cwd = os.path.join(r'D:\2025-04-03_Meeting-Oleksandr\ZHRM\Shp2\unselected')
    crosslink_files = Path.list_given_type_files(cwd, 'zhrm')
    crosslinks = MeroX.load_data(crosslink_files, 'DSBU')
    crosslinks = CrossLink.filter_by_score(crosslinks, 50)

    config = VennConfig('Title1', 'Title2', 'Title3', title='Title')

    venn2 = Venn2(crosslinks[0], crosslinks[1], config)
    venn2.save(os.path.join(cwd, 'venn2.svg'))

    venn3 = Venn3(crosslinks[0], crosslinks[1], crosslinks[2], config)
    venn3.save(os.path.join(cwd, 'venn3.svg'))
