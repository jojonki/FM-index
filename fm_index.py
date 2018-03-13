import sys
from tqdm import tqdm
from itertools import groupby
from operator import itemgetter



class FMIndex:
    # ref https://www.cs.jhu.edu/~langmea/resources/lecture_notes/bwt_and_fm_index.pdf
    def __init__(self):
        self.marker = '$'

    def encode(self, text):
        self.text_len = len(text)
        print('get sa...')
        sa, _, _ = self.suffix_array(text)
        self.sa = sa # TODO reduce memory footprint
        print('get bwt...')
        self.bwt = self.bwt_via_sa(text, sa)
        return self.bwt, self.sa

    def set_dict(self, data):
        if 'bwt' in data:
            self.bwt = data['bwt']
        if 'sa' in data:
            self.sa = data['sa']
        if 'text_len' in data:
            self.text_len = data['text_len']
        if 'ch_count' in data:
            self.ch_count = data['ch_count']

    def decode(self, bwt):
        ranks, ch_count = self.rank_bwt(bwt)
        self.ch_count = ch_count
        first = self.first_col(ch_count)
        t = self.marker
        row_i = 0
        while bwt[row_i] != self.marker:
            c = bwt[row_i]
            t = c + t
            row_i = first[c][0] + ranks[row_i]
        assert (len(t) - 1) == self.text_len

        if t[-1] == self.marker:
            t = t[:-1]
        return t

    # def suffix_array(self, t):
    #     print('----1', len(t), ', size', sys.getsizeof(t))
    #
    #
    #     sfxes = [t[i:] for i in tqdm(range(len(t)))]
    #     print('----2')
    #     # The first value [len(t)] is for marker '$'
    #     # Force to set '$' to the 0th position
    #     return [len(t)] + [i[0] for i in sorted(enumerate(sfxes), key=lambda x:x[1])]

    def longest_common_substring(self, text):
        """Get the longest common substrings and their positions.
        >>> longest_common_substring('banana')
        {'ana': [1, 3]}
        >>> text = "not so Agamemnon, who spoke fiercely to "
        >>> sorted(longest_common_substring(text).items())
        [(' s', [3, 21]), ('no', [0, 13]), ('o ', [5, 20, 38])]

        This function can be easy modified for any criteria, e.g. for searching ten
        longest non overlapping repeated substrings.
        """
        sa, rsa, lcp = self.suffix_array(text)
        maxlen = max(lcp)
        result = {}
        for i in range(1, len(text)):
            if lcp[i] == maxlen:
                j1, j2, h = sa[i - 1], sa[i], lcp[i]
                assert text[j1:j1 + h] == text[j2:j2 + h]
                substring = text[j1:j1 + h]
                if not substring in result:
                    result[substring] = [j1]
                result[substring].append(j2)
        return dict((k, sorted(v)) for k, v in result.items())

    def suffix_array(self, text, _step=16):
        """Analyze all common strings in the text.

        Short substrings of the length _step a are first pre-sorted. The are the 
        results repeatedly merged so that the garanteed number of compared
        characters bytes is doubled in every iteration until all substrings are
        sorted exactly.

        Arguments:
            text:  The text to be analyzed.
            _step: Is only for optimization and testing. It is the optimal length
                   of substrings used for initial pre-sorting. The bigger value is
                   faster if there is enough memory. Memory requirements are
                   approximately (estimate for 32 bit Python 3.3):
                       len(text) * (29 + (_size + 20 if _size > 2 else 0)) + 1MB

        Return value:      (tuple)
          (sa, rsa, lcp)
            sa:  Suffix array                  for i in range(1, size):
                   assert text[sa[i-1]:] < text[sa[i]:]
            rsa: Reverse suffix array          for i in range(size):
                   assert rsa[sa[i]] == i
            lcp: Longest common prefix         for i in range(1, size):
                   assert text[sa[i-1]:sa[i-1]+lcp[i]] == text[sa[i]:sa[i]+lcp[i]]
                   if sa[i-1] + lcp[i] < len(text):
                       assert text[sa[i-1] + lcp[i]] < text[sa[i] + lcp[i]]
        >>> suffix_array(text='banana')
        ([5, 3, 1, 0, 4, 2], [3, 2, 5, 1, 4, 0], [0, 1, 3, 0, 0, 2])

        Explanation: 'a' < 'ana' < 'anana' < 'banana' < 'na' < 'nana'
        The Longest Common String is 'ana': lcp[2] == 3 == len('ana')
        It is between  tx[sa[1]:] == 'ana' < 'anana' == tx[sa[2]:]
        """
        tx = text
        size = len(tx)
        step = min(max(_step, 1), len(tx))
        sa = list(range(len(tx)))
        sa.sort(key=lambda i: tx[i:i + step])
        grpstart = size * [False] + [True]  # a boolean map for iteration speedup.
        # It helps to skip yet resolved values. The last value True is a sentinel.
        rsa = size * [None]
        stgrp, igrp = '', 0
        for i, pos in enumerate(sa):
            st = tx[pos:pos + step]
            if st != stgrp:
                grpstart[igrp] = (igrp < i - 1)
                stgrp = st
                igrp = i
            rsa[pos] = igrp
            sa[i] = pos
        grpstart[igrp] = (igrp < size - 1 or size == 0)
        while grpstart.index(True) < size:
            # assert step <= size
            nextgr = grpstart.index(True)
            while nextgr < size:
                igrp = nextgr
                nextgr = grpstart.index(True, igrp + 1)
                glist = []
                for ig in range(igrp, nextgr):
                    pos = sa[ig]
                    if rsa[pos] != igrp:
                        break
                    newgr = rsa[pos + step] if pos + step < size else -1
                    glist.append((newgr, pos))
                glist.sort()
                for ig, g in groupby(glist, key=itemgetter(0)):
                    g = [x[1] for x in g]
                    sa[igrp:igrp + len(g)] = g
                    grpstart[igrp] = (len(g) > 1)
                    for pos in g:
                        rsa[pos] = igrp
                    igrp += len(g)
            step *= 2
        del grpstart
        # create LCP array
        lcp = size * [None]
        h = 0
        for i in range(size):
            if rsa[i] > 0:
                j = sa[rsa[i] - 1]
                while i != size - h and j != size - h and tx[i + h] == tx[j + h]:
                    h += 1
                lcp[rsa[i]] = h
                if h > 0:
                    h -= 1
        if size > 0:
            lcp[0] = 0
        return sa, rsa, lcp

    def bwt_via_sa(self, t, sa):
        bwt = []
        for si in sa:
            if si == 0:
                bwt += self.marker
            else:
                bwt += t[si - 1]
        self.bwt = bwt
        return self.bwt

    def rank_bwt(self, bw):
        ch_count = {}
        ranks = []
        for c in bw:
            if c not in ch_count:
                ch_count[c] = 0
            ranks.append(ch_count[c])
            ch_count[c] += 1
        return ranks, ch_count

    def first_col(self, ch_count):
        # F must start from '$' marker
        F = {self.marker: 1}
        offset = 1
        for c, count in sorted(ch_count.items()):
            if c != self.marker: # Ignore '$' because we already add ther marker to F
                F[c] = (offset, offset + count)
                offset += count
        return F

    def rank(self, c, k):
        return self.bwt[:k].count(c)

    def rank_lt(self, c):
        # TODO impl better way
        assert self.ch_count is not None
        F = self.first_col(self.ch_count)
        if c in F:
            return F[c][0]
        else:
            return None

    def search(self, pat):
        assert self.bwt is not None
        assert self.sa is not None

        # F = self.first_col(self.ch_count)
        # L = self.bwt
        begin = 0
        end = len(self.bwt)
        for c in pat[::-1]:
            offset = self.rank_lt(c)
            if offset is None:
                begin, end = None, None
                break
            begin = offset + self.rank(c, begin)
            end   = offset + self.rank(c, end)
            if begin >= end: # no results
                begin, end = None, None
                break
        # print('[bwt] (begin, end)', begin, end)
        match = []
        if begin is not None and end is not None:
            for i in range(begin, end):
                match.append((self.sa[i], self.sa[i] + len(pat)))
        return match
