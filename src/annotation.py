# The annotation.py contains code for generating the
# annotations.
import random


def get_conj(start=False):
    # get conjunction in natural language
    if start:
        return "At first, "
    return random.choice([' Then, ', ' Next, ', ' Afterwards, ', ' After that, ', ' Moving on, ', ' Subsequently, '])


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


################################### SCAN ####################################
def sequential_scan(query_plan, start=False):
    sen = get_conj(start)
    sen += 'a sequential scan is performed on the relation '
    if "Relation Name" in query_plan:
        sen += '`{}`'.format(query_plan['Relation Name'])
    if 'Alias' in query_plan:
        if query_plan['Relation Name'] != query_plan['Alias']:
            sen += ' with alias `{}`'.format(query_plan['Alias'])
    sen += '.'
    if 'Filter' in query_plan:
        sen += ' And it is filtered with the condition {}.'.format(query_plan['Filter'].replace('::text', '').replace('::integer[]', ''))
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
            sen += ' And it is filtered with the condition {}.'.format(query_plan['Filter'].replace('::text', '').replace('::integer[]', ''))
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
        sen += ' And it is filtered with the condition {}.'.format(query_plan['Filter'].replace('::text', '').replace('::integer[]', ''))
    return sen


def values_scan(query_plan, start=False):
    sen = get_conj(start)
    sen += "it simply scan through the given values of the query."
    return sen


################################### JOIN ####################################
def hash_join(query_plan, start=False):
    sen = ''

    sen += annotate(query_plan['Plans'][1], start) + ' '
    sen += annotate(query_plan['Plans'][0]) + ' '

    sen += 'The above result are joined by Hash {} Join'.format(query_plan['Join Type'])
    if 'Hash Cond' in query_plan:
        sen += ' with hash condition {}.'.format(query_plan['Hash Cond'].replace('::text', ''))
    else:
        sen += '.'

    return sen


def merge_join(query_plan, start=False):
    sen = ''

    if 'Plans' in query_plan:
        for obj in query_plan['Plans']:
            sen += annotate(obj, start) + ' '
            if start:
                start = False

    sen += get_conj(start)
    sen += 'The above result are joined by Merge Join'

    if 'Merge Cond' in query_plan:
        sen += ' with merge condition {}'.format(query_plan['Merge Cond'].replace('::text', ''))

    if 'Join Type' == 'Semi':
        sen += ' but the result from the left table is returned.'
    else:
        sen += '.'

    return sen


################################### OTHER ####################################
def aggregate(query_plan, start=False):
    sen = ''

    if query_plan['Strategy'] == 'Sorted':
        sen += annotate(query_plan['Plans'][0], start)
        sen += " {}".format(get_conj())

        if 'Group Key' in query_plan:
            sen += ' it is grouped by '
            for key in query_plan['Group Key']:
                sen += key.replace('::text', '') + ', '
            sen = sen[:-2]
        if 'Filter' in query_plan:
            sen += ' with condition {}'.format(query_plan['Filter'].replace('::text', ''))
        sen += '.'
        return sen

    if query_plan['Strategy'] == 'Hashed':
        sen += get_conj()

        if len(query_plan['Group Key']) == 1:
            sen += 'rows are hashed on key {}, '.format(query_plan['Group Key'][0].replace('::text', ''))
        else:
            sen += 'rows are hashed on keys '
            for key in query_plan['Group Key']:
                sen += key.replace('::text', '') + ', '
        sen += 'result is produced afterwards.'

        return annotate(query_plan['Plans'][0], start) + ' ' + sen

    if query_plan['Strategy'] == 'Plain':
        sen += '{} {} then the result is aggregated.'.format(annotate(query_plan['Plans'][0], start), get_conj())
        return sen


def append(query_plan, start=False):
    sen = ''

    if 'Plans' in query_plan:
        for obj in query_plan['Plans']:
            child = annotate(obj, start)
            if start:
                start = False
            sen += child + ' '

    if query_plan['Node Type'] == 'Append':
        sen += get_conj(start)
        sen += 'results are appended together.'

    return sen


