# GridwayAI Python SDK

Official Python SDK for accessing GridwayAI's generative AI services — focused on technical document automation and compliance in the specific technical jargon of nuclear licensing.

### 🚀 Features

- Generate vector embeddings from plain text
- Designed to match the familiar feel of the OpenAI Python SDK
- Lightweight and simple to integrate

### 📦 Installation

```bash
pip install gridwayai
```

### Usage
```python
from gridwayai import GridwayAI

# Initialize the client
client = GridwayAI(api_key="your-api-key")

# Embed a single string or a list of strings
texts = ["What is nuclear fission?", "Reactor designs vary by fuel type."]
embeddings = client.embeddings(input=texts)

print(embeddings[0])  # First embedding vector
```

## Testing
```python
pip install pytest
pytest
```

## Reference
Create a new client.
```python
GridwayAI(api_key: str, base_url: Optional[str] = None)
```
`api_key`: Your GridwayAI API key

`base_url`: Optional override for API URL (defaults to https://api.gridwayai.com)

Get vector embeddings for a list of input strings.
`embeddings(input: List[str]) -> List[List[float]]`

## 🤝 License
MIT License. See LICENSE file for details.

📫 Contact
GridwayAI
www.gridwayai.com
Contact: support@gridwayai.com
