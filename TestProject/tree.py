class Tree:

    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add_child(self, value):
        self.children.append(Tree(value))

    def __getitem__(self, val) -> 'Tree':
        for c in self.children:
            if c.value == val:
                return c
            if val in c:
                return c[val]
        raise KeyError

    def __delitem__(self, key):
        for i in range(len(self.children)):
            if self.children[i] == key:
                del self.children[i]
                return
        return

    def __contains__(self, item):
        if self.value == item:
            return True
        for c in self.children:
            if item in c:
                return True
        return False

    def format(self):
        out = ['└─> ' + str(self.value)]
        if len(self.children) > 0:
            cs = self.children
            for c in cs:
                out += ['\t' + x for x in c.format()]
        return out

    def __str__(self) -> str:
        return '\n'.join(self.format())


t = Tree('EE301')
t.add_child('EE201')
t.add_child('EE202')
t['EE201'].add_child('EE101')
t['EE201'].add_child('EE102')
t['EE202'].add_child('EE103')

[t[x].add_child('Higher Maths') for x in ['EE101', 'EE102', 'EE103']]
[t[x].add_child('Higher Physics') for x in ['EE101', 'EE102', 'EE103']]
[t[x].add_child('Higher Computing') for x in ['EE103']]

print(t)