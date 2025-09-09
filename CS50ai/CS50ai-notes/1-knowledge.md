# Week 1 - Knowledge
*Link to source notes: https://cs50.harvard.edu/ai/notes/1/*

## **Vocabulary**
- **sentence**: an assertion about the world in a knowledge representation logic
- **propositional logic**: 

## **Propositional Logic**

### **Proposition Symbols**
- ex, P Q and R
- they represent a fact or sentence

### **Logical Connectives and Truth Tables**

#### **Not** (¬)
| P     | ¬P    |
|-------|-------|
| False | True  |
| True  | False |  

#### **And** (∧)
| P     | Q     | P ∧ Q |
|-------|-------|-------|
| True  | True  | True  |
| True  | False | False |
| False | True  | False |
| False | False | False |

#### **Or** (∨)
| P     | Q     | P ∨ Q |
|-------|-------|-------|
| True  | True  | True  |
| True  | False | True  |
| False | True  | True  |
| False | False | False | 

#### **Implication** (→)
- If P then Q. When P is false, no claim is made and Q is _trivially_ true
- "if it is raining, then i'm indoors" makes no claim if it isn't raining

| P     | Q     | P → Q |
|-------|-------|-------|
| True  | True  | True  |
| True  | False | False |
| False | True  | True  |
| False | False | True  |

#### **Biconditional** (↔)
- is the same as P → Q **and** Q → P together
- "if it is raining then i am indoors, if i'm indoors, it is raining"

| P     | Q     | P ↔ Q |
|-------|-------|-------|
| True  | True  | True  |
| True  | False | False |
| False | True  | False |
| False | False | True  |

#### **Exclusive Or** (⊕)
- One or the other. can't be both
- "you can have ice cream **or** cake, **not** both"

| P     | Q     | P ⊕ Q |
|-------|-------|-------|
| True  | True  | False |
| True  | False | True  |
| False | True  | True  |
| False | False | False |

### **Model**
- an assignment of a truth value to every proposition
- ex {P = True, Q = False}

### **Knowledge Base**
- a set of sentences known by the agent. 

### **Entailment**
- in every model in which a sentence alpha is true, sentence beta is also true
- α ⊨ β
- "if it is a Tuesday in Jan, then the month is Jan."

## **Inference**
- the process of deriving new sentences from old ones
- Harry Potter example:
    1. If it didn't rain, Harry visited Hagrid today.
    2. Harry visited Hagrid or Dumbledore today, but not both.
    3. Harry visited Dumbledore today. 
- We want the model to come up with new facts using these facts:
   1. Harry did not visit Hagrid
   2. It rained today

### **Model Checking Algorithm**     
- To determine if KB ⊨ α (can we conclude that α is true given our knowledge base of facts)
  - enumerate all possible models
  - only if every model where KB is true and α is true then KB ⊨ α
  - otherwise there is no entailment. 

- example:
    P: It is tuesday
    Q: It is raining
    R: Harry will go for a run

    KB: (P ∧ ¬Q)→R
    "If it **is** Tuesday and it is **not** raining then Harry will go for a run"

    what we know: P (it is tuesday), ¬Q (is is not raining) and (P ∧ ¬Q)→R

    Inference: R is true. Harry will run 

- Enumerate all possible models (2^3 possibilities)

| P     | Q     | R     | KB (reason)              |
|-------|-------|-------|--------------------------|
| False | False | False | False (P is false)       |
| False | False | True  | False (P is false)       |
| False | True  | False | False (P is false)       |
| False | True  | True  | False (P is false)       |
| True  | False | False | False (R is false)       |
| True  | False | True  | True                     |
| True  | True  | False | False (Q is true)        |
| True  | True  | True  | False (Q is true)        |

