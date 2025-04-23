from newick import Node

__all__ = ['get_tree']


def get_tree(gc2lid, lgs):
    assert all(lgs[gc].lineage for gc in gc2lid), (
        'Unexpected isolates {}'.format([gc for gc in gc2lid if not lgs[gc].lineage]))
    family_gcs = [lgs[gc].lineage[0][1] for gc in gc2lid]
    assert len(set(family_gcs)) == 1, 'Languoids from multiple families in wordlist'

    tree = lgs[family_gcs[0]].newick_node(template='{l.id}')
    tree.prune_by_names(list(gc2lid), inverse=True)

    # Sometimes lingpy_wordlists contain data on languoids which are classified in Glottolog in the
    # same lineage, i.e. one is considered a dialect of the other. We resolve these cases by making
    # direct descendants siblings.
    lineages = {gc: {lgc for _, lgc, _ in lgs[gc].lineage} for gc in gc2lid}
    direct_descendants = {}
    for gc in gc2lid:
        for other, lineage in lineages.items():
            if gc in lineage:
                direct_descendants[gc] = other

    nodes = list(tree.walk())
    for n in nodes:
        if n.name in direct_descendants:
            n.add_descendant(Node(n.name))
            n.name = ''

    # Rename nodes from Glottocodes to dataset-specific language IDs.
    rename = {n.name: '' for n in tree.walk() if not n.is_leaf}
    multi = {}
    for gc, lids in gc2lid.items():
        lids = sorted(lids)
        rename[gc] = lids[0]
        # Keep track of cases where multiple IDs are mapped to the same Glottocode:
        if len(lids) > 1:
            multi[rename[gc]] = lids
    tree.rename(**rename)
    tree.remove_redundant_nodes(keep_leaf_name=True)

    # Some lingpy_wordlists contain data on varieties which are mapped to the same Glottolog
    # languoid. In order to maximize the overlapo between tree nodes and varieties in the wordlist,
    # we replace the one node for the Glottolog languoid with sibling nodes for the mapped
    # varieties.
    if multi:
        nodes = list(tree.walk())
        for n in nodes:
            if n.name in multi:
                for lid in multi[n.name]:
                    n.add_descendant(Node(lid))
                    n.name = ''

    tree.remove_redundant_nodes(keep_leaf_name=True)
    tree.visit(lambda n: setattr(n, 'length', None))
    return tree


def topology(t, level=0):  # pragma: no cover
    def branchname(n):
        if n.name:
            return n.name
        descs = [n.name for n in n.descendants if n.name]
        if descs:
            return sorted(descs)[0]
        return ''

    if t.name:
        yield t.name, level
    for node in sorted(t.descendants, key=branchname):
        yield from topology(node, level + 1)


def quartet(t, leafs):  # pragma: no cover
    import newick

    t = newick.loads(t)[0]
    t.prune_by_names(leafs, inverse=True)
    t.remove_redundant_nodes(keep_leaf_name=True)
    t.visit(lambda n: setattr(n, 'length', None))
    return tuple(topology(t)), t.newick


def quartet_distance(t1, t2):  # pragma: no cover
    import itertools
    import newick

    t1 = newick.read(t1)[0]
    t2 = newick.read(t2)[0]

    leafs = {n.name for n in t1.walk() if n.is_leaf}
    assert leafs == {n.name for n in t1.walk() if n.is_leaf}

    n1 = t1.newick
    n2 = t2.newick

    dist = 0
    for q in itertools.combinations(leafs, 4):
        q1 = quartet(n1, q)
        q2 = quartet(n2, q)
        if q1[0] != q2[0]:
            print('{} vs {}'.format(q1[1], q2[1]))
            dist += 1
    return dist
