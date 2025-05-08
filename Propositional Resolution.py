import re
pattern_complement_literal=re.compile("¬[A-Z]")
pattern_literal=re.compile("[A-Z]")
# checks if the argument of the function is a literal
def check_literal(text):
    if len(pattern_complement_literal.findall(text))!=0 or len(pattern_literal.findall(text))!=0:
        return 1
    return 0
# provides the complement of a literal
def complement(literal):
    if len(pattern_complement_literal.findall(literal))!=0:
            return literal[1::]
    if len(pattern_literal.findall(literal))!=0:
            return "¬"+literal
# creating the clause set
def create_clause_set():
    clause_set=[]
    n=int(input("How many clauses are in the clause set?: "))
    for x in range(n):
        clause=input(f"Input clause number {x+1}: ").split(' ')
        for literal in clause:
            if not check_literal(literal):
                clause.remove(literal)
                print(f"\"{literal}\" is not a literal!")
        clause_set.append(clause)
    return(clause_set)

# checks for the empty set of clauses (unsatisfiability)
def check_unsatisfiable(clause_set):
     for clause in clause_set:
          if len(clause)<=0:
               return True
     return False

# the union of two clauses in case one contains
# the complement of a literal in the other
def union(clause_1,clause_2,literal):
     clause=clause_1+clause_2
     clause.remove(literal)
     clause.remove(complement(literal))
     clause=list(set(clause))
     return(clause)

# finding redundant clauses and correcting them
def check_redundant(clause):
     final_clause=[]
     for literal in clause:
          if complement(literal) not in clause:
               final_clause.append(literal)
     return final_clause

# main algorithm for the resolution method
def resolution_method(clause_set):
    seen=[]
    print("Resolution method steps:")
    for clause_1 in clause_set:
        for clause_2 in clause_set:
            for literal in clause_1:
                    if complement(literal) in clause_2:
                         if len(union(clause_1,clause_2,literal))!=0:
                              union_clause=check_redundant(union(clause_1,clause_2,literal))
                         else:
                              clause_set.append([])
                              print(f"After applying the resolution method for the clauses {clause_1} and {clause_2}, the empty clause was achieved.")
                              print("\n")
                              return False
                         if union_clause not in seen and len(union_clause)!=0:
                              clause_set.append(union_clause)
                              seen.append(union_clause)
                              print(f"After applying the resolution method for the clause sets {clause_1} and {clause_2}, the clause {union_clause} was added to the clause set.")
                         if check_unsatisfiable(clause_set):
                              print("\n")
                              return False
    # if the empty set of clauses hasn't been achieved
    # then the function returns True (satisfiable)
    print("\n")
    return True
    
                         
clause_set=create_clause_set()
print(clause_set,"\n")
# conclusion
if resolution_method(clause_set):
     print("Satisfiable, all possible clauses have been formed after applying the resolution method and the empty clause is not one of them.\n",clause_set)
else:
     print("Unsatifiable, applying the resolution method resulted in a empty clause.\n",clause_set)