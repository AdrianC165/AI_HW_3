import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {

    // Represents a clause (e.g., a disjunction of literals) and the parents it was derived from
    static class Clause {
        List<String> literals;       // The literals in this clause
        List<Integer> parents;       // IDs of the parent clauses used to derive this one (empty for input)

        Clause(Collection<String> literals, List<Integer> parents) {
            this.literals = new ArrayList<>(literals);
            this.parents = new ArrayList<>(parents);
        }

        // Two clauses are equal if they contain the same set of literals (order doesn't matter)
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Clause)) return false;
            Clause other = (Clause) o;
            return new HashSet<>(this.literals).equals(new HashSet<>(other.literals));
        }

        // Hash code is based on the set of literals
        @Override
        public int hashCode() {
            return new HashSet<>(literals).hashCode();
        }

        // For printing: show literals followed by their parent clause IDs
        @Override
        public String toString() {
            return String.join(" ", literals) + " " + parentsToString();
        }

        // Print parents in curly braces, or {} if none
        public String parentsToString() {
            if (parents.isEmpty()) return "{}";
            return "{" + String.join(", ", parents.stream().map(String::valueOf).toList()) + "}";
        }
    }

    public static void main(String[] args) throws IOException {
        // Expect a filename as the first argument
        if (args.length < 1) {
            System.out.println("Usage: java Main <input_file>");
            return;
        }

        // Read all lines from the input file
        List<String> lines = Files.readAllLines(Paths.get(args[0]));

        LinkedHashSet<Clause> initialClauses = new LinkedHashSet<>();   // KB (initial clauses)
        Queue<Clause> sos = new LinkedList<>();                         // Set of Support (starts with negated goal literals)
        Map<Clause, Integer> clauseIds = new LinkedHashMap<>();         // Assign unique IDs to clauses
        List<Clause> allClauseList = new ArrayList<>();                 // Keeps clauses in insertion order for printing
        int clauseId = 1;

        // Parse each line into a clause
        for (String line : lines) {
            line = line.trim();
            if (line.isEmpty()) continue;

            List<String> lits = Arrays.asList(line.split("\\s+"));
            Clause c = new Clause(lits, List.of());

            // If we haven't seen this clause before
            if (!clauseIds.containsKey(c)) {
                clauseIds.put(c, clauseId++);
                allClauseList.add(c);

                // If it's a unit clause, treat it as part of the negated goal → add to SOS
                if (lits.size() == 1) {
                    sos.add(c);
                }
            }
        }

        // allClauses is the main set we resolve against
        Set<Clause> allClauses = new LinkedHashSet<>(clauseIds.keySet());
        List<Clause> processed = new ArrayList<>();
        boolean contradictionFound = false;
        Clause contradiction = null;

        // Main resolution loop: while we still have things to try in the SOS
        while (!sos.isEmpty()) {
            Clause ci = sos.poll();

            // Try resolving ci with every clause in our knowledge base
            for (Clause cj : new ArrayList<>(allClauses)) {
                if (ci.equals(cj)) continue; // skip same clause

                // Try resolving ci and cj on all possible complementary literals
                for (Clause resolvent : resolveAll(ci, cj, clauseIds.get(ci), clauseIds.get(cj))) {

                    // If we derive the empty clause, we’ve proven the goal is valid
                    if (resolvent.literals.isEmpty()) {
                        clauseIds.put(resolvent, clauseId++);
                        allClauseList.add(resolvent);
                        contradiction = resolvent;
                        contradictionFound = true;
                        break;
                    }

                    // If it's a new clause, add it to our structures
                    if (!clauseIds.containsKey(resolvent)) {
                        clauseIds.put(resolvent, clauseId++);
                        allClauseList.add(resolvent);
                        sos.add(resolvent);         // New things go into the SOS for further resolution
                        allClauses.add(resolvent);  // And into our full clause set
                    }
                }

                if (contradictionFound) break;
            }

            if (contradictionFound) break;
            processed.add(ci); // Mark clause as processed
        }

        // Output all clauses with their IDs
        for (int i = 0; i < allClauseList.size(); i++) {
            Clause c = allClauseList.get(i);
            System.out.println((i + 1) + ". " + c);
        }

        // If we found contradiction, print the success message
        if (contradictionFound) {
            List<Integer> parents = contradiction.parents;
            System.out.println("Contradiction {" + parents.get(0) + ", " + parents.get(1) + "}");
            System.out.println("Valid");
        } else {
            System.out.println("Failure");
        }

        // Always show total number of clauses used/derived
        System.out.println("Total clauses: " + allClauseList.size());
    }

    // Try resolving every possible complementary literal pair between a and b
    public static List<Clause> resolveAll(Clause a, Clause b, int idA, int idB) {
        List<Clause> resolvents = new ArrayList<>();

        for (String lit : a.literals) {
            // Complement: ~p <-> p
            String complement = lit.startsWith("~") ? lit.substring(1) : "~" + lit;

            if (b.literals.contains(complement)) {
                // Build the resolvent clause (all literals from both, except the pair that cancels)
                Set<String> newLits = new LinkedHashSet<>(a.literals);
                newLits.addAll(b.literals);
                newLits.remove(lit);
                newLits.remove(complement);

                // Track where this resolvent came from
                Clause newClause = new Clause(newLits, List.of(idA, idB));
                resolvents.add(newClause);
            }
        }

        return resolvents;
    }
}
