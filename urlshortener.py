import redis
import uuid

# Connect to local Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Function to generate a unique short code using UUID
def generate_code(length=6):
    return uuid.uuid4().hex[:length]

# Shorten a long URL
def shorten_url(long_url):
    # Check if this URL is already shortened
    existing_code = r.get(f"long:{long_url}")
    if existing_code:
        return existing_code

    while True:
        short_code = generate_code()
        if not r.exists(f"short:{short_code}"):
            break

    # Store bidirectional mappings
    r.set(f"short:{short_code}", long_url)
    r.set(f"long:{long_url}", short_code)
    return short_code

# Retrieve the original long URL using short code
def redirect_to_long(short_code):
    long_url = r.get(f"short:{short_code}")
    if not long_url:
        return "URL not found"
    return long_url

# Example usage:
if __name__ == "__main__":
    long = "https://www.example.com/article/123456789"
    code = shorten_url(long)
    print("Short code:", code)
    print("Redirects to:", redirect_to_long(code))
