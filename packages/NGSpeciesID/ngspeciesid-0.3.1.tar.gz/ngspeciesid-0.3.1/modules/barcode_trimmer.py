
import edlib
import logging

from modules import help_functions

def reverse_complement(string):
    #rev_nuc = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N', 'X':'X'}
    # Modified for Abyss output
    rev_nuc = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'a':'t', 'c':'g', 'g':'c', 't':'a', 'N':'N', 'X':'X', 'n':'n', 'Y':'R', 'R':'Y', 'K':'M', 'M':'K', 'S':'S', 'W':'W', 'B':'V', 'V':'B', 'H':'D', 'D':'H', 'y':'r', 'r':'y', 'k':'m', 'm':'k', 's':'s', 'w':'w', 'b':'v', 'v':'b', 'h':'d', 'd':'h'}

    rev_comp = ''.join([rev_nuc[nucl] for nucl in reversed(string)])
    return(rev_comp)

def read_barcodes(primer_file):
    barcodes = { acc + '_fw' : seq.strip() for acc, (seq, _) in help_functions.readfq(open(primer_file, 'r'))}

    for acc, seq in list(barcodes.items()):
        logging.debug(f"{acc} {seq} {acc[:-3]}")
        barcodes[acc[:-3] + '_rc'] = reverse_complement(seq.upper())

    logging.debug(f"{barcodes}")
    return barcodes

def get_universal_tails():
    barcodes = {'1_F_fw' : 'TTTCTGTTGGTGCTGATATTGC',
                 '2_R_rc' : 'ACTTGCCTGTCGCTCTATCTTC'}
    barcodes['1_F_rc'] = reverse_complement(barcodes['1_F_fw'])
    barcodes['2_R_fw'] = reverse_complement(barcodes['2_R_rc'])
    logging.debug(f"{barcodes}")
    return barcodes


def find_barcode_locations(center, barcodes, primer_max_ed):
    "Find barcodes in a center using edlib"
    
    # Creation of a IUPAC equivalence map for edlib to allow IUPAC code in primers
    # The IUPAC map was created with:
    # from Bio.Data import IUPACData
    # IUPAC_map = [(i, k) for i, j in IUPACData.ambiguous_dna_values.items() for k in j]
    IUPAC_map = [('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T'), ('M', 'A'), ('M', 'C'),
                 ('R', 'A'), ('R', 'G'), ('W', 'A'), ('W', 'T'), ('S', 'C'), ('S', 'G'),
                 ('Y', 'C'), ('Y', 'T'), ('K', 'G'), ('K', 'T'), ('V', 'A'), ('V', 'C'),
                 ('V', 'G'), ('H', 'A'), ('H', 'C'), ('H', 'T'), ('D', 'A'), ('D', 'G'),
                 ('D', 'T'), ('B', 'C'), ('B', 'G'), ('B', 'T'), ('X', 'G'), ('X', 'A'),
                 ('X', 'T'), ('X', 'C'), ('N', 'G'), ('N', 'A'), ('N', 'T'), ('N', 'C')]
    all_locations = []
    for primer_acc, primer_seq in barcodes.items():
        # Add additionalEqualities=IUPAC_map allow edlib to understand IUPAC code
        result = edlib.align(primer_seq, center,
                             mode="HW", task="locations", k=primer_max_ed,
                             additionalEqualities=IUPAC_map)
        ed = result["editDistance"]
        locations = result["locations"]
        logging.debug(f"{locations} {ed}")
        if locations:
            all_locations.append((primer_acc, locations[0][0], locations[0][1], ed))
    return all_locations


def remove_barcodes(centers, barcodes, args):
    """
        Modifies consensus sequences by copping of at barcode sites.
        This implies changing the datastructure centers with the modified consensus sequeces
    """

    centers_updated = False
    for i, (nr_reads_in_cluster, c_id, center, reads_path_name) in enumerate(centers):

        # if consensus is smaller than 2*trim_window we set trim window to half the sequence
        if 2*args.trim_window > len(center):
            trim_window = len(center)//2
        else:
            trim_window = args.trim_window

        barcode_locations_beginning = find_barcode_locations(center[:trim_window], barcodes, args.primer_max_ed) 
        barcode_locations_end = find_barcode_locations(center[-trim_window:], barcodes, args.primer_max_ed) 
        logging.debug(f"{center}")
        
        cut_start = 0
        if barcode_locations_beginning:
            logging.debug(f"FOUND BARCODE BEGINNING {barcode_locations_beginning}")
            for bc, start, stop, ed in barcode_locations_beginning:
                if stop > cut_start:
                    cut_start = stop
            
        cut_end = len(center)
        if barcode_locations_end:
            logging.debug(f"FOUND BARCODE END {barcode_locations_end}")
            earliest_hit = len(center)
            for bc, start, stop, ed in barcode_locations_end:
                if start < earliest_hit:
                    earliest_hit = start
            cut_end = len(center) - (trim_window - earliest_hit)

        if cut_start > 0 or cut_end < len(center):
            center = center[cut_start: cut_end]

            logging.debug(f"{center} NEW")
            logging.debug(f"cut start {cut_start} cut end {cut_end}")
            centers[i][2] = center
            centers_updated = True

    return centers_updated
