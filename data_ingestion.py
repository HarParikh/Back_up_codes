import neo4j
from neo4j import GraphDatabase

USERNAME = "neo4j"
PASSWORD = "test"


def create_patent(tx, patent):
    query = "MERGE (patent:Patent {patent:$patent})"
    tx.run(query, patent=patent)
    print(f"Created {patent} patent")


def create_organisation(tx, organisation):
    query = "MERGE (organisation:Organisation {organisation:$organisation})"
    tx.run(query, organisation=organisation)
    print(f"Created {organisation} organisation")


def create_law_firm(tx, law_firm):
    query = "MERGE (law_firm:Law_Firm {law_firm:$law_firm})"
    tx.run(query, law_firm=law_firm)
    print(f"Created {law_firm} law_firm")


def create_lawyer(tx, lawyer):
    query = "MERGE (lawyer:Lawyer {lawyer:$lawyer})"
    tx.run(query, lawyer=lawyer)
    print(f"Created {lawyer} lawyer")


def create_expert(tx, expert):
    query = "MERGE (expert:Expert {expert:$expert})"
    tx.run(query, expert=expert)
    print(f"Created {expert} expert")


def create_case_id(tx, case_id):
    query = "MERGE (case_id:Case_ID {case_id:$case_id})"
    tx.run(query, case_id=case_id)
    print(f"Created {case_id} case_id")


def create_case_number(tx, case_number):
    query = "MERGE (case_number:Case_Number {case_number:$case_number})"
    tx.run(query, case_number=case_number)
    print(f"Created {case_number} case_number")


def create_document(tx, document):
    query = "MERGE (document:Document {document:$document})"
    tx.run(query, document=document)
    print(f"Created {document} document")


def create_investigation_number(tx, investigation_number):
    query = "MERGE (investigation_number:Investigation_Number {investigation_number:$investigation_number})"
    tx.run(query, investigation_number=investigation_number)
    print(f"Created {investigation_number} investigation_number")


def create_patent_co_occurs(tx, patent_1, patent_2):
    query = """MATCH 
    (patent_1:Patent {patent:$patent_1}), \
    (patent_2:Patent {patent:$patent_2}) \
    MERGE \
    (patent_1)-[:CITES]->(patent_2)"""
    query = query.strip().replace("\n", "")
    tx.run(query, patent_1=patent_1, patent_2=patent_2)


def create_law_firm_hire(tx, law_firm_1, law_firm_2, organisation_1, organisation_2):
    """
    law_firm_1, organisation_1: For plaintiffs.
    law_firm_2, organisation_2: For defendants.
    """
    query = """MATCH (law_firm_1:Law_Firm {law_firm:$law_firm_1}), \
    (law_firm_2:Law_Firm {law_firm:$law_firm_2}), \
    (organisation_1:Organisation {organisation:$organisation_1}), \
    (organisation_2:Organisation {organisation:$organisation_2}) \
    MERGE (organisation_1)-[:HIRED]->(law_firm_1) \
    MERGE (law_firm_1)-[:REPRESENTS_PLAINTIFF]->(organisation_1) \
    MERGE (organisation_2)-[:HIRED]->(law_firm_2) \
    MERGE (law_firm_2)-[:REPRESENTS_DEFENDANT]->(organisation_2)"""
    query = query.strip().replace("\n", "")

    tx.run(
        query,
        law_firm_1=law_firm_1,
        law_firm_2=law_firm_2,
        organisation_1=organisation_1,
        organisation_2=organisation_2,
    )


def lawyer_firm_relationship(tx, lawyer_1, lawyer_2, law_firm_1, law_firm_2):
    """
    lawyer_1,law_firm_1: Plaintiff
    lawyer_2,plaintiff_2: Defendant
    """
    query = """ MATCH \
    (lawyer_1:Lawyer {lawyer:$lawyer_1}), \
    (lawyer_2:Lawyer {lawyer:$lawyer_2}), \
    (law_firm_1:Law_Firm {law_firm:$law_firm_1}), \
    (law_firm_2:Law_Firm {law_firm:$law_firm_2}) \
    
    MERGE (lawyer_1)-[:WORKS_AT]->(law_firm_1) \
    MERGE (lawyer_2)-[:WORKS_AT]->(law_firm_2)"""
    query = query.strip().replace("\n", "")

    tx.run(
        query,
        lawyer_1=lawyer_1,
        lawyer_2=lawyer_2,
        law_firm_1=law_firm_1,
        law_firm_2=law_firm_2,
    )


def expert_file_relation(tx, expert, document):
    """
    Expert who has filed the document for the case.
    """
    query = """MATCH \
    (expert:Expert {expert:$expert}), \
    (document:Document {document:$document}) \
    MERGE \
    (expert)-[:HAS_FILED {filing_date:datetime("2002-11-01"),issue_date:datetime("2008-02-01")}]->(document)"""
    query = query.strip().replace("\n", "")
    tx.run(query, expert=expert, document=document)


