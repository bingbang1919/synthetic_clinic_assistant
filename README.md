# Synthetic Clinic Data Assistant

A local database assignment project: natural-language question -> GPT-generated SQL -> SQLite query -> GPT-generated plain-language answer. All patients, providers and clinical records are fictional. Not a clinical decision-support tool.

## Setup (Python 3.10 or newer)
1. Extract this project and open its folder in VS Code.
2. Open a terminal in that folder.
3. Create an environment: `python -m venv .venv`.
4. Activate it:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
   - If activation is restricted, select the .venv interpreter in VS Code or invoke its Python directly.
5. Run `python -m pip install -r requirements.txt`.
6. Copy `.env.example` to `.env` using your editor. Replace the placeholder with your own OpenAI API key. Do not share or submit this file.
7. The populated `clinic.db` is already included. To generate it again, deliberately delete that file and run `python seed_database.py`. The seed script refuses to overwrite an existing database.
8. Run `python -m unittest -v test_project`.
9. Run `python -m streamlit run app.py` and open the local browser address printed in the terminal.

## API requirements
You need an OpenAI API account with API access and sufficient billing/credits. A ChatGPT subscription alone is not an API key. The default model setting is gpt-4o-mini; change OPENAI_MODEL to an available model supporting the Responses API and JSON-object output if needed. Each successful question normally makes two API calls and can incur charges. There is no fake/offline AI mode: without a key, the database and tests work but AI answers do not.

## Included files
- schema.sql: seven relational tables, keys, constraints and indexes.
- clinic.db: seeded SQLite database.
- seed_database.py: reproducible fictional records using random seed 42.
- database.py: read-only query executor and schema loader.
- ai_queries.py: SQL-generation call and result-explanation call.
- app.py: Streamlit interface with SQL and results inspection.
- test_project.py: offline tests for data integrity and query safeguards.
- example_queries.sql and expected_answers.json: four manually runnable reference queries and verified results.
- database_diagram.pdf: table diagram with primary and foreign keys.
- requirements.txt, .env.example, .gitignore: environment configuration.

## Design and semantics
Patients have many visits, conditions, and prescriptions. Providers have many visits and prescriptions. patient_condition resolves the many-to-many patient/condition relationship. A patient has at most one recorded diagnosis per condition in this simplified schema. Each prescription is a distinct record, so renewals may produce multiple rows. There is no prescription-to-visit FK: prescriptions are modeled independently.

All dates are ISO YYYY-MM-DD. Reference date is fixed at 2026-10-13 to make answers reproducible. Last month means September 2026. Ages are computed from birth dates. A condition record does not establish active disease. An active prescription has start_date <= reference date and end_date NULL or >= reference date; it does not prove medication adherence.

The seed includes 100 patients, 8 providers, 500 visits, 10 conditions, and 15 medications. Patients 91-100 intentionally have no visits. Medication assignment is simplified fictional test data, not a clinical simulation or treatment recommendation. Provider and patient names are fictitious; identify people by ID because names are not unique.

## Query safeguards and limitations
The app uses a read-only connection, an SQLite authorizer that permits only selected reads/functions, single-statement execution, a three-second progress-handler budget, and a 200-row result cap. The cap limits displayed/fetched results, not the computation of whole-population aggregates. Read-only WITH queries are supported. Truncation is passed to the answer model. Prompts tell the model not to invent data or provide clinical advice. These controls are a classroom prototype, not a production security boundary. Aggregate errors and hallucinations remain possible; inspect SQL and verify results. The timeout is a SQLite VM progress check, not a hard operating-system deadline.

GPT sees the schema and your question in call one; it sees question, SQL and returned data in call two. Never use real patient information. API calls set store=False, which is not a guarantee of zero retention. Keep the app local; this project has no authentication or production deployment controls.

## Verification
The database, query executor and included offline tests were run in the build environment. Python source was syntax checked. Live API calls and the browser UI were not executed in that environment; finish validation locally with your key. Generated SQL and natural-language output can vary, so test the example questions and compare to expected_answers.json.

## Suggested demonstration
Show the diagram, explain the seed process, ask how many patients have diabetes, expand the SQL/results panel, ask which provider had the most visits last month, and show the active-prescription question to demonstrate multiple joins. Try a request to delete data to show that writes are disallowed.
