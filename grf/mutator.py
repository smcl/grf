from decision import (
    Classification,
    Decision,
    DecisionTreeGenerator
)
from .decisionvm import (
    PushConstant,
    PushAttribute,
    BinaryOperation,
    boolean_operators
)
import random

class Mutator(DecisionTreeGenerator):
    def __init__(self, env):
        self.env = env

    def mutate(self, decision):

        # for every 16 times we call this
        # - 10 should mutate once
        # - 5 should mutate twice
        # - 1 should mutate three times
        mutation_count = random.choice(
            [1] * 10
            + [2] * 5
            + [3] * 1
        )

        for n in range(mutation_count):
            mutation_function = random.choice([
                self.constant_scale,
                self.replace_op,
                self.swap_args,
                self.swap_true_false,
                self.replace_attribute,
                self.replace_classification,
                self.regenerate_true_node,
                self.regenerate_false_node
            ])

            mutation_function(decision)

    # find a PushConstant, change the value by some factor
    def constant_scale(self, decision):
        instr = self.get_instr(decision, PushConstant)

        if instr:
            available_scaling_factors = [ 0.01, 0.1, 1, 10 ]
            available_scaling_values = range(1,10)

            scale_factor = random.choice(available_scaling_factors)
            scale_value = random.choice(available_scaling_values)

            instr.constant *= scale_factor * scale_value

    # change the operator that this decision uses
    def replace_op(self, decision):
        instr = self.get_instr(decision, BinaryOperation)
        if instr:
            new_instr = random.choice(boolean_operators)
            instr.op = new_instr.op
            instr.name = new_instr.name

    # swap the true and false branches
    def swap_true_false(self, decision):
        if type(decision) is Decision:
            temp_node = decision.true_node
            decision.true_node = decision.false_node
            decision.false_node = temp_node

    # swap arg0 and arg1 around
    def swap_args(self, decision):
        if type(decision) is Decision:
            instrs = decision.instructions
            for i in range(len(instrs)):
                if ((instrs[i] is PushAttribute or instrs[i] is PushConstant) and
                    (instrs[i+1] is PushAttribute or instrs[i+1] is PushConstant)):
                    temp_instr = instrs[i]
                    instrs[i] = instrs[i+1]
                    instrs[i+1] = temp_instr

    def regenerate_true_node(self, decision):
        if type(decision) is Decision:
            decision.true_node = self.generate_node(decision.depth)
            self.populate_incomplete_node(decision)

    def regenerate_false_node(self, decision):
        if type(decision) is Decision:
            decision.false_node = self.generate_node(decision.depth)
            self.populate_incomplete_node(decision)

    # find a PushAttribute, and change the target attribute
    def replace_attribute(self, decision):
        instr = self.get_instr(decision, PushAttribute)
        if instr:
            instr.attribute = random.choice(self.env.attributes)


    # if decision is a classification, switch it up
    # otherwise NOP
    def replace_classification(self, decision):
        if type(decision) is Classification:
            decision.classification = random.choice(self.env.classifications)

    def get_instr(self, decision, this_type):
        instrs = [ i for i in decision.instructions if type(i) is this_type ]

        if instrs:
            return random.choice(instrs)
        return None
