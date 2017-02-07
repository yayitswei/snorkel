import os
import csv

def main():
    # First, execute:
    # corpus='signalmedia=1m.jsonl'
    # cat $corpus | jq -r '[.id, .content] | map(@json) | join("\t")' > articles-1m.tsv
    small_file='articles.tsv'
    large_file = 'articles-1m.tsv'
    final_file = 'articles'
    small_docs = set()
    with open(small_file, 'rb') as tsvin:
        reader = csv.reader(tsvin, delimiter='\t')
        for row in reader:
            (id, _) = row
            small_docs.add(id[5:])
    with open(large_file, 'rb') as tsvin:
        botched = 0
        reader = csv.reader(tsvin, delimiter='\t')
        for i, row in enumerate(reader):
            try:
                (id, text) = row
                if id in small_docs:
                    print i
                import pdb; pdb.set_trace()
            except ValueError:
                botched +=1
    # split_data(labels_file, labeled_docs_file, train=0.40, dev=0.40, test=0.20)


if __name__ == '__main__':
    main()