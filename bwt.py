class BWT:
    def __init__(self, text=None):
        if text:
            self.text = text
            self.encode(text)

    def encode(self, text):
        assert self.text is not None
        circ_mat = []
        L = len(text)
        for i in range(L):
            circ_mat.append(text[L-i:] + text[:L-i])

        sorted_idx = sorted(range(L), key=lambda k: circ_mat[k])
        self.bwt = [circ_mat[idx][-1] for idx in sorted_idx]
        self.org_idx = sorted_idx.index(0)

        # print('circulant_mat', circ_mat)
        # print('sorted circulant_mat', sorted(circ_mat))
        # print('sorted_idx', sorted_idx)
        # print('bwt', self.bwt)
        self.sort_index_map = sorted(range(L), key=lambda k: self.bwt[k])
        # print('original index', org_idx)

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

        L = len(self.text)
        d = self._fixed_sort(self.bwt)
        for _ in range(L - 1):
            for i in range(L):
                d[i] = self.bwt[i] + d[i]
            d = self._fixed_sort(d)
        return d[self.org_idx]
