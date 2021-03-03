import math

class IntervalRBNode:
    def __init__(self, inter, color='R'):
        self.color = color
        self.right = None
        self.left = None
        self.parent = None
        self.max = inter.high
        self.inter = inter

    def printNode(self):
        print("Interval = [%s, %s]" % (self.inter.low, self.inter.high))
        print("color = ", self.color)
        print("right = ", self.right)
        print("left = ", self.left)
        print("parent = ", self.parent)
        print("Max = ", self.max)

class Inter:
    def __init__(self, low, high):
        self.low = low
        self.high = high

class IntervalRBTree:
    def __init__(self):
        self.nil = IntervalRBNode(Inter(-float('inf'), -float('inf')), color = 'B')
        self.root = self.nil

    def preorderTreeWalk(self, node):
        if node != self.nil:
            print(node.inter.low, node.inter.high, node.color, node.max)
            self.preorderTreeWalk(node.left)
            self.preorderTreeWalk(node.right)

    def inorderTreeWalk(self, node):
        if node != self.nil:
            self.inorderTreeWalk(node.left)
            print(node.inter.low, node.inter.high, node.color, node.max)
            self.inorderTreeWalk(node.right)

    def postorderTreeWalk(self, node):
        if node != self.nil:
            self.postorderTreeWalk(node.left)
            self.postorderTreeWalk(node.right)
            print(node.inter.low, node.inter.high, node.color, node.max)

    def TREEMinimum(self, z):
        while z.left != self.nil:
            z = z.left
        return z

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if y.parent.inter.low == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        y.max = x.max
        x.max = max(x.left.max, x.right.max, x.inter.high)

    def rightRotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y

        x.parent = y.parent
        if x.parent.inter.low == None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x
        x.max = y.max
        y.max = max(y.left.max, y.right.max, y.inter.high)

    def RBInsert(self, inter):
        # 找到插入的位置，与BST插入相同
        z = IntervalRBNode(inter)
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            y.max=max(y.max, inter.high)
            if z.inter.low < x.inter.low:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.inter.low < y.inter.low:
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
        yOriginalColor = z.color
        if z.left == self.nil:
            x = z.right
            self.RBTransplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.RBTransplant(z, z.left)
        else:
            y = self.TREEMinimum(z.right)
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
        y.max = max(y.max, y.left.max, y.right.max)
        temp = y
        while temp != self.root:
            temp.parent.max = max(temp.parent.max, temp.parent.left.max, temp.parent.right.max)
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

    def intervalSearch(self, i):
        x = self.root
        while x != self.nil and (i.high < x.inter.low or x.inter.high < i.low):
            if x.left != self.nil and x.left.max >= i.low:
                x = x.left
            else:
                x = x.right
        return x

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
                print("[", end = '')
                print('{:2}'.format(r.inter.low), end=', ')
                print('{:2}'.format(r.inter.high), end='')
                print("]", end = '')
                print(',', end='')
                print(r.color, end='')
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

if __name__ == "__main__":
    number_list = (8, 9, 25, 30, 5, 8, 15, 23, 17, 19, 26, 26, 0, 3, 6, 10, 19, 20)
    rbt = IntervalRBTree()
    for i in range(0, len(number_list), 2):
        inter=Inter(number_list[i], number_list[i+1])
        rbt.RBInsert(inter)

    rbt.printTree(5, 5)
    rbt.preorderTreeWalk(rbt.root)
    delnode = rbt.intervalSearch(Inter(8, 10))
    delnode.printNode()
    rbt.RBDelete(delnode)
    print("删除值区间[%s, %s]的结点后的红黑树:" % (delnode.inter.low, delnode.inter.high))
    rbt.preorderTreeWalk(rbt.root)
    print("中序遍历:")
    rbt.inorderTreeWalk(rbt.root)
    print("后序遍历:")
    rbt.postorderTreeWalk(rbt.root)