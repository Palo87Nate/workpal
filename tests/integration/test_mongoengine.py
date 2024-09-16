import pytest
from mongoengine import disconnect, connect
from app.models import Documents, Candidate

@pytest.fixture(scope='function')
def mongo_test_db():
    disconnect()
    connect('mongoenginetest', host='mongomock://localhost')
    yield
    disconnect()

def test_document_creation(mongo_test_db):
    candidate = Candidate(first_name="John", last_name="Doe", position="Developer", experience=5)
    candidate.save()

    doc = Documents(candidate_id=candidate.id)
    doc.save()

    retrieved_doc = Documents.objects(candidate_id=candidate.id).first()
    assert retrieved_doc is not None
    assert retrieved_doc.candidate_id == candidate.id