#### **Coding for Model Checking**
```python
from logic import *    # logic.py file defines classes for connectives, etc.

# Create new Symbol classes. Each of these represents a proposition
rain = Symbol('rain')   # it is raining
hagrid = Symbol('hagrid')   # harry visited hagrid
dumbledore = Symbol('dumbledore')   # harry visited dumbledore

# put everything we know to be true into a KB
knowledge = And(                        # put everything we know to be true inside the and connective.
    Implication(Not(rain), hagrid),     # it is not raining implies harry visited hagrid
    Or(hagrid, dumbledore),             # harry visited dumbledore or hagrid
    Not(And(hagrid, dumbledore)),       # harry EITHER visited hagrid or dumbledore, not both
    dumbledore                          # harry visited dumbledore
)
```   

- Run the model Checking algorithm we need:
  - A knowledge base
  - a query (the proposition we are interested in)
  - Symbols: a list of all symbols (atomic propositions)
  - a model: as assignment of T/F values to symbols

```python
def check_all(knowledge, query, symbols, model):
    """
    A function that recursively pops a symbol from the list and generates two models, one when the symbol is True and one when the symbol is false, then recurses until all models have an assignment.
    When all models are assigned, each model that the KB is true is evaluated to see if the query is also true.
    """

    # once all models have been assigned values
    if not symbols:

        # if the model evaluates to true and the query is also true
        if knowledge.evaluate(model):
            return query.evaluate(model)     # will return false for models that are true, but queries are false
        return True
    
    # choose a symbol from the remaining symbols
    remaining = symbols.copy()
    p = remaining.pop()

    # create a model where the symbol is true
    model_true = model.copy()
    model_true[p] = True

    # create a model where the symbol is false
    model_false = model.copy()
    model_false[p] = False

    # recurse both models until symbol list is empty
    return(check_all(knowledge, query, remaining, model_true), check_all(knowledge, query, remaining, model_false))
```
### **Inference Rules**
- the number of variables for model checking quickly becomes intractable. 
- we need a way to simplify the propositional logic
- we use inference rules to come up with conclusions based on the propositions

#### **Modus Ponens**
- (α → β) ∧ α  then  we know β is true
- "if it is raining, then harry is inside." 
- If we know it is raining, then we know harry is inside

#### **AND Elimination**
- (α ∧ β) then α is true and β is true
- "Harry is friends with Hermione and Ron." 
- Then we know harry is friends with hermione and harry is friends with ron

#### **Double Negation Elimination**
- ¬(¬α) then we know that α is true
- "It is NOT true that harry did NOT pass the test." 
- Then we know that harry passed the test

#### **Implication Elimination**
- turns an implication into an OR
- α → β then we know either ¬α OR β 
- "If it is raining, then harry is inside." 
- then we know either it is NOT raining OR harry is inside.

#### **Biconditional Elimination**
- turns a biconditional into 2 implications
- α ↔ β then we know α → β AND β → α 
- "if it is raining, then harry is inside AND if harry is inside then it is raining"

#### **DeMorgan's Law**
- Turn an AND into an OR/ vice versa
- ¬(α ∧ β) then we know ¬α OR ¬β  |  ¬(α OR β) then we know ¬α AND ¬β
- "It is NOT true that both harry and ron passed the test."
- we know either harry did not pass the test or ron did not pass the test
- can go both ways: "it is not true that harry OR ron passed the test"
- then we know harry did not pass the test AND ron did not pass the test

#### **Distributive Property**
- (α ∧ (β ∨ gamma)) then we know (alpha and beta) OR (alpha and gamma)

### **Theorem Proving as a Search Problem**
- initial state: starting KB
- actions: inference rules
- transition model: new KB after applying inference rule
- goal test: check statement we're trying to prove
- path cost function: number of steps in proof

### **Resolution**
- (P or Q) and ¬P -> Q
- P and ¬P "complement" each other (cancel out)
- (Ron is in the great hall) or (hermione is in the library)
- ron is not in the great hall -> hermione is in the library

- (P ∨ Q) ∧ (¬P ∨ R) then (Q or R)
- (ron is in the great hall) or (hermione is in the library)
- (ron is not in the great hall) or (harry is sleeping)
- concludes to (hermione is in the library) or (harry is sleeping)

