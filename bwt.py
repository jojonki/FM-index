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
        # print('bwt', bwt)
        # print('original index', org_idx)

    def decode(self):
        assert self.bwt is not None
        assert self.text is not None
        assert self.org_idx is not None

        L = len(self.text)
        d = sorted(self.bwt)
        for _ in range(L - 1):
            for i in range(L):
                d[i] = self.bwt[i] + d[i]
            d = sorted(d)
        return d[self.org_idx]
