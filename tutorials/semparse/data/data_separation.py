import csv

def split_data(labels, articles, articles_large, labeled_articles, unlabeled_articles):
    # get list of labeled/unlabeled cos
    with open(labels, 'rb') as labels_in,\
         open(articles, 'rb') as articles_in,\
         open(articles_large, 'rb') as articles_large_in,\
         open(labeled_articles, 'wb') as labeled_out,\
         open(unlabeled_articles, 'wb') as unlabeled_out:
        # Get labeled doc names (with and without number prefixes)
        label_reader = csv.reader(labels_in, delimiter='\t')
        label_reader.next()
        labeled_doc_names = set()
        for row in label_reader:
            (person1, person2, label) = row
            doc = person1[:person1.index(':')]
            labeled_doc_names.add(doc)
        # write articles_dev (and start of articles_train)
        reader = csv.reader(articles_in, delimiter='\t')
        writer_labeled = csv.writer(labeled_out, delimiter='\t')
        writer_unlabeled = csv.writer(unlabeled_out, delimiter='\t')
        doc_names_stripped = set()
        for row in reader:
            (doc, text) = row
            doc_names_stripped.add(doc[5:])
            if doc in labeled_doc_names:
                writer_labeled.writerow([doc, text])
            else:
                writer_unlabeled.writerow([doc, text])
        reader_large = csv.reader(articles_large_in, delimiter='\t')
        # add to articles_dev (avoiding files already included)
        botched = 0
        i = 1000
        for row in reader_large:
            try:
                (doc, text) = row
                if doc not in doc_names_stripped:
                    i += 1
                    writer_unlabeled.writerow(['{}_'.format(i) + doc, text])
            except:
                botched += 1
        print "Total botched: {}".format(botched)
        

def main():
    labels='gold_labels.tsv'
    articles='articles.tsv'
    articles_large='articles-1m.tsv'
    labeled_articles='articles_dev.tsv'
    unlabeled_articles='articles_train.tsv'
    split_data(labels, articles, articles_large, labeled_articles, unlabeled_articles)


if __name__ == '__main__':
    main()