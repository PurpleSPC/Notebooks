# Week 1 - Knowledge
    link to source notes: https://cs50.harvard.edu/ai/notes/1/

## Vocab
    - sentence: an assertion about the world in a knowledge representation logic
    - propositional logic: 

## Propositional logic

### Proposition Symbols
    - ex, P Q and R
    - they represent a fact or sentence
### Logical Connectives and truth tables
    - **Not** (¬)
      - | P     | ¬P    |
        |-------|-------|
        | False | True  |
        | True  | False |  
    - **And** (∧)
      - | P     | Q     | P ∧ Q |
        |-------|-------|-------|
        | True  | True  | True  |
        | True  | False | False |
        | False | True  | False |
        | False | False | False |
    - **Or** (∨)
      - | P     | Q     | P ∨ Q |
        |-------|-------|-------|
        | True  | True  | True  |
        | True  | False | True  |
        | False | True  | True  |
        | False | False | False | 
    - **Implication** (→)
      - If P then Q. When P is false, no claim is made and Q. is _trivially_ true
      - "if it is raining, then i'm indoors" makes no claim if it itsn't raining
      - | P     | Q     | P → Q |
        |-------|-------|-------|
        | True  | True  | True  |
        | True  | False | False |
        | False | True  | True  |
        | False | False | True  |
    - **Biconditional** (↔)
      - is the same as P -> Q **and** Q -> P together
      - "if it is raining then i am indoors, if i'm indoors, it is raining"
      - | P     | Q     | P ↔ Q |
        |-------|-------|-------|
        | True  | True  | True  |
        | True  | False | False |
        | False | True  | False |
        | False | False | True  |
    - **Exclusive Or** (⊕)
      - One or the other. cant be both
      - "you can have ice cream **or** cake, **not** both"
      - | P     | Q     | P ⊕ Q|
        |-------|-------|-------|
        | True  | True  | False |
        | True  | False | True  |
        | False | True  | True  |
        | False | False | False |

### Model
    - an assignment of a truth value to every proposition
    - ex {P = True, Q = False}
### Knowledge base
    - a set of sentences known by the agent. 
### Entailment
    - in every model in which a sentence alpha is true, sentence beta is also true
    - α ⊨ β
    - "if it is a Tuesday in Jan, then the month is Jan."

## Inference
    - the process of deriving new sentences from old ones
    - Harry Potter example:
        1. If it didn’t rain, Harry visited Hagrid today.
        2. Harry visited Hagrid or Dumbledore today, but not both.
        3. Harry visited Dumbledore today. 
    - We want the model to come up with new facts using these facts:
       1. Harry did not visit Hagrid
       2. It rained today

### Model Checking Algorithm     
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

    - Enumerate all possible modelsv ( 2^3 possibilities)
      - | P     | Q     | R     | KB(reson)              |
        |-------|-------|-------|------------------------|
        | False | False | False | False(P is false)      |
        | False | False | True  | False(P is false)      |
        | False | True  | False | False(P is false)      |
        | False | True  | True  | False(P is false)      |
        | True  | False | False | False(R is false)      |
        | True  | False | True  | True                   |
        | True  | True  | False | False(Q is true)       |
        | True  | True  | True  | False(Q is true)       |

### Coding for model checking
```Python
from logic import *    # logic.py file defines classes for connectives, etc.

# Create new Symbol classes. Each of these represents a proposition
rain = Symbol('rain')   # it is raining
hagrid = Symbol('hagrid')   # harry visited hagrid
dumbledore = Symbol('dumbledore')   # harry visited dumbledore

# put everything we know to be true into a KB
knowledge = And(   # put everything we know to be true inside the and connective.
    Implication(Not(rain), hagrid),   # it is not raining implies harry visited hagrid
    Or(hagrid, dumbledore),   # harry visited dumbledore or hagrid
    Not(And(hagrid, dumbledore)),   # harry EITHER visited hagrid or dumbledore, not both
    dumbledore   # harry visited dumbledore
)
```   

 - Run the model Checking algorithm we need:
   - A knowledge base
   - a query (the proposition we are interested in)
   - Symbols: a list of all symbols (atomic propositions)
   - a model: as assignment of T/F values to symbols

```Python
def check_all(knowledge, query, symbols, model):
    """
    This function is recursive. Each recursion pops a symbol from the list and generates two models, one when the sybmol is True and one when the symbol is false, then recurses until all models have an assignment.
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