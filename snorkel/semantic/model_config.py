configuration = {
    # general
    'parallelism': 1,
    'max_docs': 1500,
    'splits': [0,1],
    'verbose': True,
    'seed': 0,

    # Supervision
    'source': 'py',
    'include': ['correct', 'passing'],
    'include_closer_lfs': True,
    'remove_twins': False,
    'remove_useless': False,
    'remove_paren': False,
    'max_lfs': None,
    'max_train': None,
    'model_dep': False,
    'majority_vote': False,
    'traditional': False, # e.g, 1000
    'threshold': 1.0/3.0,
    'display_correlation': False,
    'display_marginals': False,
    'empirical_from_train': False,

    # Classification,
    'model': 'logreg',
    'n_search': 10,
    'n_epochs': 50,
    'rebalance': True,
    'b': 0.5,
    'lr': [1e-5, 1e-2],
    'l1_penalty': [1e-6, 1e-2],
    'l2_penalty': [1e-6, 1e-2],
    'print_freq': 5,
}