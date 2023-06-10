#
# Model, analyze, & score the similarity of text samples
#

import math

# function0
def clean_text(txt):
    """ returns a list of the words in txt after it has been cleaned
        input: str text txt
    """
    text = txt.lower()
    
    for symbols in """.,?"'!;:""":
        text = text.replace(symbols, '')

    return text.split()

# function1
def stem(s):
    """ return the stem of s
        input: str s
    """
    if s in ['they', 'them', 'themselves']:
        word = s
    elif len(s) <= 3:
        word = s
    elif s[-1] == 's':
        stem_rest = stem(s[:-1])
        return stem_rest
    elif s[-2:] == 'er':
        word = s[:-2] 
    elif s[-2:] == 'ed':
        word = s[:-2]
    elif s[-3:] == 'ing':
        if len(s) == 4:
            word = s
        else:
            if s[-4] == s[-5]:
                word = s[:-4]
            else:
                word = s[:-3]
    elif s[-2:] == 'ly':
        stem_rest = stem(s[:-2])
        return stem_rest
    elif s[-3:] == 'ful':
        word = s[:-3]
    else:
        return s
    
    return word
    
# function2
def compare_dictionaries(d1, d2):
    """ computes & returns the log similarity score
        input: dict d1 & d2
    """
    if d1 == {}:
        return -50
 
    log_sim_score = 0
    total = 0
    for key in d1:
        total += d1[key]
    
    for key in d2:
        if key in d1:
            prob = (d1[key] / total)
            log_sim_score += math.log(prob) * d2[key]
        else:
            prob = (0.5 / total)
            log_sim_score += math.log(prob) * d2[key]
    
    return log_sim_score

