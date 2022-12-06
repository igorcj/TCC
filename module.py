import networkx as nx
import argparse
import pickle
import spacy
import os
import re


def configure():
    os.system('pip3 install -r requirements.txt')
    os.system('python3 -m spacy download pt_core_news_lg')

def regularize_name(name):
    if ',' in name:
        name = name.split(',')
        name = ' '.join([name[-1]] + name[:-1])
    return re.sub(' +', ' ', re.sub(r'[^A-Za-z\u00C0-\u00FF ]+', '', name)).strip().lower()

def get_subject(d):
    info = dict([map(lambda k:k.strip(), x.split(':')) for x in d.split('\n') if x != '' and ':' in x])
    if info.get('natureza') == 'biográfico': return regularize_name(info['title'])
    else: return

def process_file(inpath, file):
    print('processing', file)
    with open(inpath + file) as f:
        d = f.read().split('---')
    subject = get_subject(d[-2])
    text = d[-1].replace('\n', ' ')
    nlp = spacy.load("pt_core_news_lg")
    nlp.add_pipe('sentencizer')
    return subject, nlp(text)

def get_parents(G, doc):
    for sentence in doc.sents:
        root = sentence.root
        if root.text != 'nasceu': continue
        children = list(root.children)
        node = list(filter(lambda x:x.dep_=='nsubj', children))
        if node == []: continue
        node = node[0]
        name = regularize_name(' '.join([t.text for t in node.subtree if t.pos_=='PROPN']))
        G.add_node(name)
        subtree = list(filter(lambda x:x.text.startswith('filh'), children))
        if not len(subtree): continue
        parents = [' '.join([x.text for x in t.subtree if x.pos_=='PROPN']) for t in subtree[0].children if t.pos_=='PROPN']
        for p in parents:
            G.add_edge(regularize_name(p), name)
    return G

def get_people(G, doc, subject):
    people = [regularize_name(ent.text) for ent in doc.ents if ent.label_ == 'PER']
    for p in people:
        G.add_edge(subject, p)
    return G

def process(inpath, outpath):
    if not inpath: inpath = '../dhbb-1.0.0/text/'
    if not outpath: outpath = ''
    if os.path.isfile(inpath): inlist = [inpath]
    elif os.path.isdir(inpath): inlist = [f for f in os.listdir(inpath) if f.endswith(".text")]
    else: raise Exception('Input file or directory is invalid')

    P = nx.DiGraph()
    G = nx.MultiDiGraph()
    for f in inlist:
        subject, doc = process_file(inpath, f)
        if not subject: continue
        P = get_parents(P, doc)
        G = get_people(G, doc, subject)

    with open('parent_graph.pickle', 'wb') as f:
        pickle.dump(P, f)
    with open('people_graph.pickle', 'wb') as f:
        pickle.dump(G, f)


if __name__ == '__main__':

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

# data = pd.DataFrame(sorted(G.degree, key=lambda x:-x[1]), columns=['Nome','Citações'])
# data.drop(1).drop(2).drop(3).drop(4).drop(13).head(10)

# pr = pd.DataFrame(sorted(nx.pagerank(G).items(), key=lambda x:-x[1]), columns=['Nome', 'PageRank'])
# pr.drop(0).drop(1).drop(2).drop(6).drop(7).drop(8).drop(13).drop(14).drop(16).drop(17).head(10)

# cc = sorted([(len(x), x) for x in nx.connected_components(G.to_undirected())], reverse=True)
# comp = pd.DataFrame(cc, columns=['lenght', 'elements'])

# sobrenomes = Counter([x for node in P.nodes for x in node.split(' ')])