### **Conjunctive Normal Form (CNF)**
- logical sentence that is a conjunction (conjunction means AND) of clauses
- used for inference by resolution
- ex: (A or B or C) and (D or ¬E) and (F or G)

#### **Clause**
- a clause is a disjunction of literals
- disjunction means OR 
- literals are a statement or not(statement)

#### **Process of Transforming to CNF**
- example problem: (P or Q) -> R
- eliminate biconditionals
  - none in example
- eliminate implications
  - ¬(P or Q) or R
- move ¬'s inwards with DeMorgan's Law
  - (¬P and ¬Q) or R
- use distributive law to put OR's inside clause AND's outside
  - (¬P or R) and (¬Q or R)

### **Inference by Resolution**
- to determine if KB ⊨ α:
  - check if (KB and ¬α) is a contradiction:
    - if so, then KB ⊨ α
    - otherwise no entailment

- convert (KB ∧ ¬α) to CNF
- keep checking to see if we can use resolution to produce a new clause
  - if ever we produce the empty clause: 
    - there is a contradiction and KB ⊨ α
  - if we can't further add new clauses:
    - no entailment

#### **Example Problem:**
- Does (A ∨ B) ∧ (¬B ∨ C) ∧ (¬C) entail A?

- (KB ∧ ¬α) in CNF:
  - (A ∨ B) ∧ (¬B ∨ C) ∧ (¬C) ∧ (¬A)
- (¬B ∨ C) and (¬C) resolve:
  - (A ∨ B) ∧ (¬B ∨ C) ∧ (¬C) ∧ (¬A) ∧ (¬B)
- (A ∨ B) and ¬B resolve:
  - (A ∨ B) ∧ (¬B ∨ C) ∧ (¬C) ∧ (¬A) ∧ (¬B) ∧ (A)
- (¬A) and (A) resolve to () - empty clause
  - entailment proven

```python
# Example implementation of resolution algorithm
def resolution_proof(kb_clauses, query):
    """
    Simple resolution proof implementation
    Returns True if KB entails query, False otherwise
    """
    # Add negation of query to KB
    negated_query = negate_literal(query)
    clauses = kb_clauses + [negated_query]
    
    # Keep applying resolution until no new clauses can be derived
    new_clauses = []
    while True:
        # Try to resolve all pairs of clauses
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = resolve(clauses[i], clauses[j])
                if resolvent is not None:
                    if is_empty_clause(resolvent):
                        return True  # Contradiction found, entailment proven
                    if resolvent not in clauses and resolvent not in new_clauses:
                        new_clauses.append(resolvent)
        
        # If no new clauses were derived, no entailment
        if not new_clauses:
            return False
        
        # Add new clauses and continue
        clauses.extend(new_clauses)
        new_clauses = []

def resolve(clause1, clause2):
    """
    Attempt to resolve two clauses
    Returns resolvent if possible, None otherwise
    """
    # Look for complementary literals
    for lit1 in clause1:
        for lit2 in clause2:
            if are_complementary(lit1, lit2):
                # Remove complementary literals and combine remaining
                resolvent = [l for l in clause1 if l != lit1] + [l for l in clause2 if l != lit2]
                return list(set(resolvent))  # Remove duplicates
    return None

def are_complementary(lit1, lit2):
    """Check if two literals are complementary (e.g., A and ¬A)"""
    return (lit1.startswith('¬') and lit2 == lit1[1:]) or (lit2.startswith('¬') and lit1 == lit2[1:])

def negate_literal(literal):
    """Negate a literal"""
    if literal.startswith('¬'):
        return [literal[1:]]
    else:
        return ['¬' + literal]

def is_empty_clause(clause):
    """Check if clause is empty (contradiction)"""
    return len(clause) == 0

# Example usage for the problem above
kb_clauses = [
    ['A', 'B'],      # (A ∨ B)
    ['¬B', 'C'],     # (¬B ∨ C)  
    ['¬C']           # (¬C)
]

query = 'A'

result = resolution_proof(kb_clauses, query)
print(f"Does KB entail A? {result}")  # Should print: Does KB entail A? True
```

