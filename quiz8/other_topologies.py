"""
Question 5:

Create a belief network with five random variables A, B, C, D, and E with the following properties:

A and C are independent of any other variable (and each other).
D and E depend on each other unless B is given (observed).
Hints
The first property is expressing absolute independence of A and C from any other variable. In other words, no arc comes in or goes out of these nodes.
The second property is expressing conditional independence. It means D and E are independent of each other when B is given (observed).
The second property is achieved by the right topology (arrows/parents) and a set of different CPTS in D and E. [If the CPTs are the same, even though the topology allows dependence, they remain independent.]

"""

network = {
    'A': {
        'Parents': [],
        'CPT': {
            (): 0.2 # You can change this value
            }
        
    },
    'C': {
        'Parents': [],
        'CPT': {
            (): 0.2 # You can change this value
            }
        
    },
    'B': {
        'Parents': [],
        'CPT': {
            (): 0.51 # You can change this value
            }
        
    },
    'D': {
        'Parents': ["B"],
        'CPT': {
            (True,): 0.4, 
            (False,): 0.9
        }
    },
    'E': {
        'Parents': ["B"],
        'CPT': {
            (True,): 0.1, 
            (False,): 0.2
        }
    },
    
# add more variables

}

"""

Consider the belief network given in the answer box with three random variables A, B, and C. The topology of the network implies the following:

A influences B
A influences C
B and C are conditionally independent given A
Without modifying the topology of the network, change the CPTs such that B and C become independent (unconditionally).

Notes
You can achieve this by making B independent of A or by making C independent of A. While you could do this by simply removing one of the arcs (i.e. parents), here you are being asked to do this without changing the topology/parents and by only changing the CPTs.
The point of this exercise is to show that arcs allow dependence but do not enforce it. We can have an arc from A to B and still have the CPTs in B in a way that makes it independent of A.
When hand-designing belief networks, there is no point in changing CPTs in order to make two variables independent; instead you can (and should) modify the topology.
When the topology of the network is hand-designed but the CPTs are obtained by looking at data (machine learning), then the values obtained for CPTs may effectively make two variables independent. For example in this network if A is a disease and B and C are some tests, when designing the topology, you may consider A as influencing both B and C but after you use data to obtain the values in CPTs, in turns out that B is independent of A (i.e. does not provide useful information).

"""
            
            
network = {
    'A': {
        'Parents': [],
        'CPT': {
            (): 0.1
            }},
    'B': {
        'Parents': ['A'],
        'CPT': {
            (False,): 0.3,
            (True,): 0.3
            }},
            
    'C': {
        'Parents': ['A'],
        'CPT': {
            (False,): 0.5,
            (True,): 0.5
            }},
}
