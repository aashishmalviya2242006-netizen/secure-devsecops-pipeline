from datetime import timedelta

# Secret key used to sign JWTs
SECRET_KEY = "your_super_secret_key_for_devsecops_project_2026"

# JWT signing algorithm
ALGORITHM = "HS256"

# Access token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Optional timedelta object for convenience
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
