from openai import OpenAI
 
client = OpenAI()
 
assistant = client.beta.assistants.create(
  name="Instructor",
  instructions="You are an expert penetration tester. You are tasked with providing guidance on specific task to a junior penetration tester.",
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Textbook")
 
# Ready the files for upload to OpenAI
file_paths = ["edgar/goog-10k.pdf", "edgar/brka-10k.txt"]
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
 
# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)