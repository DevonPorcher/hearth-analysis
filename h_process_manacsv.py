import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import Tkinter as tk
import pandas as pd

def mana_analysis(csv_file_name):
    df = pd.read_csv(csv_file_name)

    avg_hp_dif    = df["w_hp_dif"].mean()
    avg_card_dif  = df["w_card_dif"].mean()
    avg_fm_05_dif = df["w_floated_mana_05_dif"].mean()
    avg_fm_10_dif = df["w_floated_mana_10_dif"].mean()
    avg_fm_dif    = df["w_floated_mana_dif"].mean()

    # temp = df["w_floated_mana_10_dif"]
    # low_q = temp.quantile(.05)
    # high_q = temp.quantile(.95)
    # print low_q
    # print high_q
    # filt_df = df[(df["w_floated_mana_10_dif"] > low_q) & (df["w_floated_mana_10_dif"] < high_q)]
    # avg_fm_dif_outlire = filt_df["w_floated_mana_10_dif"].mean()

    print "hero power dif: %s\ncards played dif: %s\nfloated mana turn 5 dif: %s\nfloated mana turn 10 dif: %s\nfloated mana dif: %s" \
    %(avg_hp_dif,avg_card_dif,avg_fm_05_dif,avg_fm_10_dif,avg_fm_dif)

    df["w_floated_mana_dif"].hist(bins=[-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,0, \
                                        5,10,15,20,25,30,35,40,45,50])
    plt.savefig('myfig')

    # print (df.describe())

def main():
    mana_analysis(sys.argv[1])

if __name__== "__main__":
    main()