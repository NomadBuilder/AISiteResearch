# API Documentation

## Web API Endpoints

The Flask application provides REST API endpoints for enriching domains and retrieving stored data.

---

## Endpoints

### 1. Enrich and Store Domain

**POST** `/api/enrich`

Enrich a domain and automatically store results in both PostgreSQL and Neo4j databases.

**Request Body:**
```json
{
  "domain": "example.com",
  "source": "Manual entry",
  "notes": "Optional notes about this domain"
}
```

**Response (Success - 201):**
```json
{
  "message": "Domain enriched and stored successfully",
  "domain": "example.com",
  "data": {
    "domain": "example.com",
    "ip_address": "93.184.216.34",
    "country": "United States",
    "cms": "WordPress",
    "cdn": "Cloudflare",
    ...
  },
  "status": "success"
}
```

**Response (Already Exists - 200):**
```json
{
  "message": "Domain already exists in database",
  "domain": "example.com",
  "status": "exists"
}
```

**Response (Error - 400/500):**
```json
{
  "error": "Error message",
  "domain": "example.com",
  "status": "error"
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:5000/api/enrich \
  -H "Content-Type: application/json" \
  -d '{"domain": "purapdx.com", "source": "Test", "notes": "Test domain"}'
```

---

### 2. Get All Domains

**GET** `/api/domains`

Retrieve all enriched domains from the database.

**Response:**
```json
{
  "domains": [
    {
      "domain": "example.com",
      "source": "Manual entry",
      "ip_address": "93.184.216.34",
      "country": "United States",
      "cms": "WordPress",
      ...
    },
    ...
  ],
  "count": 10
}
```

**Example (curl):**
```bash
curl http://localhost:5000/api/domains
```

---

### 3. Get Specific Domain

**GET** `/api/domains/<domain>`

Retrieve enrichment data for a specific domain.

**Response (Success - 200):**
```json
{
  "domain": "example.com",
  "source": "Manual entry",
  "ip_address": "93.184.216.34",
  "country": "United States",
  "cms": "WordPress",
  "cdn": "Cloudflare",
  "payment_processor": "Stripe",
  ...
}
```

**Response (Not Found - 404):**
```json
{
  "error": "Domain not found"
}
```

**Example (curl):**
```bash
curl http://localhost:5000/api/domains/purapdx.com
```

---

### 4. Get Graph Data

**GET** `/api/graph`

Retrieve graph data from Neo4j for visualization.

**Response:**
```json
{
  "nodes": [
    {
      "id": "123",
      "label": "Domain",
      "properties": {
        "name": "example.com",
        "source": "Manual entry"
      }
    },
    ...
  ],
  "edges": [
    {
      "source": "123",
      "target": "456",
      "type": "HOSTED_ON"
    },
    ...
  ]
}
```

---

### 5. Get Statistics

**GET** `/api/stats`

Get statistics about the dataset.

**Response:**
```json
{
  "total_nodes": 50,
  "total_edges": 75,
  "node_types": {
    "Domain": 10,
    "Host": 5,
    "CDN": 3,
    "CMS": 2
  }
}
```

---

## Database Storage

### PostgreSQL (Relational Data)

**Tables:**
- `domains` - Domain metadata (domain, source, notes, timestamps)
- `domain_enrichment` - Enrichment data (IP, hosting, CMS, payment, etc.)

**Use Cases:**
- Query domains by country, CMS, hosting provider
- Export to CSV/JSON
- Search and filter domains

### Neo4j (Graph Relationships)

**Node Types:**
- `Domain` - Domains being tracked
- `Host` - IP addresses and hosting providers
- `CDN` - Content delivery networks
- `CMS` - Content management systems
- `PaymentProcessor` - Payment processors

**Relationships:**
- `Domain -[:HOSTED_ON]-> Host`
- `Domain -[:USES_CDN]-> CDN`
- `Domain -[:USES_CMS]-> CMS`
- `Domain -[:USES_PAYMENT]-> PaymentProcessor`

**Use Cases:**
- Visualize infrastructure relationships
- Find domains sharing same host/CDN
- Map infrastructure networks

---

## Storage Flow

```
1. User calls POST /api/enrich
   ↓
2. Domain is enriched (WHOIS, DNS, IP, CMS, etc.)
   ↓
3. Data stored in PostgreSQL (relational)
   ↓
4. Nodes and relationships created in Neo4j (graph)
   ↓
5. Response returned with enrichment data
```

---

## Example Usage

### JavaScript/Fetch
```javascript
// Enrich a domain
const response = await fetch('http://localhost:5000/api/enrich', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    domain: 'example.com',
    source: 'Web search',
    notes: 'Found via research'
  })
});

const data = await response.json();
console.log(data);
```

### Python/Requests
```python
import requests

# Enrich a domain
response = requests.post('http://localhost:5000/api/enrich', json={
    'domain': 'example.com',
    'source': 'Web search',
    'notes': 'Found via research'
})

data = response.json()
print(data)
```

---

## Notes

- Domains are automatically checked for duplicates before enrichment
- All enrichment data is stored persistently in databases
- Graph visualization updates automatically when new domains are added
- Data persists across server restarts (Docker volumes)