### **Limitations of Propositional Logic**
- number and complexity of symbols

## **First Order Logic**
- an improvement on propositional logic

| Constant Symbols | Predicate Symbols |
|------------------|-------------------|
| minerva          | Person            |
| pomona           | House             | 
| horace           | BelongsTo         |
| gildroy          |                   |
| gryffyndor       |                   |
| fufflepuff       |                   |
| ravenclaw        |                   |
| slytherin        |                   |

- what a sentence looks like in FOL:
  - Person(minerva)                  # minerva is a person
  - House(gryffyndor)                # gryffyndor is a house
  - ¬House(minerva)                  # minerva is not a house
  - BelongsTo(minerva, gryffyndor)   # minerva belongs to gryffyndor

- Less symbols needed than propositional logic

### **Quantifiers**

#### **Universal Quantification**
- holds true for all values (∀)

**Example:**
```
∀x. BelongsTo(x, Gryffyndor) -> ¬BelongsTo(x, Hufflepuff)
```
- "for all values of x, if x belongs to gryffyndor, then x does not belong to hufflepuff"
- "anyone in gryffyndor is not in hufflepuff"

#### **Existential Quantification**
- holds true for at least one value (∃)

**Example:** 
```
∃x. House(x) ∧ BelongsTo(Minerva, x)
```
- "There exists an object x such that x is a house and minerva belongs to x"
- "minerva belongs to a house"

#### **Combining Quantifiers**
**Example:** 
```
∀x. Person(x) -> (∃y. House(y) ∧ BelongsTo(x,y))
```
- ∀x. Person(x)                                # for all objects x, if x is a person:
- -> (∃y. House(y) ∧ BelongsTo(x,y))           
  - ∃y. House(y)                               # there exists an object y such that y is a house 
  - ∧ BelongsTo(x,y)                           # and x belongs to y

