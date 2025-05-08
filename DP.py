import re
pattern_complement_literal=re.compile("¬[A-Z]")
pattern_literal=re.compile("[A-Z]")

# checks if the argument of the function is a literal
def check_literal(text):
    if len(pattern_complement_literal.findall(text))!=0 or len(pattern_literal.findall(text))!=0:
        return 1
    return 0

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

# provides the complement of a literal
def complement(literal):
    if len(pattern_complement_literal.findall(literal))!=0:
            return literal[1::]
    if len(pattern_literal.findall(literal))!=0:
            return "¬"+literal

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
    
# find a clause set that contains only one literal
# and apply the one literal rule (one time)
def one_literal_rule(clause_set):
     for clause_1 in clause_set[:]:  # Use a copy of the list to avoid skipping elements
          if len(clause_1) == 1:
               literal = clause_1[0]
               clause_set.remove(clause_1)
               for clause_2 in clause_set[:]:  # Iterate over a copy to avoid skipping elements
                    if literal in clause_2:
                         clause_set.remove(clause_2)
                    elif complement(literal) in clause_2:
                         clause_2.remove(complement(literal))
               return True
     return False
        
# find a clause set that contains a pure literal
# and apply the pure literal rule (one time)
def pure_literal(clause_set):
     for clause_1 in clause_set[:]:
          for literal in clause_1:
               exist=0
               for clause_2 in clause_set:
                    if complement(literal) in clause_2:
                         exist=1
                         break
               if exist==0:
                    for clause_2 in clause_set:
                         if literal in clause_2:
                              clause_set.remove(clause_2)
                    return True
     return False
     
# applying resolution method (one time)
def resolution_method(clause_set):
    for clause_1 in clause_set:
        for clause_2 in clause_set:
            for literal in clause_1:
                    if complement(literal) in clause_2:
                         if len(union(clause_1,clause_2,literal))!=0:
                              union_clause=check_redundant(union(clause_1,clause_2,literal))
                         else:
                              clause_set.append([])
                              return False
                         union_clause=check_redundant(union(clause_1,clause_2,literal))
                         if union_clause not in clause_set and len(union_clause)!=0:
                              clause_set.append(union_clause)
                              return True
    return False
        
# applying DP
def DP(clause_set):
    while len(clause_set)!=0:
         if one_literal_rule(clause_set):
              print(f"The one literal rule can be applied, the clause set is now:\n{clause_set}")
              if [] in clause_set:
                    print("\n")
                    return False             
         elif pure_literal(clause_set):
              print(f"The 1st rule of DP can't be applied, but the pure literal rule can be applied. The clause set is now:\n{clause_set}")
              if [] in clause_set:
                    print("\n")
                    return False
         elif resolution_method(clause_set):
              print(f"The 1st and 2nd rules of DP cannot be applied, but resolution can be applied. The clause set is now:\n{clause_set}")
              if [] in clause_set:
                    print("\n")
                    return False
         else:
              if [] not in clause_set:
                    print("None of the rules can be applied.")
                    return True
    print("\n")
    return True

clause_set=create_clause_set()
print(clause_set,"\n")

# conclusion
if DP(clause_set):
     print("Satisfiable.\n",clause_set)
else:
     print("Unsatifiable, applying the DP method the empty clause was achieved.\n",clause_set)

               
