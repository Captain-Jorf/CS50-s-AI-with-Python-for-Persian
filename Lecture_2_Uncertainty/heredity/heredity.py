import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def _pass_prob(gene_count, mut):
    # probability that a parent with `gene_count` copies passes the gene
    if gene_count == 2:
        return 1 - mut
    if gene_count == 1:
        return 0.5
    return mut


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    """
    mut = PROBS["mutation"]
    total = 1

    for person in people:
        if person in two_genes:
            g = 2
        elif person in one_gene:
            g = 1
        else:
            g = 0

        mom = people[person]["mother"]
        dad = people[person]["father"]

        if mom is None and dad is None:
            gene_p = PROBS["gene"][g]
        else:
            if mom in two_genes:
                mg = 2
            elif mom in one_gene:
                mg = 1
            else:
                mg = 0
            if dad in two_genes:
                dg = 2
            elif dad in one_gene:
                dg = 1
            else:
                dg = 0

            pm = _pass_prob(mg, mut)
            pd = _pass_prob(dg, mut)

            if g == 2:
                gene_p = pm * pd
            elif g == 1:
                gene_p = pm * (1 - pd) + (1 - pm) * pd
            else:
                gene_p = (1 - pm) * (1 - pd)

        has = person in have_trait
        trait_p = PROBS["trait"][g][has]

        total *= gene_p * trait_p

    return total


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    """
    for person in probabilities:
        if person in two_genes:
            g = 2
        elif person in one_gene:
            g = 1
        else:
            g = 0
        probabilities[person]["gene"][g] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for field in probabilities[person]:
            s = sum(probabilities[person][field].values())
            if s == 0:
                continue
            for key in probabilities[person][field]:
                probabilities[person][field][key] /= s


if __name__ == "__main__":
    main()