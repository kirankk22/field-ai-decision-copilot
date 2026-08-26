# Field AI Decision Copilot

An AI-powered decision-support system for geospatial infrastructure detections.

## Project Goal

The system connects field detections from a geospatial platform with organizational knowledge using Retrieval-Augmented Generation (RAG).

The user selects a detection on the map and opens an AI Decision Copilot.

The copilot can:

- Understand the selected detection
- Retrieve relevant documents
- Scope information by client and area
- Provide source citations
- Calculate controlled costs
- Compare alternative actions
- Identify missing information
- Explain uncertainty

## Architecture

Map
→ Detection
→ FastAPI
→ RAG
→ Tools
→ LLM
→ Grounded Decision Support

## Project Structure

- `backend/` - FastAPI and AI services
- `frontend/` - React application
- `data/` - demonstration knowledge base
- `tests/` - automated tests
