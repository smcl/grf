import decisionvm
import random

class ClassifiedObject(object):
    def __init__(self):
        pass

def get_attributes(o):
    base = ClassifiedObject()
    return list(set(dir(o)) - set(dir(base)))

#---------------------------------------
class Decision(object):
    def __init__(self, instructions, depth):
        self.instructions = instructions
        self.true_node = None
        self.false_node = None
        self.depth = depth

    def Classify(self, obj):
        stack = []
        for ins in self.instructions:
            ins.Execute(obj, stack)
        result = stack.pop()
        if result:
            return self.true_node.Classify(obj)
        return self.false_node.Classify(obj)

class Classification(object):
    def __init__(self, classification, depth):
        self.classification = classification
        self.depth = depth

    def Classify(self, obj):
        return self.classification

#---------------------------------------
class DecisionTreeGenerator(object):
    def __init__(self, data, const_attribute_prob=0.75):
        self.data = data
        self.classifications = list(set([d[1] for d in data]))
        self.attributes = get_attributes(d[0])
        self.const_attribute_prob = const_attribute_prob
        all_values = []
        for d in data:
            for a in self.attributes:
                all_values.append(d[0].__getattribute__(a))
        self.all_values = all_values

    def generate(self):
        root = self.generate_node(0)
        node = self.get_incomplete_node(root)
        while node:
            depth = node.depth + 1
            node.true_node = self.generate_node(depth)
            node.false_node = self.generate_node(depth)
            node = self.get_incomplete_node(root)
        return root

    def get_incomplete_node(self, node):
        if type(node) is Classification:
            return None

        if not node.true_node and not node.false_node:
            return node

        incomplete_in_true_branch = self.get_incomplete_node(node.true_node)
        if incomplete_in_true_branch:
            return incomplete_in_true_branch

        incomplete_in_false_branch = self.get_incomplete_node(node.false_node)
        if incomplete_in_false_branch:
            return incomplete_in_false_branch

        return None

    def decision_probability_at_depth(self, depth):
        return (2 ** (1 - depth)) / 2.0

    def generate_node(self, depth):
        if random.random() < self.decision_probability_at_depth(depth):
            return self.generate_decision(depth)
        return self.generate_classification(depth)

    def generate_classification(self, depth):
        return Classification(random.choice(self.classifications), depth)

    def generate_decision(self, depth):
        op = random.choice(decisionvm.boolean_operators)
        arg0 = decisionvm.PushAttribute(random.choice(self.attributes))
        if random.random() > self.const_attribute_prob:
            arg1 = decisionvm.PushAttribute(random.choice(self.attributes))
        else:
            arg1 = decisionvm.PushConstant(random.choice(self.all_values))
        return Decision([ arg0, arg1, op ], depth)
