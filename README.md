---
date: 2024-04-17T04:07:40.973875
author: AutoGPT <info@agpt.co>
---

# OCR API 4

The API design focuses on receiving lead data through a POST request and generating a comprehensive scope of work proposal utilizing two instances of OpenAI's GPT-4. The primary instance drafts the initial version, while the second instance refines the draft by incorporating proven strategies from previous successful documents. Below are the key components of the project, synthesized from the information gathered:

### Key Components:
- **Endpoint Design**: An endpoint named '/process-lead' will accept POST requests containing lead data. The required fields for these requests are first_name, last_name, company_name, budget, timeline, and tech_used (an array of strings).

- **Lead Data Processing**: Upon receiving a request, the initial lead data is processed to generate a context or prompt that will be used by the first GPT-4 instance. This involves parsing the input fields and converting them into a structured format that GPT-4 can understand.

- **Initial Draft Generation**: The first GPT-4 instance uses the prepared prompt to compose an initial draft of the scope of work. This draft will encompass details like project objectives, deliverables, expected timelines, and estimated budgets.

- **Refinement Process**: The rough draft is then passed to the second GPT-4 instance. Utilizing a database of strategies from successful scope of work documents, this instance refines the draft. It focuses on enhancing clarity, improving the structure, and ensuring the document aligns with client expectations and industry standards.

- **Integration with FastAPI and Prisma PostgreSQL**: The API is built using FastAPI for its async capabilities and simplicity. Prisma is used as the ORM for PostgreSQL, ensuring efficient and safe database interactions. The interaction with GPT-4 is facilitated through OpenAI's Python SDK, with appropriate API keys and security measures in place.

- **Return of Final Proposal**: Once the refinement process is complete, the final scope of work document is returned to the user in response to the initial POST request. This document is tailored to the provided lead data and incorporates both innovative and time-tested elements to ensure its effectiveness.

This design ensures a seamless and automated process for generating high-quality scope of work proposals, leveraging the latest in AI technology to provide customized and actionable plans for prospective clients.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'OCR API 4'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
