#!/usr/bin/env python3

import argparse, csv, sys
import os 
os.chdir('D:\\pySourecode\\kaggle-2014-criteo-master\\')
from converters.common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

#from common import *

#parser = argparse.ArgumentParser()
#parser.add_argument('-n', '--nr_bins', type=int, default=int(1e+6))
#parser.add_argument('-t', '--threshold', type=int, default=int(10))
#parser.add_argument('csv_path', type=str)
#parser.add_argument('gbdt_path', type=str)
#parser.add_argument('out_path', type=str)
#args = vars(parser.parse_args())

args={"nr_bins":20,"threshold":10,"csv_path":"tr.csv","gbdt_path":"tr.gbdt.out","out_path":"tr.ffm"}
#args={"nr_thread":20,"cvt_path":"converters/pre-b.py","src1_path":"tr.csv","src2_path":"tr.gbdt.out","dst_path":"tr.ffm"}

def gen_hashed_fm_feats(feats, nr_bins):
    feats = ['{0}:{1}:1'.format(field-1, hashstr(feat, nr_bins)) for (field, feat) in feats]
    return feats
#
#def read_freqent_feats(threshold=10):
#    frequent_feats = set()
#    for row in csv.DictReader(open('fc.trva.t10.txt')):
#        if int(row['Total']) < threshold:
#            continue
#        frequent_feats.add(row['Field']+'-'+row['Value'])
#    return frequent_feats

frequent_feats = read_freqent_feats(args['threshold'])
print(1222)
with open(args['out_path'], 'w') as f:
    for row, line_gbdt in zip(csv.DictReader(open(args['csv_path'])), open(args['gbdt_path'])):
#        break
        feats = []
#        print(row)
#        print(line_gbdt)
        for feat in gen_feats(row):
#            break
            field = feat.split('-')[0]
            type, field = field[0], int(field[1:])
            
            if type == 'C' and feat not in frequent_feats:
                feat = feat.split('-')[0]+'less'
                print(feat)
            if type == 'C':
                field += 13
            feats.append((field, feat))

        for i, feat in enumerate(line_gbdt.strip().split()[1:], start=1):
            field = i + 39
            feats.append((field, str(i)+":"+feat))

#        feats = gen_hashed_fm_feats(feats, args['nr_bins'])
        print(row['Label'] + ' ' + str(feats) + '\n')
        break
#        break
#        f.write(row['Label'] + ' ' + ' '.join(feats) + '\n')
