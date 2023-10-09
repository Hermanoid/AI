

example_network = {
    'Burglary': {
        'Parents': [],
        'CPT': {
            (): 0.001,
         }
    },
        
    'Earthquake': {
        'Parents': [],
        'CPT': {
            (): 0.002,
        }
    },

    'Alarm': {
        'Parents': ['Burglary','Earthquake'],
        'CPT': {
            (True,True): 0.95,
            (True,False): 0.94,
            (False,True): 0.29,
            (False,False): 0.001,
        }
    },

    'John': {
        'Parents': ['Alarm'],
        'CPT': {
            (True,): 0.9,
            (False,): 0.05,
        }
    },

    'Mary': {
        'Parents': ['Alarm'],
        'CPT': {
            (True,): 0.7,
            (False,): 0.01,
        }
    },
}

### Question 1:

# This is just counts
network_no_smoothing = {
    'Y': {
        'Parents': [],
        'CPT': {
            (): 4/7,
         }
    },
        
    'X1': {
        'Parents': ['Y'],
        'CPT': {
            (True,): 1/4,
            (False,): 3/3
        }
    },

    'X2': {
        'Parents': ['Y'],
        'CPT': {
            (True,): 1/4,
            (False,): 2/3
        }
    },

    'X3': {
        'Parents': ['Y'],
        'CPT': {
            (True,): 0/4,
            (False,): 0/3,
        }
    },
}

# This is smoothed
network = {
    'Y': {
        'Parents': [],
        'CPT': {
            (): 6/11,
         }
    },
        
    'X1': {
        'Parents': ['Y'],
        'CPT': {
            (True,): 3/8,
            (False,): 5/7
        }
    },

    'X2': {
        'Parents': ['Y'],
        'CPT': {
            (True,): 3/8,
            (False,): 4/7
        }
    },

    'X3': {
        'Parents': ['Y'],
        'CPT': {
            (True,): 2/8,
            (False,): 2/7,
        }
    },
}