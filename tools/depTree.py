class Tree(object):
    def __init__(self, name, *children):
        self.name = name
        self.children = children

    def __str__(self):
        return '\n'.join(self.tree_lines())

    def tree_lines(self):
        yield self.name
        last = self.children[-1] if self.children else None
        for child in self.children:
            prefix = '`-' if child is last else '+-'
            for line in child.tree_lines():
                yield prefix + line
            prefix = '  ' if child is last else '| '


tree = Tree('Change',
    Tree('External',
        Tree('External A'),Tree('External B'),Tree('External C',Tree('Sub Ext C'))),
    Tree('Internal',
        Tree('Internal A'),Tree('Internal B',Tree('Sub Int B')),Tree('Internal C'))
    )   

print(tree) 