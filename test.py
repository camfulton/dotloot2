from collections import namedtuple


Block = namedtuple(
    'Block', ['lines', 'show', 'nosound', 'comment', 'category', 'lookup']
)

Line = namedtuple(
    'Line', ['parameter', 'value', 'category_name', 'block_name']
)

line = Line(1, 1, 1, 1)
block = Block([line], 1, 1, 1, 1, 1)

print(line)

for line in block.lines:
    line.parameter = 2
    line.value = 2
    line.category_name = 2
    line.block_name = 2

print(block)