def groupby(query_plan, start=False):
    sen = ''

    sen += annotate(query_plan['Plans'][0], start)
    sen += ' {}'.format(get_conj())

    if len(query_plan['Group Key']) == 1:
        sen += 'the grouped key for the query is '
        sen += query_plan['Group Keys'][0].replace('::text', '') + '.'
    else:
        sen += 'the grouped keys for the keys are '
        for key in query_plan['Group Key'][:-1]:
            sen += key.replace('::text', '') + ', '
        sen += query_plan['Group Key'][-1].replace('::text', '') + '.'

    return sen


def hash(query_plan, start=False):
    sen = ''
    print(query_plan)

    if 'Plans' in query_plan:
        sen += annotate(query_plan['Plans'][0], start)
        sen += ' A memory hash occurs.'
    else:
        sen += get_conj(start)
        sen += ' a memory hash occurs.'
    return sen


def limit(query_plan, start=False):
    sen = ''

    sen += annotate(query_plan['Plans'][0], start)
    sen += 'The result is limited with {} entries.'.format(query_plan['Plan Rows'])

    return sen


def materialize(query_plan, start=False):
    sen = ''

    if 'Plans' in query_plan:
        for obj in query_plan['Plans']:
            child = annotate(obj, start)
            if start:
                start = False
            sen += child + ' '

    if query_plan['Node Type'] == 'Materialize':
        sen += get_conj(start)
        sen += 'the results are materialized in memory'

    return sen


def nested_loop(query_plan, start=False):
    sen = ''

    sen += annotate(query_plan['Plans'][0], start)
    sen += annotate(query_plan['Plans'][1])

    return sen


def setop(query_plan, start=False):
    sen = ''

    sen += annotate(query_plan['Plans'][0], start)
    sen += ' {}'.format(get_conj())
    sen += 'it discovers the '
    cmd = str(query_plan['Command'])
    if 'Except' in cmd:
        sen += 'differences '
    else:
        sen += 'similarities '
    sen += 'between the scanned tables using {} operation.'.format(query_plan['Node Type'])

    return sen


def sort(query_plan, start=False):
    sen = ''

    if 'Plans' in query_plan:
        for obj in query_plan['Plans']:
            child = annotate(obj, start)
            if start:
                start = False
            sen += child + ' '

    # ASC / DESC
    if query_plan['Node Type'] == 'Sort':
        sen += '{}the result is sorted using '.format(get_conj())
        if 'DESC' in query_plan['Sort Key']:
            sen += str(query_plan['Sort Key'].replace('DESC', '')) + 'in descending order.'
        elif 'INC' in query_plan['Sort Key']:
            sen += str(query_plan['Sort Key'].replace('INC', '')) + ' in ascending order.'
        else:
            sen += str(query_plan['Sort Key']) + '.'

    return sen


def unique(query_plan, start=False):
    sen = ''

    sen += annotate(query_plan['Plans'][0], start) + ' ' + get_conj()
    sen += 'it keeps the unique value on the data.'

    return sen


def unrecognize(query_plan, start=False):
    # parser for unrecognized nodes
    sen = ''
    print(query_plan['Node Type'])
    sen += '{}execute {}.'.format(get_conj(start), query_plan['Node Type'])
    if 'Plans' in query_plan:
        for obj in query_plan['Plans']:
            sen += ' ' + annotate(obj)

    return sen

  
class ParserSelector:
    """ ParserSelectorClass """

    def __init__(self):
        """ Init Class """
        self.generic_parser = unrecognize

        self.Hash_Join = hash_join
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
    selector = ParserSelector()
    try:
        annotator = getattr(selector, query_plan["Node Type"].replace(" ", "_"))
    except:
        annotator = selector.unrecognize
    parsed_plan = initplan(query_plan, start)
    parsed_plan += annotator(query_plan, start)
    return parsed_plan


