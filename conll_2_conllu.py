f = open('set.sr.plus.conllu', 'w')
for line in open('set.sr.plus.conll'):
    if line.startswith('#'):
        f.write(line)
    elif line.strip() == '':
        f.write('\n')
    else:
        tid, token, lemma, _, xpos, _, _, ud, upos, misc, ner = line.strip().split('\t')
        ud_head = ud.split(':')[0]
        ud_label = ':'.join(ud.split(':')[1:])
        upos = upos.split('|')
        feats = '|'.join(upos[1:])
        upos = upos[0].split('=')[1]
        misc_list = []
        if misc != '_':
            misc_list.append(misc)
        if ner != 'O':
            misc_list.append('NER='+ner)
        if len(misc_list) == 0:
            misc_list.append('_')
        f.write('\t'.join((tid, token, lemma, upos, xpos, feats, ud_head, ud_label, '_', '|'.join(misc_list)))+'\n')
