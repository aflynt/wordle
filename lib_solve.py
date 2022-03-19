import subprocess as sp
import re

wdict = '/home/aflynt/ww_words/wordle-answers-alphabetical.txt'
fdict = '/home/aflynt/ww_words/fws.dat'

def findWordsWithSpots(hasSpots, ifile=wdict,
        ofile=fdict):
    #cr= sp.run(["grep",hasSpots,ifile, " > ", f"{ofile}"], capture_output=True,
    cmdList=[
            "grep",
            '^'+hasSpots+'$',
            ifile
            ]
    cmd = ' '.join(cmdList)
    with open(ofile, "w") as f:
        sp.run(cmd, stdout=f, shell=True)

    return

def findYellowWords(spots, ofile=fdict):

    with open(ofile, 'r') as f:
        all_words = f.readlines()

    all_words = [w.strip() for w in all_words]


    bad_words = []
    for w in all_words:
        for i in range(5):
            if w[i] in spots[i]:
                #print(f'match for: |{w}|')
                bad_words.append(w)

    strlist = [w for w in all_words if w not in bad_words]

    if strlist:
        strlist = sorted(list(set(strlist)))

        with open(ofile, "w") as f:
            for w in strlist:
                f.write(w+'\n')

    return strlist

def findWordsWithChars(hasChars):
    if len(hasChars) ==0:
        hasChars = "abcdefghijklmnopqrstuvwxyz"
    hasChars ='['+hasChars+']'
    cr= sp.run(["grep",hasChars,fdict], capture_output=True,
            universal_newlines=True)

    strlist=cr.stdout.split("\n")
    strlist=[s for s in strlist if len(s) > 0]
    return strlist

def findWordsWithoutChars(hasNoChars):
    if len(hasNoChars) ==0:
        hasNoChars = "9"
    hasNoChars ='['+hasNoChars+']'
    cr= sp.run(["grep","-v",hasNoChars,fdict], capture_output=True,
            universal_newlines=True)

    strlist=cr.stdout.split("\n")
    strlist=[s for s in strlist if len(s) > 0]
    return strlist

def printNstrings(strlist,N):

    for i, s in enumerate(strlist):
        if i % N == 0:
            print()
        print(s.lower(),end=' ')
    print()

def writeStrings(strings,ofile):
    with open(ofile, "w") as f:
        for s in strings:
            f.write(s+'\n')

def mkHits(guess):
    ws = []
    wc = []
    nc = []
    word=guess['word']
    fdbk=guess['fdbk']
    for w_c,f_c in zip(word,fdbk):
        if f_c == 'y':
            wc.append(w_c)
            ws.append('.')
        elif f_c == ' ':
            nc.append(w_c)
            ws.append('.')
        else:
            wc.append(w_c)
            ws.append(w_c)
    wss = ''.join(ws)
    wcs = ''.join(wc)
    ncs = ''.join(nc)
    return wss, wcs,ncs

def findWords(hasSpots,hasChars,hasNoChars, spots,
    f1="fws.dat",
    idict=wdict,
    ):

    findWordsWithSpots(hasSpots,idict,f1)

    strlist = findWordsWithChars(hasChars)
    writeStrings(strlist,f1)

    strlist = findWordsWithoutChars(hasNoChars)
    writeStrings(strlist,f1)

    #print('SPOTS = ', spots)
    if spots:
        strlist = findYellowWords(spots)

    return strlist

def find_all_chars_in_word(wtries):
    # chars is word is the wc item [word chars]
    # so collect them
    all_ws = []
    all_wc = []
    all_nc = []

    for wtry in wtries:

        ws, wc, nc = mkHits(wtry)
        all_ws.append(ws)
        all_wc.append(wc)
        all_nc.append(nc)

    return all_ws, all_wc, all_nc

def split_word(word):
    return [char for char in word]

def find_known_spots(aws_list):

    known_spots = split_word('.....')

    #loop over words,
    for word in aws_list:
        word_list = split_word(word)

        # loop thru 5 chars
        for i,word_char in enumerate(word_list):
            if word_char != '.':
                known_spots[i] = word_char


    return ''.join(known_spots)

def get_yellow_list(wtries):
  """
  generate list of ( index, char )
  """
  yellow_list = []

  for wtry in wtries:
      word = wtry['word']
      fdbk = wtry['fdbk']
      for i, char in enumerate(fdbk):
        if char == 'y':
          yellow_list.append( (i, word[i])  )

  # convert to list of 5 lists containing yellow chars per spot
  spot_list = [[],[],[],[],[]]
  for i in range(5):
      spot_list[i] = [ c for idx, c in yellow_list if idx == i]

  for i in range(5):
      #print(f'i={i}, yellow chars = {spot_list[i]}')
      spot_list[i].append('.')
      spot_list[i].append('-')
      spot_list[i].append("'")


  return spot_list

def make_yellow_string(yellow_list):
  spots = [
      [],
      [],
      [],
      [],
      [],
  ]

  # push chars into spots
  for i in range(len(spots)):
    for idx, char in yellow_list:
      if idx == i:
        spots[i].append(char)

  # turn spot lists into strings
  for i in range(len(spots)):
    spot_i_list = spots[i]
    spot_i_str = ''.join(spot_i_list)
    if(len(spot_i_str) == 0):
      spot_i_str = '.'
    else:
      spot_i_str = '['+ spot_i_str + ']'
    spots[i] = spot_i_str

  return ''.join(spots)

def iso_all_chars(wtries):
    # given a bunch of word tries { work, fdbk }

     # get all words spots, all word chars, all words not in
    aws, awc, anc = find_all_chars_in_word(wtries)

    # find set of chars in word
    chars_in_word = ''.join(awc)
    # find set of chars not in word
    chars_not_in_word = ''.join(anc)
    # find known spots for chars
    known_spots = find_known_spots(aws)


    ciw_list = sorted(list(set(split_word(chars_in_word))))
    niw_list = sorted(list(set(split_word(chars_not_in_word))))

    abet = 'abcdefhijklmnopqrstuvwxyz'
    abet_list = split_word(abet)
    abet_left = [char for char in abet_list if char not in niw_list]

    chars_in_word = ''.join(ciw_list)
    chars_not_in_word = ''.join(niw_list)
    abet_left = ''.join(abet_left)

    yeller_list = get_yellow_list(wtries)

    #spots = make_yellow_string(yeller_list)


    return known_spots, chars_in_word, chars_not_in_word, abet_left, yeller_list