def owns_patent_relationship(tx, organisation_1, organisation_2, patent_1, patent_2):
    """
    organisation_1,patent_1: Plaintiff
    organisation_2,patent_2: Defendant
    """
    query = """MATCH \
    (organisation_1:Organisation {organisation:$organisation_1}), \
    (organisation_2:Organisation {organisation:$organisation_2}), \
    (patent_1:Patent {patent:$patent_1}), \
    (patent_2:Patent {patent:$patent_2}) \
    MERGE (organisation_1)-[:OWNS_PATENT]->(patent_1) \
    MERGE (organisation_2)-[:OWNS_PATENT]->(patent_2)"""
    query = query.strip().replace("\n", "")
    tx.run(
        query,
        organisation_1=organisation_1,
        organisation_2=organisation_2,
        patent_1=patent_1,
        patent_2=patent_2,
    )


def expert_patent_relationship(tx, expert, patent_1, patent_2):
    """
    patent_1: Plaintiff
    patent_2: Defendants
    """
    query = """MATCH  
    (expert:Expert {expert:$expert}), \
    (patent_1:Patent {patent:$patent_1}), \
    (patent_2:Patent {patent:$patent_2}) \
    MERGE (patent_1)-[:REFERED_BY]->(expert) \
    MERGE (patent_2)-[:REFERED_BY]->(expert)"""
    query = query.strip().replace("\n", "")
    tx.run(query, expert=expert, patent_1=patent_1, patent_2=patent_2)


def worked_on_relationship(tx, case_id, law_firm_1, law_firm_2):
    """
    case_id: The case id.
    law_firm_1: Firm representing plaintiff
    law_firm_2: Firm representing defendant
    """
    query = """MATCH \
    (case_id:Case_ID {case_id:$case_id}), \
    (law_firm_1:Law_Firm {law_firm:$law_firm_1}), \
    (law_firm_2:Law_Firm {law_firm:$law_firm_2}) \
    MERGE (law_firm_1)-[:WORKING_ON_CASE]->(case_id) \
    MERGE (law_firm_2)-[:WORKING_ON_CASE]->(case_id)"""
    query = query.strip().replace("\n", "")
    tx.run(
        query,
        case_id=case_id,
        law_firm_1=law_firm_1,
        law_firm_2=law_firm_2,
    )


def case_association_relationship(tx, case_no_1, case_no_2):
    """
    case_no_1,case_no_2: case_numbers associated with the main case.
    """
    query = """MATCH \
    (case_no_1:Case_Number {case_number:$case_no_1}), \
    (case_no_2:Case_Number {case_number:$case_no_2}) \
    MERGE (case_no_1)-[:ASSOCIATED_WITH]->(case_no_2) \
    MERGE (case_no_2)-[:ASSOCIATED_WITH]->(case_no_1)"""
    query = query.strip().replace("\n", "")
    tx.run(query, case_no_1=case_no_1, case_no_2=case_no_2)


def init_graph():
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(USERNAME, PASSWORD))
    print("Conncted to db successfully")
    return driver


if __name__ == "__main__":
    driver = init_graph()
    with driver.session() as session:
        session.write_transaction(create_patent, "733626032")
        session.write_transaction(create_patent, "780848832")
        session.write_transaction(create_patent_co_occurs, "733626032", "780848832")
        session.write_transaction(create_organisation, "APPLE INC")
        session.write_transaction(create_organisation, "IMMERSION CORPORATION")
        session.write_transaction(create_law_firm, "DLA PIPER LLC")
        session.write_transaction(create_law_firm, "IRELL & MANELLA LLC")
        session.write_transaction(create_lawyer, "James Heinz")
        session.write_transaction(create_lawyer, "Michael Flemming")
        session.write_transaction(create_case_id, "IPR2016-01187")
        session.write_transaction(create_case_number, "1:16-cv-00077")
        session.write_transaction(create_case_number, "1:16-cv-00325")
        session.write_transaction(create_expert, "Dr. Majid Sarrafzadeh")
        session.write_transaction(create_document, "Declaration.pdf")
        session.write_transaction(
            lawyer_firm_relationship,
            "James Heinz",
            "Michael Flemming",
            "DLA PIPER LLC",
            "IRELL & MANELLA LLC",
        )

        session.write_transaction(
            create_law_firm_hire,
            "DLA PIPER LLC",
            "IRELL & MANELLA LLC",
            "APPLE INC",
            "IMMERSION CORPORATION",
        )

        session.write_transaction(
            case_association_relationship, "1:16-cv-00077", "1:16-cv-00325"
        )

        session.write_transaction(
            worked_on_relationship,
            "IPR2016-01187",
            "DLA PIPER LLC",
            "IRELL & MANELLA LLC",
        )
        session.write_transaction(
            expert_patent_relationship,
            "Dr. Majid Sarrafzadeh",
            "733626032",
            "733626032",
        )
        session.write_transaction(
            owns_patent_relationship,
            "APPLE INC",
            "IMMERSION CORPORATION",
            "733626032",
            "780848832",
        )
        session.write_transaction(
            expert_file_relation, "Dr. Majid Sarrafzadeh", "Declaration.pdf"
        )
