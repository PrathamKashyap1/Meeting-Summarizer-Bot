import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load user data
with open("userdata.json", "r") as f:
    user_data = json.load(f)

# Prepare vectors and metadata
vectors = []
id_to_user = {}
index_to_id = []

for i, (user_id, details) in enumerate(user_data.items()):
    skills_str = ", ".join(details["skills"])
    embedding = model.encode(f"skills: {skills_str}")
    vectors.append(embedding)
    id_to_user[user_id] = {
        "skills": skills_str,
        "experience": details["experience"],
        "availability": details["availability"]
    }
    index_to_id.append(user_id)

# Convert to numpy array for FAISS
vectors_np = np.array(vectors).astype("float32")

# Create FAISS index
dimension = vectors_np.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors_np)

# Function to match best users
def find_users_for_tasks(task_list):
    matched_users = []
    visited = set()

    for task in task_list:
        query_vec = model.encode(f"query: {task}").astype("float32").reshape(1, -1)
        distances, indices = index.search(query_vec, k=5)

        assigned = False
        for idx in indices[0]:
            user_id = index_to_id[idx]
            user_info = id_to_user[user_id]
            if user_id not in visited and user_info["availability"]:
                matched_users.append({"task": task, "user": user_id})
                visited.add(user_id)
                assigned = True
                break

        if not assigned:
            matched_users.append({"task": task, "user": None})

    return matched_users

# Example usage
if __name__ == "__main__":
    task_list = [
        "Design a promotional poster",
        "Create a marketing flyer",
        "Backend design for a mobile app"
    ]
    results = find_users_for_tasks(task_list)
    print(results)
