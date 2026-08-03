from app.db.session import SessionLocal
from app.keyword_search.repository import KeywordSearchRepository

db = SessionLocal()

repo = KeywordSearchRepository(db)

results = repo.search(
    organization_id=1,
    project_id=1,
    query="casual leave",
)

for chunk in results:
    print("=" * 80)
    print(chunk.chunk_index)
    print(chunk.content)