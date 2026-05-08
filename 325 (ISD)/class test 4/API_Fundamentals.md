# APIs: Depth + Test Prep (300 Lines)

## What is an API?

An **API (Application Programming Interface) is a contract** between a client (your React app in the browser) and a server (your Express backend). It defines how they communicate without knowing each other's internal workings.

**Why it exists**: Your frontend runs in the user's browser—code is public. Users can open DevTools and see it. If the frontend had direct database access:
- Credentials are exposed
- Users can write malicious database queries
- Data can be copied or deleted

**The API acts as a gatekeeper**: It validates requests, enforces permissions, hides credentials, and applies business logic. Frontend talks to API. API talks to Database. Frontend never touches the database.

**Analogy**: API is a waiter. You (client) don't go to the kitchen (database). You tell the waiter what you want, he fetches it from the kitchen and brings it back.

---

## The Request/Response Loop

Every API interaction follows this pattern:   

```
Frontend → POST /users    → API Server → (validates, applies logic) → Database ✓
           (with JSON body)             ↓
                          ← JSON Response ← (fetches data, formats)
```

1. **Client sends a request**: What it wants (method + endpoint + optional data)
2. **Server processes**: Validates, queries database, applies business logic
3. **Server responds**: Returns data (JSON) + status code

**Example**:
- **Request**: `POST https://api.example.com/posts` with body `{"title":"Hello","content":"World"}`
- **Response** (201 Created): `{"id":123,"title":"Hello","content":"World","createdAt":"2024-03-27"}`

---

## Endpoint Anatomy: 4 Parts

Every API endpoint has exactly 4 components:

1. **Base URL**: Where the server lives. `https://api.example.com`
2. **Path**: The resource you're targeting. `/users/123/posts/456`
3. **HTTP Method**: The action you're taking. GET, POST, PUT, DELETE
4. **Body**: Optional JSON data. `{"name":"Alice","email":"alice@example.com"}`

**Full Example**: 
```
PUT https://api.example.com/users/123
Body: {"name":"Alice Johnson","role":"admin"}
```

This updates user 123's name and role.

---

## HTTP Methods (CRUD Operations)

| Method | Action | Use Case | Example |
|--------|--------|----------|---------|
| **GET** | Read | Fetch data | `GET /posts/123` → Returns post content |
| **POST** | Create | Add new data | `POST /posts` → Creates new post |
| **PUT** | Update/Replace | Replace resource | `PUT /posts/123` → Replaces entire post |
| **DELETE** | Remove | Delete data | `DELETE /posts/123` → Removes post |

**Critical Rule**: GET must be **safe**—it never changes state. POST/PUT/DELETE change state. A server *could* let you GET when deleting, but it violates the contract and breaks other systems that expect GET to be side-effect-free.

---

## REST Design: The Golden Rules

**REST = Representational State Transfer**. It's a design pattern for building APIs.

### Rule 1: Resource-Based Naming (Use Nouns, Not Verbs)

❌ **Bad**: 
- `/getUsers` 
- `/deletePost` 
- `/fetchProfilePicture`

✅ **Good**: 
- `/users` 
- `/posts/{id}` 
- `/users/{id}/avatar`

Why? REST treats everything as a **resource**. You don't ask for actions; you ask for things.

### Rule 2: Hierarchy Shows Relationships

```
/users/123           → User with ID 123
/users/123/posts     → All posts by user 123
/users/123/posts/456 → Specific post (456) by user 123
```

This is self-documenting and scales.

### Rule 3: Query Parameters for Filtering & Pagination

```
GET /posts?limit=10&offset=20           → Get 10 posts, skip first 20
GET /users?role=admin&status=active     → Filter users by role and status
GET /posts?search=javascript&sort=date  → Search and sort
```

Query params don't change the resource; they filter it.

---

