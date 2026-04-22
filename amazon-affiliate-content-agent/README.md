# affiliate-content-agent

## Archive Status

This copy is retained only as an archived portfolio snapshot.

Active development should happen in:
`C:\Users\trenp\affiliate-content-agent`

That standalone project now contains the consolidated workflow, docs, tests, and Creators API scaffold that used to be split across both copies.

Beginner-friendly affiliate content workflow project with:
- product loading
- draft generation
- compliance checks
- approval queue review

## Current product source behavior

The app currently defaults to a local mock product provider for safe development.

- `PRODUCT_SOURCE_PROVIDER=mock` keeps the workflow fully local
- `PRODUCT_SOURCE_PROVIDER=creators_api` enables the signed Creators API request flow
- if the Creators API configuration is incomplete, the app falls back to the mock provider

This keeps the workflow usable while you validate the real Amazon endpoint details for your account.

## Environment configuration

Create a local `.env` file from `.env.example`.

Important settings:

- `AMAZON_ASSOCIATE_TAG`
- `PRODUCT_SOURCE_PROVIDER`

Future Creators API scaffold settings:

- `CREATORS_API_PUBLIC_KEY`
- `CREATORS_API_PRIVATE_KEY`
- `CREATORS_API_HOST`
- `CREATORS_API_REGION`
- `CREATORS_API_MARKETPLACE`
- `CREATORS_API_SERVICE`
- `CREATORS_API_PATH`
- `CREATORS_API_TARGET`
- `CREATORS_API_ITEM_IDS`

## Creators API notes

The app now includes a SigV4-style signed JSON request flow for Amazon's
Creators API path. The exact request body and endpoint shape can vary by
account and rollout, so the host, path, service, target, and item IDs are
configurable through environment variables.

Recommended first test:

1. Set `PRODUCT_SOURCE_PROVIDER=creators_api`
2. Add your Creators API credentials and endpoint details
3. Add one or more comma-separated ASINs to `CREATORS_API_ITEM_IDS`
4. Run `python -m app.main`

If the real provider is selected but required config is missing, the app
falls back to the local mock provider so development stays safe.

## Run the app

From the project root:

```bash
python -m app.main
```

## Run the review queue

From the project root:

```bash
python -m scripts.review_queue
```

## Why use module execution?

Running modules with `python -m ...` tells Python to treat the project root
as the import base. That makes package imports like `from app...` work
cleanly without adding manual `sys.path` hacks.
