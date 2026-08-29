# Med Key

Med Key is an independently written Streamlit application for making text-based lab-report PDFs easier to understand. It offers account access, private saved report sessions, an AI-generated educational explanation, and report-grounded follow-up questions.

It is not a diagnostic or treatment tool. Med Key does not provide medication, dosages, or medical decisions. Users should consult a qualified clinician for personal advice.

## Stack

- Streamlit for the web application
- Groq and `llama-3.3-70b-versatile` for AI responses
- Supabase for sign-in and private persistence
- pypdf for extracting text from PDFs

## Run locally

1. Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the packages.

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a Supabase project. In its SQL editor, run [`src/db/schema.sql`](src/db/schema.sql). This creates the data tables and row-level-security rules so users can only access their own information.

4. Copy the secrets template to `.streamlit/secrets.toml`, then enter your own Supabase URL, Supabase anon key, and Groq API key.

   ```powershell
   Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
   ```

5. Start Med Key.

   ```powershell
   streamlit run src/main.py
   ```

## Repository structure

```text
med-key/
├── .streamlit/                 # local secret template
├── src/
│   ├── agents/                 # report review and report-grounded chat
│   ├── auth/                   # Supabase access and session lifecycle
│   ├── components/             # Streamlit screens and navigation
│   ├── config/                 # product settings, prompts, demo data
│   ├── db/                     # Supabase schema and RLS policies
│   ├── services/               # Groq client adapter
│   └── main.py                 # application entry point
├── LICENSE                     # MIT license
└── requirements.txt
```

## Before publishing

- Keep `.streamlit/secrets.toml` out of Git. The supplied `.gitignore` already does this.
- Replace the copyright holder in `LICENSE` with your name or legal entity, if desired.
- Configure Supabase email confirmation and redirect URLs for your deployment domain.
- Review your hosting provider's privacy, security, and health-information requirements before accepting real health records.

## Ownership and attribution

This Med Key codebase was written independently. It uses standard third-party libraries subject to their own licenses and is released under the MIT License included in this repository.
