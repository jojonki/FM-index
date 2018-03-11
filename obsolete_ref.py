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
