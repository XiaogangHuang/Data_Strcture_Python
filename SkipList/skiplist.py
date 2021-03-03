import random
MAXLevel = 20

class Node:
    def __init__(self, level, key):
        self.key = key
        self.forward = [None] * level

    def printNode(self):
        print(self.key)
        for i in self.forward:
            print(i.key)

class Skiplist:
    def __init__(self):
        self.level = 0
        self.header = Node(MAXLevel, None)
        self.size = 0

    def search(self, key):
        i = self.level - 1
        q = self.header
        while i >= 0:
            while q.forward[i] and q.forward[i].key <= key:
                if q.forward[i].key == key:
                    return q.forward[i]
                q = q.forward[i]
            i -= 1
        return self.header

    def insert(self, key):
        update = [None] * MAXLevel
        i = self.size - 1
        q = None
        while i >= 0:
            q = self.header
            while q.forward[i] and q.forward[i].key <key:
                q = q.forward[i]
            update[i] = q
            i -= 1

        if q and q.key == key:
            return False

        k = random.randint(1, self.level + 1)

        if k > self.level:
            i =self.level
            update[i] = self.header
            self.level += 1
            k = self.level

        q = Node(k, key)
        i = 0
        while i < k:
            q.forward[i] = update[i].forward[i]
            update[i].forward[i] = q
            i += 1

        self.size += 1

        return True

    def delete(self, key):
        update = [None] * MAXLevel
        i =self.level - 1
        q = None
        while i >= 0:
            q = self.header
            while q.forward[i] and q.forward[i].key < key:
                q =q.forward[i]
            update[i] = q
            i -= 1

        if q and q.key == key:
            i = 0
            while i < self.level:
                if update[i].forward[i] == q:
                    update[i].forward[i] = q.forward[i]
                i += 1
            del q
            i = self.level - 1
            while i >= 0:
                if self.header.forward[i] is None:
                    self.level -= 1
                i -= 1
            self.size -= 1

            return True
        else:
            return False


if __name__ == "__main__":
    number_list = [1, 2, 3, 4, 5, 6, 7]
    sl = Skiplist()
    for i in number_list:
        sl.insert(i)

    sl.search(3).printNode()
