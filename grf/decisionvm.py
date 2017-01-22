#!/usr/bin/python

class Instruction(object):
    def Execute(self, obj, stack):
        raise Exception("Execute(obj, stack) not implemented")

    def ToString(self):
        raise Exception("ToString() not implemented on this instruction")


class PushConstant(Instruction):
    def __init__(self, constant):
        self.constant = constant

    def Execute(self, obj, stack):
        stack.append(self.constant)

    def ToString(self):
        return "PushConstant(%s)" % (str(self.constant))

class PushAttribute(Instruction):
    def __init__(self, attribute):
        self.attribute = attribute

    def Execute(self, obj, stack):
        stack.append(obj.__getattribute__(self.attribute))

    def ToString(self):
        return "PushAttribute(%s)" % (str(self.attribute))

class BinaryOperation(Instruction):
    def __init__(self, name, op):
        self.name = name
        self.op = op

    def Execute(self, obj, stack):
        y = stack.pop()
        x = stack.pop()
        stack.append(self.op(x, y))

    def ToString(self):
        return "BinaryOperation(%s)" % (self.name)


boolean_operators = [
    BinaryOperation("greater_than", lambda x, y: x > y),
    BinaryOperation("greater_than_equal", lambda x, y: x >= y),
    BinaryOperation("less_than", lambda x, y: x < y),
    BinaryOperation("less_than_equal", lambda x, y: x <= y),
    BinaryOperation("equal", lambda x, y: x == y),
    BinaryOperation("not_equal", lambda x, y: x != y)
]
