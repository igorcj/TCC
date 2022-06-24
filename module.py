import argparse
import os.path
import spacy


def extract(inpath, outpath):
    if not inpath: inpath = '../dhbb-1.0.0/text/'
    if not outpath: outpath = 'raw/'
    if os.path.isfile(inpath): inlist = [inpath]
    elif os.path.isdir(inpath): inlist = [1,2,3]
    else: raise Exception('Input file or directory is invalid')


    print(inlist)


def transform():
    print('transform')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Main project module')
    parser.add_argument("-e", "--extract", action="store_true",
        help="load sentences from dhbb")
    parser.add_argument("-t", "--transform", action="store_true",
        help="transform sentences from dhbb")
    parser.add_argument('inpath', nargs='?', const=None,
        help='input file or directory path. none for all files')
    parser.add_argument('outpath', nargs='?', const=None,
        help='output file or directory path. none for all files')
    args = parser.parse_args()

    if args.extract: extract(args.inpath, args.outpath)
    elif args.transform: transform()
    else: parser.print_help()




# >>> with open('../dhbb-1.0.0/text/5458.text') as f:
# ...     d = f.read()
# ... 
# >>> p = d.split('\n\n')[1]
# >>> s = p.replace('\n',' ').split('.')[0]
# >>> s
# '«Getúlio Dornelles Vargas» nasceu em São Borja (RS) no dia 19 de abril de 1882, filho de Manuel do Nascimento Vargas e de Cândida Dornelles Vargas'
# >>> doc = nlp(s)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'nlp' is not defined
# >>> import spacy
# >>> nlp = spacy.load("pt_core_news_lg")
# >>> doc = nlp(s)
# >>> for token in doc:
# ...     if token.pos_=='PROPN': print(token.text, token.pos_, token.dep_)
# ...