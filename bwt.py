class BWT1:
    # ref: https://ja.wikipedia.org/wiki/%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF%E3%82%BD%E3%83%BC%E3%83%88
    def __init__(self, text=None):
        if text:
            self.text = text
            self.encode(text)

    def encode(self, text):
        assert self.text is not None
        circ_mat = []
        text_len = len(text)
        for i in range(text_len):
            circ_mat.append(text[text_len-i:] + text[:text_len-i])

        sorted_idx = sorted(range(text_len), key=lambda k: circ_mat[k])
        self.bwt = [circ_mat[idx][-1] for idx in sorted_idx]
        self.org_idx = sorted_idx.index(0)
        self.sort_index_map = sorted(range(text_len), key=lambda k: self.bwt[k])

    def _fixed_sort(self, d):
        '''
        Effective sort by using that sort mapping is always same in BWT
        '''
        assert self.sort_index_map is not None
        return [d[index] for index in self.sort_index_map]

    def decode(self):
        assert self.bwt is not None
        assert self.text is not None
        assert self.org_idx is not None

        text_len = len(self.text)
        d = self._fixed_sort(self.bwt)
        for _ in range(text_len - 1):
            for i in range(text_len):
                d[i] = self.bwt[i] + d[i]
            d = self._fixed_sort(d)
        return d[self.org_idx]


class BWT2:
    # ref: http://d.hatena.ne.jp/naoya/20081016/1224173077
    def __init__(self, text=None):
        self.marker = '$'
        if text:
            self.text = text + self.marker
            self.encode(self.text)

    def encode(self, text):
        assert self.text is not None
        if text[-1] != self.marker:
            text += self.marker
            self.text = text

        circ_mat = []
        text_len = len(text)
        for i in range(text_len):
            circ_mat.append(text[text_len-i:] + text[:text_len-i])

        sorted_idx = sorted(range(text_len), key=lambda k: circ_mat[k])
        self.bwt = [circ_mat[idx][-1] for idx in sorted_idx]
        # print(self.bwt)

    def decode(self):
        assert self.bwt is not None
        assert self.text is not None

        L = self.bwt
        mem = {}
        for i, c in enumerate(L):
            if c not in mem:
                mem[c] = 1
            else:
                mem[c] += 1
            L[i] += str(mem[c])

        F = sorted(L)
        idx = L.index(self.marker + '1')
        ret_text = ''
        for _ in range(len(self.text)):
            ret_text += F[idx][0]
            idx = L.index(F[idx])
        return ret_text


class BWT3:
    # ref https://www.cs.jhu.edu/~langmea/resources/lecture_notes/bwt_and_fm_index.pdf
    def __init__(self):
        self.marker = '$'

    def encode(self, text):
        # self.encode(self.text)
        sa = self.suffix_array(text)
        print('sa', sa)
        self.bwt = self.bwt_via_sa(text, sa)
        return self.bwt
        
    def decode(self, bwt):
        ranks, tots = self.rank_bwt(bwt)
        print('ranks', ranks)
        print('tots', tots)
        first = self.firstCol(tots)
        print('first', first)
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
        tots = {}
        ranks = []
        for c in bw:
            if c not in tots:
                tots[c] = 0
            ranks.append(tots[c])
            tots[c] += 1
        return ranks, tots

    def firstCol(self, tots):
        first = {}
        totc = 0
        for c, count in sorted(tots.items()):
            first[c] = (totc, totc + count)
            totc += count
        return first
