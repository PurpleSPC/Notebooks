# Logic Flow
- Is a safe move available?|  Yes -> make safe move
                           |  No -> make random move

- Add new sentence (neighbors, count) to KB
- for cells not in mines or safes:
  - does KB entail "mine"?
    - copy KB
    - add "not mine" to KB.copy
    - new_clauses = []
    - while true:
      - resolve pairs of clauses in kb.copy
        - if contradiction found, empty clause, entailment proven, cell is a mine, return true
        - otherwise add new clause to new clauses
        - if no new clauses, no entailment, return false
        - add new clauses to KB and continue loop