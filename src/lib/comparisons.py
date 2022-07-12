# -*- coding: utf-8 -*-
import sys

class JaccardSimilarity():
    """
    Calculates the similarity of two statements based on the Jaccard index.
    The Jaccard index is composed of a numerator and denominator.
    In the numerator, we count the number of items that are shared between the sets.
    In the denominator, we count the total number of items across both sets.
    Let's say we define sentences to be equivalent if 50% or more of their tokens are equivalent.
    Here are two sample sentences:
        The young cat is hungry.
        The cat is very hungry.
    When we parse these sentences to remove stopwords, we end up with the following two sets:
        {young, cat, hungry}
        {cat, very, hungry}
    In our example above, our intersection is {cat, hungry}, which has count of two.
    The union of the sets is {young, cat, very, hungry}, which has a count of four.
    Therefore, our `Jaccard similarity index`_ is two divided by four, or 50%.
    Given our similarity threshold above, we would consider this to be a match.
    .. _`Jaccard similarity index`: https://en.wikipedia.org/wiki/Jaccard_index
    """

    SIMILARITY_THRESHOLD = 0.5

    # def initialize_nltk(self):
    def compare(self, text1, text2):
        from nltk.corpus import wordnet
        import nltk
        import string

        nltk.data.path.append('/app/nltk_data/')
        #nltk.download('all')

        # SET BOTH TEXTS LOWER
        a = text1.lower()
        b = text2.lower()

        # GET STOPWORDS IN PORTUGUESE AND EXTEND WITH PUNCTUATION
        stopwords = nltk.corpus.stopwords.words('portuguese')
        stopwords.extend(string.punctuation)
        stopwords.append('')

        # LEMMATIZER = CHURCHES = CHURCH, DOGS = DOG, .....
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

        def get_wordnet_post(pos_tag):
            if pos_tag[1].startswith('J'):
                return (pos_tag[0],wordnet.ADJ)
            elif pos_tag[1].startswith('V'):
                return (pos_tag[0], wordnet.VERB)
            elif pos_tag[1].startswith('N'):
                return (pos_tag[0], wordnet.NOUN)
            elif pos_tag[1].startswith('R'):
                return (pos_tag[0], wordnet.ADV)
            else:
                return (pos_tag[0], wordnet.NOUN)

        ratio = 0
        pos_a = map(get_wordnet_post,nltk.pos_tag(nltk.tokenize.word_tokenize(a)))
        pos_b = map(get_wordnet_post, nltk.pos_tag(nltk.tokenize.word_tokenize(b)))

        lemma_a = [
            lemmatizer.lemmatize(
                token.strip(string.punctuation),
                pos
            ) for token, pos in pos_a if pos == wordnet.NOUN and token.strip(
            string.punctuation
            ) not in stopwords
        ]

        lemma_b = [
            lemmatizer.lemmatize(
                token.strip(string.punctuation),
                pos
            )
            for token, pos in pos_b if pos == wordnet.NOUN and token.strip(
                    string.punctuation
            ) not in stopwords
        ]

        # CALCULATE JACCARD SIMILARITY
        try:
            numerator   = len(set(lemma_a).intersection(lemma_b))
            denominator = float(len(set(lemma_a).union(lemma_b)))
            ratio       = numerator / denominator
        except Exception as e:
            print('Error', str(e))
        return ratio


from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
import unidecode

class LevenshteinDistance():
    """
    Compare two statements based on the Levenshtein distance
    of each statement's text.
    For example, there is a 65% similarity between the statements
    "where is the post office?" and "looking for the post office"
    based on the Levenshtein distance algorithm.
    """

    def compare(self, text1, text2):
        """
        Compare the two input statements.
        :return: The percent of similarity between the text of the statements.
        :rtype: float
        """

        # Get the lowercase version of both strings
        text1 = unidecode.unidecode(text1.lower()).strip()
        text2 = unidecode.unidecode(text2.lower()).strip()

        if text1.endswith("."):
            text1 = text1[:-1]
        if text2.endswith("."):
            text2 = text2[:-1]

        similarity = SequenceMatcher(
            None,
            text1,
            text2
        )

        # Calculate a decimal percent of the similarity
        percent = round(similarity.ratio(), 2)

        return percent

# ---------------------------------------- ---------------------------------------- ---------------------------------------- #

# TODO: create test
comparator = LevenshteinDistance()
# a = comparator.compare("{entity=city}", "{entity=state}")
# print(a)
