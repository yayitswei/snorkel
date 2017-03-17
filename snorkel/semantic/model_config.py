configuration = {
    # general
    'db': None,
    'parallelism': 1,
    'max_docs': 1500,
    'splits': 3,
    'verbose': True,
    'seed': 0,

    # Supervision
    'source': 'py',
    'include': [],
    'max_lfs': None,
    'max_train': None,
    'model_dep': False,
    'majority_vote': False,
    'traditional': False,
    'threshold': 1.0/3.0,
    'display_correlation': False,
    'display_marginals': False,
    'empirical_from_train': False,

    # Classification,
    'model': 'logreg',
    'n_search': 10,
    'n_epochs': 50,
    'rebalance': True,
    'lr': None,
    'l1_penalty': None,
    'l2_penalty': None,
    'print_freq': 5,
}