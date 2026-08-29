"""Central configuration for Med Key."""

PRODUCT_NAME = "Med Key"
PRODUCT_ICON = "🔑"
PRODUCT_TAGLINE = "Make your lab report easier to understand."

PDF_PAGE_LIMIT = 12
PDF_SIZE_LIMIT_MB = 10
ANALYSES_PER_DAY = 5
INACTIVITY_TIMEOUT_SECONDS = 30 * 60

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.2
GROQ_RESPONSE_TOKEN_LIMIT = 1800
