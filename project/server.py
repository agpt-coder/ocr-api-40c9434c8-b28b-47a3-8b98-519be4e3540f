import logging
from contextlib import asynccontextmanager
from typing import List

import project.process_lead_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="OCR API 4",
    lifespan=lifespan,
    description="The API design focuses on receiving lead data through a POST request and generating a comprehensive scope of work proposal utilizing two instances of OpenAI's GPT-4. The primary instance drafts the initial version, while the second instance refines the draft by incorporating proven strategies from previous successful documents. Below are the key components of the project, synthesized from the information gathered:\n\n### Key Components:\n- **Endpoint Design**: An endpoint named '/process-lead' will accept POST requests containing lead data. The required fields for these requests are first_name, last_name, company_name, budget, timeline, and tech_used (an array of strings).\n\n- **Lead Data Processing**: Upon receiving a request, the initial lead data is processed to generate a context or prompt that will be used by the first GPT-4 instance. This involves parsing the input fields and converting them into a structured format that GPT-4 can understand.\n\n- **Initial Draft Generation**: The first GPT-4 instance uses the prepared prompt to compose an initial draft of the scope of work. This draft will encompass details like project objectives, deliverables, expected timelines, and estimated budgets.\n\n- **Refinement Process**: The rough draft is then passed to the second GPT-4 instance. Utilizing a database of strategies from successful scope of work documents, this instance refines the draft. It focuses on enhancing clarity, improving the structure, and ensuring the document aligns with client expectations and industry standards.\n\n- **Integration with FastAPI and Prisma PostgreSQL**: The API is built using FastAPI for its async capabilities and simplicity. Prisma is used as the ORM for PostgreSQL, ensuring efficient and safe database interactions. The interaction with GPT-4 is facilitated through OpenAI's Python SDK, with appropriate API keys and security measures in place.\n\n- **Return of Final Proposal**: Once the refinement process is complete, the final scope of work document is returned to the user in response to the initial POST request. This document is tailored to the provided lead data and incorporates both innovative and time-tested elements to ensure its effectiveness.\n\nThis design ensures a seamless and automated process for generating high-quality scope of work proposals, leveraging the latest in AI technology to provide customized and actionable plans for prospective clients.",
)


@app.post(
    "/process-lead", response_model=project.process_lead_service.ProcessLeadResponse
)
async def api_post_process_lead(
    first_name: str,
    last_name: str,
    company_name: str,
    budget: str,
    timeline: str,
    tech_used: List[str],
) -> project.process_lead_service.ProcessLeadResponse | Response:
    """
    Receives and processes lead data for scope of work generation.
    """
    try:
        res = await project.process_lead_service.process_lead(
            first_name, last_name, company_name, budget, timeline, tech_used
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