class TextModel:
    """ a data type for objects that model a body of text
    """
    def __init__(self, model_name):
        """ constructs a new TextModel object by initializing an attribute 
            name (str, a label for this text model),
            words (dict, # of each word appears),
            word_lengths (dict, # of each word length appears)
            stems (dict, # of each word stem appears)
            sentence_lengths (dict, # of each sentence length)
            personal_pn (dict, # of each personal pronouns)
            input: str model_name
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.personal_pns = {}
    
    def __repr__(self):
        """ returns a string that includes the name of the model as well as
            the sizes of the dict for each feature of the text
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' \
                + str(len(self.sentence_lengths)) + '\n'
        s += '  number of personal pronouns: ' + str(len(self.personal_pns))
        
        return s
    
    def add_string(self, s):
        """ analyzes the str text and adds its pieces to all of the dict
            in this text model / adds a str of text s to the model
            input: str s
        """
        words = s.split()
        total_words = len(words)
        
        word_count = 0
        for w in words:
            word_count += 1
            if w[-1] in '.?!' or word_count == total_words:
                if word_count not in self.sentence_lengths:
                    self.sentence_lengths[word_count] = 1
                else:
                    self.sentence_lengths[word_count] += 1 
                total_words -= word_count
                word_count = 0

        word_list = clean_text(s)
        personal_pns_list = ['i', 'you', 'he', 'she', 'it', 'we', 'they', \
                            'me', 'him', 'her', 'us', 'them']
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
            if w in personal_pns_list:
                if w not in self.personal_pns:
                    self.personal_pns[w] = 1
                else:
                    self.personal_pns[w] += 1
    
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename
            to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        
        self.add_string(text)
        
    def save_model(self):
        """ saves the TextModel by writing its various feature dict to files
        """
        file_w = self.name + '_words'
        file_wl = self.name + '_word_lengths'
        file_stem = self.name + '_stems'
        file_sl = self.name + '_sentence_lengths'
        file_pn = self.name + '_personal_pronouns'
        
        f_w = open(file_w, 'w')
        f_w.write(str(self.words))
        f_w.close()
        
        f_wl = open(file_wl, 'w')
        f_wl.write(str(self.word_lengths))
        f_wl.close
        
        f_stem = open(file_stem, 'w')
        f_stem.write(str(self.stems))
        f_stem.close()
        
        f_sl = open(file_sl, 'w')
        f_sl.write(str(self.sentence_lengths))
        f_sl.close()
        
        f_pn = open(file_pn, 'w')
        f_pn.write(str(self.personal_pns))
        f_pn.close()
    
    def read_model(self):
        """ reads the stored dict for the called TextModel from their files
            and assigns them to the attributes of the called object
        """
        file_w = self.name + '_words'
        file_wl = self.name + '_word_lengths'
        file_stem = self.name + '_stems'
        file_sl = self.name + '_sentence_lengths'
        file_pn = self.name + '_personal_pronouns'
        
        f_w = open(file_w, 'r')
        word_str = f_w.read()
        f_w.close()
        d_w = dict(eval(word_str))
        self.words = d_w
        
        f_wl = open(file_wl, 'r')
        word_lengths_str = f_wl.read()
        f_wl.close()
        d_wl = dict(eval(word_lengths_str))
        self.word_lengths = d_wl
        
        f_stem = open(file_stem, 'r')
        stem_str = f_stem.read()
        f_stem.close()
        d_stem = dict(eval(stem_str))
        self.stems = d_stem
        
        f_sl = open(file_sl, 'r')
        sl_str = f_sl.read()
        f_sl.close()
        d_sl = dict(eval(sl_str))
        self.sentence_lengths = d_sl
        
        f_pn = open(file_pn, 'r')
        pn_str = f_pn.read()
        f_pn.close()
        d_pn = dict(eval(pn_str))
        self.personal_pns = d_pn
    
    def similarity_scores(self, other):
        """ computes & returns a list of log_sim_scores measuring
            the similarity of self & other-one score for each type of feature
            input: dict other
        """
        scores = []
        scores += [compare_dictionaries(other.words, self.words)]
        scores += [compare_dictionaries(other.word_lengths, \
                                        self.word_lengths)]
        scores += [compare_dictionaries(other.stems, self.stems)]
        scores += [compare_dictionaries(other.sentence_lengths, \
                                       self.sentence_lengths)]
        scores += [compare_dictionaries(other.personal_pns, \
                                        self.personal_pns)]
        
        return scores
    
    def classify(self, source1, source2):
        """ compares & determines the called TextModel object to
            two other source objects & find out which source is more likely
            source of the called TextModel
            input: object source1 & source2
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))
        
        weighted_sum1 = len(self.words) * scores1[0] + \
                        len(self.word_lengths) * scores1[1] + \
                        len(self.stems) * scores1[2] + \
                        len(self.sentence_lengths) * scores1[3] + \
                        len(self.personal_pns) * scores1[4]
        weighted_sum2 = len(self.words) * scores2[0] + \
                        len(self.word_lengths) * scores2[1] + \
                        len(self.stems) * scores2[2] + \
                        len(self.sentence_lengths) * scores2[3] + \
                        len(self.personal_pns) * scores2[4]
        
        if weighted_sum1 > weighted_sum2:
            print(self.name + ' is more likely to have come from ' + \
                  source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + \
                  source2.name)

# testing
def test():
    """ performs test calls on the function above """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ performs test calls on the function above """
    # model 1
    source1 = TextModel('jkr')
    source1.add_file('jkr.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare.txt')

    new1 = TextModel('wr120')
    new1.add_file('wr120.txt')
    new1.classify(source1, source2)
    print()
    
    # model 2
    source3 = TextModel('friends')
    source3.add_file('friends.txt')

    source4 = TextModel('how_i_met_your_mother')
    source4.add_file('how_mother_pineapple_incident.txt')
    source4.add_file('how_mother_zipzipzip.txt')
    
    new2 = TextModel('pilot')
    new2.add_file('pilot_hm.txt')
    new2.classify(source3, source4)
    print()
    
    # model 3
    source5 = TextModel('vogue')
    source5.add_file('vogue.txt')

    source6 = TextModel('mit_tech_review')
    source6.add_file('mit_tech_review.txt')
    
    new3 = TextModel('elle')
    new3.add_file('elle.txt')
    new3.classify(source5, source6)
    print()
    
    # model 4
    source7 = TextModel('michelle_obama_ted')
    source7.add_file('michelle_obama_ted.txt')

    source8 = TextModel('mark_zuckerberg')
    source8.add_file('mark_zuckerberg.txt')
    
    new4 = TextModel('cnn_speech_mo')
    new4.add_file('cnn_speech_mo.txt')
    new4.classify(source7, source8)
    print()
    
    # compare
    new1.classify(source1, source6)
    print()
    new2.classify(source3, source6)
    print()
    new3.classify(source5, source8)
    print()
    new4.classify(source7, source4)    