```python
# First Order Logic Quantifiers in Python
class FOLModel:
    def __init__(self):
        self.domain = set()  # Universe of discourse
        self.predicates = {}  # Predicate interpretations
        self.constants = {}   # Constant interpretations
    
    def add_constant(self, name, value):
        """Add a constant to the domain"""
        self.constants[name] = value
        self.domain.add(value)
    
    def add_predicate(self, name, interpretation):
        """
        Add a predicate interpretation
        interpretation: dict mapping tuples to boolean values
        """
        self.predicates[name] = interpretation
    
    def check_universal(self, variable, condition_func):
        """Check if condition holds for all objects in domain"""
        for obj in self.domain:
            if not condition_func(obj):
                return False
        return True
    
    def check_existential(self, variable, condition_func):
        """Check if condition holds for at least one object in domain"""
        for obj in self.domain:
            if condition_func(obj):
                return True
        return False

# Example 1: Universal Quantification
# ∀x. BelongsTo(x, Gryffyndor) -> ¬BelongsTo(x, Hufflepuff)
def example_universal():
    model = FOLModel()
    
    # Add some students to the domain
    students = ['Harry', 'Hermione', 'Ron', 'Draco', 'Luna']
    for student in students:
        model.add_constant(student, student)
    
    # Define BelongsTo predicate
    belongs_to = {
        ('Harry', 'Gryffindor'): True,
        ('Hermione', 'Gryffindor'): True,
        ('Ron', 'Gryffindor'): True,
        ('Draco', 'Slytherin'): True,
        ('Luna', 'Ravenclaw'): True,
        ('Harry', 'Hufflepuff'): False,
        ('Hermione', 'Hufflepuff'): False,
        ('Ron', 'Hufflepuff'): False,
        ('Draco', 'Hufflepuff'): False,
        ('Luna', 'Hufflepuff'): False,
    }
    model.add_predicate('BelongsTo', belongs_to)
    
    # Check: ∀x. BelongsTo(x, Gryffindor) -> ¬BelongsTo(x, Hufflepuff)
    def condition(x):
        gryffindor_member = model.predicates['BelongsTo'].get((x, 'Gryffindor'), False)
        hufflepuff_member = model.predicates['BelongsTo'].get((x, 'Hufflepuff'), False)
        # If x belongs to Gryffindor, then x does not belong to Hufflepuff
        return not gryffindor_member or not hufflepuff_member
    
    result = model.check_universal('x', condition)
    print(f"∀x. BelongsTo(x, Gryffindor) -> ¬BelongsTo(x, Hufflepuff): {result}")
    return result

# Example 2: Existential Quantification
# ∃x. House(x) ∧ BelongsTo(Minerva, x)
def example_existential():
    model = FOLModel()
    
    # Add houses to domain
    houses = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    for house in houses:
        model.add_constant(house, house)
    
    # Define House predicate
    house_predicate = {house: True for house in houses}
    model.add_predicate('House', house_predicate)
    
    # Define BelongsTo predicate for Minerva
    minerva_belongs = {
        ('Minerva', 'Gryffindor'): True,
        ('Minerva', 'Hufflepuff'): False,
        ('Minerva', 'Ravenclaw'): False,
        ('Minerva', 'Slytherin'): False,
    }
    model.add_predicate('BelongsTo', minerva_belongs)
    
    # Check: ∃x. House(x) ∧ BelongsTo(Minerva, x)
    def condition(x):
        is_house = model.predicates['House'].get(x, False)
        minerva_belongs_to_x = model.predicates['BelongsTo'].get(('Minerva', x), False)
        return is_house and minerva_belongs_to_x
    
    result = model.check_existential('x', condition)
    print(f"∃x. House(x) ∧ BelongsTo(Minerva, x): {result}")
    return result

# Example 3: Combining Quantifiers
# ∀x. Person(x) -> (∃y. House(y) ∧ BelongsTo(x,y))
def example_combined():
    model = FOLModel()
    
    # Add people and houses to domain
    people = ['Harry', 'Hermione', 'Ron', 'Draco', 'Luna']
    houses = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    
    for person in people:
        model.add_constant(person, person)
    for house in houses:
        model.add_constant(house, house)
    
    # Define Person predicate
    person_predicate = {person: True for person in people}
    model.add_predicate('Person', person_predicate)
    
    # Define House predicate
    house_predicate = {house: True for house in houses}
    model.add_predicate('House', house_predicate)
    
    # Define BelongsTo predicate
    belongs_to = {
        ('Harry', 'Gryffindor'): True,
        ('Hermione', 'Gryffindor'): True,
        ('Ron', 'Gryffindor'): True,
        ('Draco', 'Slytherin'): True,
        ('Luna', 'Ravenclaw'): True,
    }
    model.add_predicate('BelongsTo', belongs_to)
    
    # Check: ∀x. Person(x) -> (∃y. House(y) ∧ BelongsTo(x,y))
    def condition(x):
        is_person = model.predicates['Person'].get(x, False)
        if not is_person:
            return True  # If not a person, implication is trivially true
        
        # Check if there exists a house y such that x belongs to y
        def house_condition(y):
            is_house = model.predicates['House'].get(y, False)
            belongs_to_y = model.predicates['BelongsTo'].get((x, y), False)
            return is_house and belongs_to_y
        
        return model.check_existential('y', house_condition)
    
    result = model.check_universal('x', condition)
    print(f"∀x. Person(x) -> (∃y. House(y) ∧ BelongsTo(x,y)): {result}")
    return result

# Run examples
if __name__ == "__main__":
    print("First Order Logic Quantifier Examples:")
    print("=" * 50)
    
    print("\n1. Universal Quantification:")
    example_universal()
    
    print("\n2. Existential Quantification:")
    example_existential()
    
    print("\n3. Combining Quantifiers:")
    example_combined()
```

