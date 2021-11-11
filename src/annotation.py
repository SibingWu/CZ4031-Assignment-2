# The annotation.py contains code for generating the
# annotations.
import random


def get_conj(start=False):
    # get conjunction in natural language
    if start:
        return "At first, "
    return random.choice(['Then, ', 'Next, ', 'Afterwards, ', 'After that', 'Moving on, ', 'Subsequently, '])


"""
Query plan
@:param Node Type
@:Parallel Aware
@:Async Capable
@:Relation Name
@:Alias
@:Filter
@:Startup Cost
@:Total Cost
@:Plan Rows
@:Plan Width
"""


################################### SCAN ####################################
def sequential_scan(query_plan):
    sen = get_conj()
    sen += 'a sequential scan is performed on the relation '
    if "Relation Name" in query_plan:
        sen += '`{}`'.format(query_plan['Relation Name'])
    if 'Alias' in query_plan:
        sen += ' with alias `{}`'.format(query_plan['Alias'])
    sen += '.'
    if 'Filter' in query_plan:
        sen += ' And it is filtered with the condition {}.'.format(query_plan['Filter'].replace('::text', ''))
    return sen


def subquery_scan(query_plan):
    pass


def cte_scan(query_plan):
    pass


def function_scan(query_plan):
    pass


def index_scan(query_plan):
    pass


def values_scan(query_plan):
    pass


################################### JOIN ####################################
def hash_join(query_plan):
    pass


def merge_join(query_plan):
    pass


################################### OTHER? ####################################
def aggregate(query_plan):
    pass


def append(query_plan):
    pass


def groupby(query_plan):
    pass


def hash(query_plan):
    pass


def limit(query_plan):
    pass


def materialize(query_plan):
    pass


def nested_loop(query_plan):
    pass


def setop(query_plan):
    pass


def sort(query_plan):
    pass


def unique(query_plan):
    pass


def unrecognize(query_plan):
    # generic parser
    pass


class ParserSelector:
    """ ParserSelectorClass """

    def __init__(self):
        """ Init Class """
        self.unrecognize = unrecognize()

        self.hash_join = hash_join
        self.Sort = sort
        self.Aggregate = aggregate
        self.Seq_Scan = sequential_scan
        self.Hash = hash
        self.Merge_Join = merge_join
        self.Limit = limit
        self.Unique = unique
        self.Function_Scan = function_scan
        self.Index_Scan = index_scan
        self.Index_Only_Scan = index_scan
        self.Values_Scan = values_scan
        self.Nested_Loop = nested_loop
        self.CTE_Scan = cte_scan
        self.Append = append
        self.Materialize = materialize
        self.Subquery_Scan = subquery_scan
        self.SetOp = setop
        self.Group = groupby


# COPIED!! NEED REPHRASE!!
def initplan(plan, start=False):
    """ Check for InitPlan """
    result = ""

    if "Parent Relationship" in plan:
        if plan["Parent Relationship"] == "InitPlan":
            result = get_conj(start)
            result += "the " + plan["Node Type"]
            result += " node and its subsequent child node is executed first"
            result += " since the result from this node needs to be calculated first"
            result += " and it is only calculated once for the whole query. "
            result += "The plan is as follows:"

    return result


def annotate(query_plan, start=False):
    selector = ParserSelector()
    try:
        parser = getattr(selector, query_plan["Node Type"].replace(" ", "_"))
    except:
        parser = selector.generic_parser
    parsed_plan = initplan(query_plan, start)
    parsed_plan += parser(query_plan, start)
    return parsed_plan


