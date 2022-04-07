import csv
import re


def uspatentcitation_parser(path):
    """
    Enter the path of uspatentcitation.tsv
    """
    feats = {}
    with open(path) as feed:
        file = csv.reader(feed, delimiter="\t")
        for row in file:
            for element in row:
                feats[element] = None
            break
        next(file)
        for row in file:
            if "patent_id" and "citation_id" in feats:
                yield (row[1], row[2])
            else:
                return "Elements not found"


def application_parser(path):
    """
    Enter the path of application.tsv
    """
    feats = {}
    with open(path) as feed:
        file = csv.reader(feed, delimiter="\t")
        for row in file:
            for element in row:
                feats[element] = None
            break
        next(file)
        for row in file:
            if "patent_id" and "number" in feats:
                yield (row[1], row[3])
            else:
                return "Elements not found"


def patent_inventor_parser(path):
    """
    Enter the path of patent_inventor.tsv
    """
    feats = {}
    with open(path) as feed:
        file = csv.reader(feed, delimiter="\t")
        for row in file:
            for element in row:
                feats[element] = None
            break
        next(file)
        for row in file:
            if "patent_id" in feats:
                yield (row[0])
            else:
                return "Element not found"


def inventor_parser(path):
    """
    Enter the path of inventor.tsv
    """
    feats = {}
    with open(path) as feed:
        file = csv.reader(feed, delimiter="\t")
        for row in file:
            for element in row:
                feats[element] = None
            break
        next(file)
        for row in file:
            if "id" in feats:
                yield (row[0])
            else:
                return "Element not found"


def patent_parser(path):
    """
    Enter the path of patent.tsv
    """
    feats = {}
    with open(path) as feed:
        file = csv.reader(feed, delimiter="\t")
        for row in file:
            for element in row:
                feats[element] = None
            break
        next(file)
        for row in file:
            if "type" and "number" in feats:
                yield (row[1], row[2])
            else:
                return "Elements not found"


def patent_lawyer_parser(path):
    """
    Enter the path of patent_lawyer.tsv
    """
    feats = {}
    with open(path) as feed:
        file = csv.reader(feed, delimiter="\t")
        for row in file:
            for element in row:
                feats[element] = None
            break
        next(file)
        for row in file:
            if "patent_id" and "lawyer_id" in feats:
                yield (row[0], row[1])
            else:
                return "Elements not found"


if __name__ == "__main__":
    path = r"/home/ftech/Code/dbs/uspatentcitation-small.tsv"
    parsed_uspatentcitation = uspatentcitation_parser(path)
    for row in parsed_uspatentcitation:
        patent_id, citation_id = row
        print(f"Patent {patent_id} cites patent {citation_id}")
