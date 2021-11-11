# The annotation.py contains code for generating the
# annotations.
import random


def get_conj(start=False):
    # get conjunction in natural language
    if start:
        return "At first, "
    return random.choice(['Then, ', 'Next, ', 'Afterwards, ', 'After that', 'Moving on, ', 'Subsequently, '])


def parse_plan(query_plan, start=False):
    """ Parse json format of query plan """
    selector = ParserSelector()
    try:
        parser = getattr(selector, query_plan["Node Type"].replace(" ", "_"))
    except:
        parser = selector.unrecognize
    parsed:str = initplan(query_plan, start)
    parsed += parser(query_plan, start)
    return parsed


def unrecognize(query_plan, start=False):
    # parser for unrecognized nodes
    parsed = get_conj(start)
    parsed += "do " + query_plan["Node Type"] + "."
    if "Plans" in query_plan:
        for child in query_plan["Plans"]:
            parsed += " " + parse_plan(child)
    return parsed

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
def sequential_scan(query_plan, start=False):
    sen = get_conj(start)
    sen += 'a sequential scan is performed on the relation '
    if "Relation Name" in query_plan:
        sen += '`{}`'.format(query_plan['Relation Name'])
    if 'Alias' in query_plan:
        sen += ' with alias `{}`'.format(query_plan['Alias'])
    sen += '.'
    if 'Filter' in query_plan:
        sen += ' Then it is filtered with the condition {}.'.format(query_plan['Filter'].replace('::text', ''))
    return sen


def subquery_scan(query_plan, start=False):
    sen = ""
    if 'Plans' in query_plan:
        # Parse each child node first
        for child in query_plan['Plans']:
            sen += parse_plan(child, start) + " "
            if start:
                start = False
    # After finishing all children, go back to the original node.
    sen += get_conj(start)
    sen += 'Subquery Scan is performed by output the results of the previous operations'
    sen += '(the purpose of Subquery scan is mainly for internal logging).'
    return sen


def cte_scan(query_plan, start=False):
    sen = get_conj(start)
    # Parse the values scan
    if query_plan["Node Type"] == "CTE Scan":
        sen += 'it does a CTE scan through the in-memory table '
        sen += '`{}`'.format(query_plan['CTE Name'])
        if "Index Cond" in query_plan:
            sen += " with condition(s) `{}`".format(query_plan["Index Cond"].replace('::text', ''))
        sen += "."
        if "Filter" in query_plan:
            sen += ' Then it is filtered with the condition {}.'.format(query_plan['Filter'].replace('::text', ''))
    return sen


def function_scan(query_plan, start=False):
    sen = get_conj(start)
    sen += "it runs the function " + query_plan["Function Name"]
    sen += " and returns the recordset as if they were rows read from a table."
    return sen


def index_scan(query_plan, start=False):
    sen = get_conj(start)
    # Parse the index scan or index only scan
    sen += "it does an index scan by using an index table "+ query_plan["Index Name"]
    if "Index Cond" in query_plan:
        sen += " with condition(s) `{}`".format(query_plan["Index Cond"].replace('::text', ''))

    if query_plan["Node Type"] == "Index Scan":
        sen += ". Next, it revisits the table `{}` and fetches rows that match index.".format(query_plan["Relation Name"])
    elif query_plan["Node Type"] == "Index Only Scan":
        sen += ". It then returns the matches found in index table scan."

    if "Filter" in query_plan:
        sen += ' Then it is filtered with the condition {}.'.format(query_plan['Filter'].replace('::text', ''))
    return sen


def values_scan(query_plan, start=False):
    sen = get_conj(start)
    sen += "it simply scan through the given values of the query."
    return sen


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


class ParserSelector:
    """ ParserSelectorClass """

    def __init__(self):
        """ Init Class """
        self.unrecognize = unrecognize

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


#
def initplan(query_plan, start=False):
    """ Check for InitPlan """
    sen = ""

    if "Parent Relationship" in query_plan:
        if query_plan["Parent Relationship"] == "InitPlan":
            sen = get_conj(start)
            sen += "the " + query_plan["Node Type"]
            sen += " node with its subsequent child node is executed first"
            sen += " for the result is only calculated once and may be needed subsequently."
            sen += "The plan is as follows:"
    return sen


def annotate(query_plan, start=False):
    parsed = ""
    selector = ParserSelector()
    try:
        parser = getattr(selector, query_plan["Node Type"].replace(" ", "_"))
    except:
        parser = selector.unrecognize
    parsed = initplan(query_plan, start)
    parsed += parser(query_plan, start)
    return parsed


