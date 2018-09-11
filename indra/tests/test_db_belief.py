from indra.db.belief import MockStatement, MockEvidence, populate_support
from indra.belief import BeliefEngine


def test_belief_calc_up_to_prior():
    be = BeliefEngine()
    test_stmts = [
        MockStatement(1, [MockEvidence('sparser'), MockEvidence('reach')]),
        MockStatement(2, MockEvidence('biopax')),
        MockStatement(3, MockEvidence('signor')),
        MockStatement(4, MockEvidence('biogrid')),
        MockStatement(5, MockEvidence('bel')),
        MockStatement(6, [MockEvidence('phosphosite'), MockEvidence('trips')]),
        ]
    be.set_prior_probs(test_stmts)
    results = {s.matches_key(): s.belief for s in test_stmts}
    print(results)
    assert len(results) == len(test_stmts), (len(results), len(test_stmts))
    assert all([0 < b < 1 for b in results.values()]), 'Beliefs out of range.'


def test_belief_calc_up_to_hierarchy():
    be = BeliefEngine()
    test_stmts = [
        MockStatement(1, [MockEvidence('sparser'), MockEvidence('reach')]),
        MockStatement(2, MockEvidence('biopax')),
        MockStatement(3, MockEvidence('signor')),
        MockStatement(4, MockEvidence('biogrid')),
        MockStatement(5, MockEvidence('bel')),
        MockStatement(6, [MockEvidence('phosphosite'), MockEvidence('trips')]),
        ]
    be.set_prior_probs(test_stmts)
    init_results = {s.matches_key(): s.belief for s in test_stmts}
    print(init_results)
    supp_links = [(1,2), (1,3), (2,3), (1,5), (4,3)]
    populate_support(test_stmts, supp_links)
    be.set_hierarchy_probs(test_stmts)
    results = {s.matches_key(): s.belief for s in test_stmts}
    print(results)

    # Test a couple very simple properties.
    assert len(results) == len(test_stmts), (len(results), len(test_stmts))
    assert all([0 < b < 1 for b in results.values()]), 'Beliefs out of range.'

    # Test the change from the initial.
    all_deltas_correct = True
    deltas_dict = {}
    for s in test_stmts:
        h = s.matches_key()
        b = s.belief

        # Get results
        res = {'actual': b - init_results[h]}

        # Define expectations.
        if s.supports:
            res['expected'] = 'increase'
            if res['actual'] <= 0:
                all_deltas_correct = False
        else:
            res['expected'] = 'no change'
            if res['actual'] != 0:
                all_deltas_correct = False

        deltas_dict[h] = res
    assert all_deltas_correct, deltas_dict

