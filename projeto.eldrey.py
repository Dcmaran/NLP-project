def open_files(file_name, type_f):
    file = open(file_name, type_f, encoding='UTF-8')

    return file


def treat_words(word):
    if word.startswith("['"):
        word = str(word)[2:]
        return word
    elif word.endswith("']"):
        word = str(word)[:-2]
        return word
    else:
        return word


def word_file(dictio):
    try:
        fileWord = open_files('peso-palavra.txt', 'r+')
        for line in fileWord.readlines():
            line = line.replace('\n', '')
            line = line.split(', ')
            dictio[line[0]] = line[1]

        return dictio
    except:
        print("Arquivo não encontrado")


def phrase_file(list_phrase, symbols):
    try:    
        filePhrase = open_files('frases-escolhidas.txt', 'r')
        for line in filePhrase.readlines():
            line = line.casefold()
            makeLineTrans = line.maketrans(symbols)
            line = line.translate(makeLineTrans)
            list_phrase.append(line.splitlines())

        return list_phrase
    except:
        print("Arquivo não encontrado")


def add_words(list_words, value):
    global dictWords
    file = open_files('peso-palavra.txt', 'a')
    for word in list_words:
        wordAdd = treat_words(word)
        if wordAdd != ' ':
            file.write('\n{}, {}'.format(wordAdd, value))
            dictWords[wordAdd] = str(value)

    return None


def grade_phrases(list_phrase):
    pValue = 0
    notKnownWord = []
    knownWords = []

    knownWords_tratada = ""
    notKnownWord_tratada = ""
    phrase_tratada = ""

    file_csv = open('calculo_sentimental.csv', 'w+', encoding='UTF-8')
    file_csv.write("Frase, P.Encontradas, C.Sentimental, P.Aprendidas")
    file_csv.write('\n')
    for i in range(len(list_phrase)):
        phrase = str(list_phrase[i])
        phrase = phrase.split(' ')
        for word in phrase:
            wordCheck = treat_words(word)
            if wordCheck in dictWords:
                pValue += int(dictWords.get(wordCheck))
                if wordCheck not in knownWords:
                    knownWords.append(wordCheck)
            else:
                if wordCheck not in notKnownWord:
                    notKnownWord.append(wordCheck)

        pValue = round(pValue / len(phrase))
        
        
        notKnownWord_tratada = '; '.join(notKnownWord)
        phrase_tratada = ' '.join(phrase)
        knownWords_tratada = '; '.join(knownWords)
        file_csv.write("{}, [{}], {}, [{}]".format(phrase_tratada, knownWords_tratada, 
                                                                    pValue, notKnownWord_tratada))
        file_csv.write('\n')
        add_words(notKnownWord, pValue)
        notKnownWord.clear()
        knownWords.clear()

    return None


unwantedSymbols = {'?': '', '!': '', ',': '', '.': '', ':': '', ';': '', '0': '', '1': '', '2': '',
                   '3': '', '4': '', '5': '', '6': '', '7': '', '8': '', '9': ''}

dictWords = {}
listPhrase = []
dictWords = word_file(dictWords)
listPhrase = phrase_file(listPhrase, unwantedSymbols)
grade_phrases(listPhrase)