import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.claim_model import Claim
from app.repositories.claim_repository import ClaimRepository

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session 

    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def sample_claims(db_session):
    claims = [
        Claim(description="Claim 1"),
        Claim(description="Claim 2"),
        Claim(description="Claim 3")
    ]
    db_session.add_all(claims)
    db_session.commit()
    db_session.refresh(claims[0])
    db_session.refresh(claims[1])
    db_session.refresh(claims[2])
    return claims

def test_get_all_claims(db_session, sample_claims):
    claim_repo = ClaimRepository(db_session)

    claims = claim_repo.get_all_claims()

    assert len(claims) == len(sample_claims)

    assert claims[0].description == "Claim 1"
    assert claims[1].description == "Claim 2"
    assert claims[2].description == "Claim 3"
