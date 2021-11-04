# SETimes.SRPlus
An extended and updated version of the original SETimes.SR annotated corpus

`conll_2_conllu.py` is used for transforming the old conll format into the conllu format. The conllu format should be the reference format.

Validating the conllu format can be done with UD tools like this:
```
python ../tools/validate.py --lang SR --level 1 set.sr.plus.conllu
```
This test should be passed completely.

```
python ../tools/validate.py --lang SR --level 2 set.sr.plus.conllu
```
This test should be passed completely as well.

XPOS tags and their mapping to UPOS should be validated as well.
```
python ../hr500k/check_xpos_upos_feats.py ../hr500k/mte5-udv2.mapping set.sr.plus.conllu set.sr.plus.uposxpos.txt |sort|uniq -c
```

Currently the output of this command should be the number of UPOS and XPOS mismatches, something along the line of

```
  33 UPOS Rgc UposTag=DET|Degree=Cmp
  31 UPOS Rgp UposTag=DET|Degree=Pos
   8 UPOS Rgp UposTag=DET|Degree=Pos|PronType=Dem
  69 UPOS Rgp UposTag=DET|Degree=Pos|PronType=Ind
   7 UPOS Rgp UposTag=DET|Degree=Pos|PronType=Int,Rel
   1 UPOS Rgs UposTag=DET|Degree=Sup
   9 UPOS Y UposTag=ADJ|_
   7 UPOS Y UposTag=NOUN|_
   4 UPOS Y UposTag=PROPN|_
   3 XPOS Y UposTag=PART|_
   1 XPOS Y UposTag=PUNCT|_
```
In the file `set.sr.plus.uposxpos.txt` these mismatches can be analysed in context by searching for `UPOS!!!` or `XPOS!!!`.
