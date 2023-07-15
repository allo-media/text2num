#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from text_to_num import alpha2digit

phrase = "Do dziesięciu","Do jedenastu","Do dwunastu","Do trzynastu ", \
 "Do czternastu","Do piętnastu","Do szesnastu","Do siedemnastu","Do osiemnastu","Do dziewiętnastu", \
 "Do dwudziestu","Do trzydziestu","Do czterdziestu","Do pięćdziesięciu","Do sześćdziesieciu", \
 "Do siedemdziesieciu","Do osiemdziesieciu","Do dziewięćdziesięciu", \
 "Mamy jeden tysiąc","Do jednego tysiąca", \
 "Do pięćdziesięciu dwóch tysięcy","Mamy dwadzieścia dwa tysiące","Trzeba dwudziestu dwóch tysięcy"

for p in phrase:
    recognized = alpha2digit(p ,"pl")
    print(p, "\t", recognized)
    print()
