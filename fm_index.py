class FMIndex:
    # ref https://www.cs.jhu.edu/~langmea/resources/lecture_notes/bwt_and_fm_index.pdf
    def __init__(self):
        self.marker = '$'

    def encode(self, text):
        if text[-1] != self.marker:
            text += self.marker
            self.text = text

        # self.encode(self.text)
        sa = self.suffix_array(text)
        self.sa = sa # TODO reduce memory footprint
        # print('sa', sa)
        self.bwt = self.bwt_via_sa(text, sa)
        return self.bwt, self.sa

    def set_dict(self, data):
        if 'bwt' in data:
            self.bwt = data['bwt']
        if 'sa' in data:
            self.sa = data['sa']

    def decode(self, bwt):
        ranks, ch_count = self.rank_bwt(bwt)
        # print('ranks', ranks)
        # print('ch_count', ch_count)
        self.ch_count = ch_count
        first = self.first_col(ch_count)
        # print('first', first)
        t = self.marker
        row_i = 0
        while bwt[row_i] != self.marker:
            c = bwt[row_i]
            t = c + t
            row_i = first[c][0] + ranks[row_i]

        if t[-1] == self.marker:
            t = t[:-1]
        return t

    def suffix_array(self, t):
        sfxes = [t[i:] for i in range(len(t))]
        return [i[0] for i in sorted(enumerate(sfxes), key=lambda x:x[1])]

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
        first = {}
        offset = 0
        for c, count in sorted(ch_count.items()):
            first[c] = (offset, offset + count)
            offset += count
        return first

    def rank(self, c, k):
        return self.bwt[:k].count(c)

    def rank_lt(self, c):
        # TODO impl better way
        F = self.first_col(self.ch_count)
        if c in F:
            return F[c][0]
        else:
            return None

    def search(self, pat):
        assert self.bwt is not None
        assert self.ch_count is not None
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
