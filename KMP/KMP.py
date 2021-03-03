class kmp():
    def KmpSearch(self, text, pattern):
        n = len(text)
        m = len(pattern)
        prefix = self.KmpPrefix(pattern)
        i = 0
        j = 0
        while i < n and j < m:
            if j == -1 or text[i] == pattern[j]:
                #若j == -1 则pattern[0] != text[i]，则i和j的指针分别加1
                #若text[i] == pattern[j]，则当前比对元素匹配，i和j递增
                i += 1
                j += 1
            else:
                #若j ！= -1且pattern[0] != text[i]，则j指向它的前缀函数(prefix)值。
                j = prefix[j]
        if j == m:
            return i-j
        else:
            return -1


    def KmpPrefix(self, pattern):
        m = len(pattern)
        prefix = [0]*m
        prefix[0] = -1
        k = -1
        j = 0
        while j < m-1:
            if k == -1 or pattern[k] == pattern[j]:
                k += 1
                j += 1
                prefix[j] = k
            else:
                k = prefix[k]
        return prefix

if __name__ == "__main__":
    s = kmp()
    print(s.KmpSearch("BBC ABCDAB ABCDABCDABDE", "ABCDABD"))
