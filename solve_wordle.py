import lib_solve as ls

pwd="/home/aflynt/"
#idict=pwd+"words"
f1="fws.dat"

#wtries = [
#   {
#     'word': 'raise'  ,
#     'fdbk': 'y   y'  ,
#   },
#   {
#     'word': 'foyer'  ,
#     'fdbk': '  yyy'  ,
#   },
#]
wtries = [
    { 'word': 'salet'  , 'fdbk': '   y '  , },
    { 'word': 'proud'  , 'fdbk': '     '  , },
    { 'word': 'filet'  , 'fdbk': ' y y '  , },
    { 'word': 'chins'  , 'fdbk': '  yy '  , },
    { 'word': 'indie'  , 'fdbk': ' y *y'  , },
    { 'word': 'filer'  , 'fdbk': ' y y '  , },
    { 'word': 'cadet'  , 'fdbk': '   y '  , },
]
wtries = [
    { 'word': 'salet'  , 'fdbk': '    g'  , },
    { 'word': 'proud'  , 'fdbk': ' yy  '  , },
    { 'word': 'filet'  , 'fdbk': '    g'  , },
    { 'word': 'chins'  , 'fdbk': '     '  , },
    { 'word': 'indie'  , 'fdbk': '     '  , },
    { 'word': 'filer'  , 'fdbk': '    y'  , },
    { 'word': 'cadet'  , 'fdbk': '    g'  , },
    { 'word': 'begin'  , 'fdbk': 'y    '  , },
]
#wtries = [
#   {
#     'word': 'stain'  ,
#     'fdbk': ' y y '  ,
#   },
#   {
#     'word': 'proud'  ,
#     'fdbk': '     '  ,
#   },
#   {
#     'word': 'thick'  ,
#     'fdbk': 'yyy  '  ,
#   },
#]



def get_word_lists(wtries):
    strlists = []
    print(f' {"SPOTS"}  {"HAS":5s}  {"Doesnt Have":20s} May have')
    for i in range(len(wtries)):
        ws, wc, nc, al,spots = ls.iso_all_chars(wtries[0:i+1])

        strlist = ls.findWords(ws,wc,nc, spots)
        strlists.append(strlist)
        nstr = len(strlist)

        print(f' {ws:5s}  {wc:5s}  {nc:15s}  {al:26s} nwords =', end="")
        print(f' {nstr:4d}  for {wtries[i]["word"]}')

    return strlists


def report_word_list(strlists):
    print()
    for i,strlist in enumerate(strlists):
        nstr = len(strlist)
        if nstr < 200:
            ls.printNstrings(strlist,16)
        else:
            print('[long list]')


strlists = get_word_lists(wtries)
report_word_list(strlists)

