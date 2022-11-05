import networkx as nx
import argparse
import pickle
import spacy
import os


def configure():
    os.system('pip3 install -r requirements.txt')
    os.system('python3 -m spacy download pt_core_news_lg')


def process_file(inpath, file):
    print('processing', file)
    with open(inpath + file) as f:
        text = f.read().split('---')[-1].replace('\n', ' ')
    nlp = spacy.load("pt_core_news_lg")
    nlp.add_pipe('sentencizer')
    return nlp(text)


def get_parents(G, doc):
    for sentence in doc.sents:
        root = sentence.root
        if root.text != 'nasceu': continue
        children = list(root.children)
        node = list(filter(lambda x:x.dep_=='nsubj', children))[0]
        name = ' '.join([t.text for t in node.subtree if t.pos_=='PROPN'])
        G.add_node(name)
        subtree = list(filter(lambda x:x.text.startswith('filh'), children))
        if not len(subtree): continue
        parents = [' '.join([x.text for x in t.subtree if x.pos_=='PROPN']) for t in subtree[0].children if t.pos_=='PROPN']
        for p in parents:
            G.add_edge(p, name)
    return G


def process(inpath, outpath):
    if not inpath: inpath = '../dhbb-1.0.0/text/'
    if not outpath: outpath = ''
    if os.path.isfile(inpath): inlist = [inpath]
    elif os.path.isdir(inpath): inlist = [f for f in os.listdir(inpath) if f.endswith(".text")]
    else: raise Exception('Input file or directory is invalid')
    G = nx.DiGraph()
    for f in inlist:
        doc = process_file(inpath, f)
        G = get_parents(G, doc)
    with open('people_graph.pickle', 'wb') as f:
        pickle.dump(G, f)


if __name__ == '__main__':

    process('test/', '')

    parser = argparse.ArgumentParser(description='Main project module')
    parser.add_argument("-c", "--configure", action="store_true",
        help="configure environment")
    parser.add_argument("-p", "--process", action="store_true",
        help="load sentences from dhbb")
    parser.add_argument('inpath', nargs='?', const=None,
        help='input file or directory path. none for all files')
    parser.add_argument('outpath', nargs='?', const=None,
        help='output file or directory path. none for all files')
    args = parser.parse_args()

    if args.configure: configure()
    elif args.process: process(args.inpath, args.outpath)
    else: parser.print_help()

# ls |sort -R |tail -100 |while read file; do cp $file ../../TCC/test/$file; done