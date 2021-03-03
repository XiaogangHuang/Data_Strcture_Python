import math

class OsRBNode:
    def __init__(self, val, color='R'):
        self.val = val
        self.color = color
        self.right = None
        self.left = None
        self.parent = None
        self.size = 0

    def printNode(self):
        print("key = ", self.val)
        print("color = ", self.color)
        print("right = ", self.right)
        print("left = ", self.left)
        print("parent = ", self.parent)
        print("size = ", self.size)


class OsRBTree:
    def __init__(self):
        self.nil = OsRBNode(None, color='B')
        self.root = self.nil

    def preorderTreeWalk(self, node):
        if node != self.nil:
            print(node.val, node.color, node.size)
            self.preorderTreeWalk(node.left)
            self.preorderTreeWalk(node.right)

    def inorderTreeWalk(self, node):
        if node != self.nil:
            self.inorderTreeWalk(node.left)
            print(node.val, node.color, node.size)
            self.inorderTreeWalk(node.right)

    def postorderTreeWalk(self, node):
        if node != self.nil:
            self.postorderTreeWalk(node.left)
            self.postorderTreeWalk(node.right)
            print(node.val, node.color, node.size)

    def TREEMinimum(self, z):
        while z.left != self.nil:
            z = z.left
        return z

    def TREEMaximum(self, z):
        while z.right != self.nil:
            z = z.right
        return z

    def RBSearch(self, val):
        x = self.root
        while x != self.nil and val != x.val:
            if val < x.val:
                x = x.left
            else:
                x = x.right
        return x

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if y.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

    def rightRotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y

        x.parent = y.parent
        if x.parent == self.nil:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x
        x.size = y.size
        y.size = y.left.size + y.right.size + 1

    def RBInsert(self, val):
        # 找到插入的位置，与BST插入相同
        z = OsRBNode(val)
        z.size = 1
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            x.size = x.size + 1
            if z.val < x.val:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.val < y.val:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        # 解决冲突(违反红黑树的规则)
        self.RBInsertFixup(z)

    def RBInsertFixup(self, z):
        while z.parent != self.nil and z.parent.color == 'R':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y != self.nil and y.color == 'R':
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    y.color = 'B'
                    z = z.parent.parent
                elif z == z.parent.right:
                    z = z.parent
                    self.leftRotate(z)
                else:
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self.rightRotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y != self.nil and y.color == 'R':
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    y.color = 'B'
                    z = z.parent.parent
                elif z == z.parent.left:
                    z = z.parent
                    self.rightRotate(z)
                else:
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self.leftRotate(z.parent.parent)
        self.root.color = 'B'

    def RBTransplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def RBDelete(self, z):
        # y:换到z原来位置的结点
        # x:换到y原本位置的结点
        y = z
        temp = y
        yOriginalColor = z.color
        if z.left == self.nil:
            x = z.right
            self.RBTransplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.RBTransplant(z, z.left)
        else:
            y = self.TREEMinimum(z.right)
            temp = y.parent
            yOriginalColor = y.color
            x = y.right
            x.parent = y
            if y.parent != z:
                self.RBTransplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.RBTransplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        y.size = y.left.size + y.right.size + 1
        temp.size -= 1
        while temp.parent != self.nil:
            temp.parent.size -= 1
            temp = temp.parent
        if yOriginalColor == 'B':
            self.RBDeleteFixup(x)

    def RBDeleteFixup(self, x):
        while x != self.root and x.color == 'B':
            if x == x.parent.left:
                t = x.parent.right
                if t.color == 'R':
                    t.color = 'B'
                    x.parent.color = 'R'
                    self.leftRotate(x.parent)
                    t = x.parent.right
                if t.left.color == 'B' and t.right.color == 'B':
                    t.color = 'R'
                    x = x.parent
                elif t.right.color == 'B':
                    t.left.color = 'B'
                    t.color = 'R'
                    self.rightRotate(t)
                    t = x.parent.right
                else:
                    t.color = x.parent.color
                    x.parent.color = 'B'
                    t.right.color = 'B'
                    self.leftRotate(x.parent)
                    x = self.root
            else:
                t = x.parent.left
                if t.color == 'R':
                    t.color = 'B'
                    x.parent.color = 'R'
                    self.rightRotate(x.parent)
                    t = x.parent.left
                if t.right.color == 'B' and t.left.color == 'B':
                    t.color = 'R'
                    x = x.parent
                elif t.left.color == 'B':
                    t.right.color = 'B'
                    t.color = 'R'
                    self.leftRotate(t)
                    t = x.parent.left
                else:
                    t.color = x.parent.color
                    x.parent.color = 'B'
                    t.left.color = 'B'
                    self.rightRotate(x.parent)
                    x = self.root
        x.color = 'B'

    def Rank(self, x):
        r = x.left.size + 1
        y = x
        while y != self.root:
            if y == y.parent.right:
                r = r + y.parent.left.size + 1
            y = y.parent
        return r

    def treeHigh(self, node):
        if node == self.nil:
            return 0
        lthigh = self.treeHigh(node.left)
        rthigh = self.treeHigh(node.right)
        return max(lthigh, rthigh) + 1

    def printTree(self, space, printlen):
        # 用广度优先实现树的打印
        # printlen每个结点打印宽度
        if space < printlen:
            print("结点间最近距离大于结点字符长度")
            return 0
        treehigh = self.treeHigh(self.root)
        if self.root == self.nil:
            return 0
        q = []
        q.append(self.root)
        pos = []
        pos.append(((printlen + space) * 2 **
                   (treehigh - 2) + 1 + math.floor((space-printlen)/2)))
        level = 1
        while len(q) > 0:
            length = len(q)
            temp = 0
            for i in range(length):
                r = q.pop(0)
                p = pos.pop(0)
                print(" " * (p - temp), end='')
                print('{:2}'.format(r.val), end='')
                print(',', end='')
                print(r.color, end='')
                print(r.size, end = '')
                temp = p + 2
                if r.left != self.nil:
                    stemp = printlen * (treehigh - level - 1) + math.floor(space/2) * (2 ** (treehigh - level - 1))
                    q.append(r.left)
                    pos.append(p - stemp)
                if r.right != self.nil:
                    stemp = printlen * (treehigh - level) + math.floor(space/2) * (2 ** (treehigh - level - 1))
                    q.append(r.right)
                    pos.append(p + stemp)
            level += 1
            print('\n')

def Select(x, i):
    r = x.left.size + 1
    if i == r:
        return x
    elif i < r:
        return Select(x.left, i)
    else:
        return Select(x.right, i - r)

def josephus(n, m):
    number_list = list(range(1, n + 1))
    rbt = OsRBTree()
    for i in number_list:
        rbt.RBInsert(i)

    josephuspermutation = []
    j = m
    p = n
    for i in range(n):
        node = Select(rbt.root, j)
        josephuspermutation.append(node.val)
        rbt.RBDelete(node)
        p = p - 1
        if i < n - 1:
            j = (j + m - 1) % p
            if j == 0:
                j = p
    return josephuspermutation

if __name__ == "__main__":
    print(josephus(100, 5))