## Status Codes: What the Response Means

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK—Request succeeded | `GET /posts/123` returns the post |
| 201 | Created—Resource made | `POST /posts` creates new post |
| 400 | Bad Request—Client error | Missing required field in body |
| 401 | Unauthorized—Not authenticated | Missing/invalid API key |
| 403 | Forbidden—Forbidden access | User can't access this resource |
| 404 | Not Found—Resource missing | `GET /posts/9999` (doesn't exist) |
| 500 | Server Error—Server broke | Database crashed |

---

## Response Format (Always JSON)

Servers return **structured data** in JSON format:

```json
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "posts": [
    {"id": 456, "title": "First Post"},
    {"id": 789, "title": "Second Post"}
  ],
  "createdAt": "2024-01-15T10:30:00Z"
}
```

Error responses:
```json
{
  "error": "User not found",
  "code": 404,
  "timestamp": "2024-03-27T12:00:00Z"
}
```

---

## API Evolution: Why REST Dominates

| Year | Protocol | Pros | Cons |
|------|----------|------|------|
| 1999 | SOAP | Strict, validated | Verbose XML, complex |
| 2000 | **REST** | Simple, resource-based, uses HTTP natively | Potential over-fetching |
| 2015 | GraphQL | Query exactly what you need | Complex to learn |
| 2016 | gRPC | Ultra-fast, binary protocol | Requires special tools |

**Today**: REST is the industry standard. Learn it well.

---

## Real-World Operational Concerns

### API Versioning
Once you release an API, clients depend on it. You can't just remove endpoints.

```
GET /v1/users           → Old version (might be deprecated)
GET /v2/users           → New version with breaking changes
```

This prevents clients from breaking when you evolve the API.

### Authentication & Authorization
APIs need to know *who* is making requests and *what* they're allowed to do.

```
GET /users/123 -H "Authorization: Bearer YOUR_API_KEY"
```

Methods: API Keys (simple), OAuth (secure, delegated), JWT (stateless tokens).

### Rate Limiting
Prevent abuse. Limit requests per user per hour.

```
Response Headers:
X-RateLimit-Limit: 100        (You get 100 requests/hour)
X-RateLimit-Remaining: 47     (You have 47 left)
X-RateLimit-Reset: 1711612800 (Resets at this Unix timestamp)
```

---

## Summary: Key Takeaways

- **API = Contract**: Defines client-server communication.
- **Frontend ≠ Database**: API is the gatekeeper.
- **4-Part Endpoint**: Base URL, Path, Method, Body.
- **CRUD**: GET (read), POST (create), PUT (update), DELETE (delete).
- **REST Rules**: Nouns for endpoints, hierarchy for relationships, query params for filtering.
- **Always JSON**: Predictable, parseable.
- **Status Codes Matter**: 200, 201, 400, 401, 404, 500.
- **Versioning**: Prevents breaking existing clients.

---

## Q&A Session

**Q1: Why can't the frontend connect directly to the database?**
A: Frontend code is public (visible in DevTools). Direct DB access would expose credentials, allow malicious queries, and leave data unprotected. The API validates, applies business logic, and hides credentials.

**Q2: What's the difference between PUT and POST?**
A: POST *creates* new resources. PUT *replaces* entire resources. `POST /users` creates a new user. `PUT /users/123` replaces user 123 entirely.

**Q3: I want to get all posts by user 123 created after January 2024. How should I structure this request?**
A: `GET /users/123/posts?createdAfter=2024-01-01`. Resource hierarchy shows you want posts from user 123. Query param filters by date.

**Q4: Why does REST use nouns instead of verbs in endpoints?**
A: REST treats everything as a resource. Instead of asking "get me users," you ask for the `/users` resource with a GET method. This is composable and predictable.

**Q5: What does a 401 status code mean? How is it different from 403?**
A: **401 Unauthorized**: You didn't provide credentials (or they're invalid). System doesn't know who you are. **403 Forbidden**: System knows who you are, but you don't have permission to access this resource.

**Q6: Why do APIs return status codes along with the response body?**
A: Status codes tell the client whether the request succeeded or failed, and *why*. The body contains the actual data. Together, they provide complete information.

**Q7: If I release an API as `/users`, then later want to add new fields to the response, do I need `/v2/users`?**
A: No. Adding fields is backward-compatible. Old clients ignore new fields. Only use versioning if you *remove* fields or change behavior.

**Q8: What's rate limiting and why do servers use it?**
A: Rate limiting caps requests per user per time period. Without it, one user could make millions of requests, crashing the server or monopolizing resources. It protects server health and fairness.

