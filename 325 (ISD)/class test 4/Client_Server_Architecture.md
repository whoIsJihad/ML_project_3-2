# Client-Server Architecture: Fundamentals

## Why Client-Server Exists

Imagine storing Netflix's entire database on your phone. Impossible: storage is limited, security is compromised, and syncing with millions of users breaks. **Solution**: One central server holds all data. Users (clients) request what they need.

## The Three-Tier Model

**Client** (Browser/App) → **Web Server** (Serves UI) → **API Server** (Business Logic) → **Database Server** (Data Storage)

### Client: The Requester
Your browser/phone. Displays UI to you. Makes HTTP requests. Cannot access the database directly (security rule).

### Web Server: The Frontend Gatekeeper
Serves HTML, CSS, JavaScript files. Even though the code *runs* in your browser, the server *delivers* it. Same static files go to every user.

### API Server: The Backend Logic
Handles complex business logic. Authenticates users. Connects to the database. Returns data in JSON format. Different users get different results.

### Database Server: The Vault
Stores all persistent data. Only the API Server talks to it (never the client directly). Example: When you post a tweet, the API Server writes it to the database.

## Static vs. Dynamic Content

| Type | Example | Source |
|------|---------|--------|
| **Static** | Landing page HTML | Web Server (same for all) |
| **Dynamic** | Your personalized dashboard | API Server (queries DB per user) |

## A Restaurant Analogy

- **You** = Client (customer makes a request)
- **Waiter** = Web Server (brings you the menu)
- **Chef & Kitchen** = API Server + Database (prepares custom meal based on request)
- **Suppliers** = Database (ingredients/data storage)

## Where Code Runs

Frontend JavaScript runs **on your computer**, but the Web Server **delivers** it.
Backend code runs **on the server**, not on your device.

## The Complete Request Flow

1. Browser requests: "Give me the dashboard HTML/CSS/JS"
2. Web Server responds with frontend code
3. Dashboard loads in your browser
4. JavaScript code makes API request: "Get my profile data"
5. API Server processes, queries database
6. Database returns user data
7. API Server sends JSON response
8. Frontend re-renders with your data

## Hosting

Hosting = Making servers publicly available on the internet via IP addresses/domain names. Your browser connects via HTTP/HTTPS.

