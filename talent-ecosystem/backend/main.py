


from fastapi import FastAPI
from pymemgraph import Memgraph
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Talent Ecosystem API",
    description="Backend for the gamified talent platform",
    version="0.1.0"
)

# Initialize Memgraph connection
memgraph = Memgraph(
    host=os.getenv("MEMGRAPH_HOST", "memgraph"),
    port=7687
)

# Initialize ChromaDB client
chroma_client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "chromadb"),
    port=8000,
    settings=Settings(
        chroma_client_auth_provider="token",
        chroma_client_auth_credentials=os.getenv("CHROMA_AUTH_TOKEN", "test-token")
    )
)

@app.get("/")
def read_root():
    return {"message": "Talent Ecosystem API is running"}

@app.get("/health")
def health_check():
    return {
        "memgraph": "connected" if memgraph._connection else "disconnected",
        "chromadb": "connected" if chroma_client.heartbeat() else "disconnected"
    }

# Graph schema initialization endpoint
@app.post("/init-graph")
def init_graph():
    # Create core node types
    memgraph.execute(
        """
        CREATE (:Person {id: 'system', type: 'System'});
        CREATE CONSTRAINT ON (p:Person) ASSERT p.id IS UNIQUE;
        CREATE (:Skill {name: 'Python', category: 'Programming'});
        CREATE CONSTRAINT ON (s:Skill) ASSERT s.name IS UNIQUE;
        CREATE (:Company {name: 'TechCorp', industry: 'Technology'});
        CREATE CONSTRAINT ON (c:Company) ASSERT c.name IS UNIQUE;
        """
    )
    return {"message": "Graph schema initialized"}

# Vector collection setup endpoint
@app.post("/init-vectors")
def init_vectors():
    collection = chroma_client.create_collection(
        name="talent_profiles",
        metadata={"hnsw:space": "cosine"}
    )
    return {"message": f"Vector collection created: {collection.name}"}


