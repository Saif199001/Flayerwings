# Flayer Wings 2.0 API Contract

Base URL: `/api/v1/`

## Health

`GET /api/v1/health/`

Response:
```json
{"status":"ok","service":"flayer-wings-api"}
```

## Leads

`POST /api/v1/leads/`

Accepted fields:
- `name` (required)
- `email` (required)
- `phone`
- `company`
- `website`
- `lead_type`: `contact`, `social_audit`, `tool`, `project`
- `source`
- `message`
- `social_profile_url`
- `tool_slug`
- `tool_document_id`
- `visitor_id`
- `session_id`
- `landing_path`
- `attribution` (object)

For `social_audit`, `social_profile_url` is required.

## Free Tools

`GET /api/v1/tools/`

Returns active Tier 1 free tools.

`GET /api/v1/tools/templates/<tool-slug>/`

Returns active persisted templates for a tool.

`POST /api/v1/tools/documents/`

Creates a persisted anonymous or authenticated document. Anonymous documents require a `visitor_id` for later history access.

`GET /api/v1/tools/documents/?visitor_id=<id>`

Returns document history for the supplied anonymous visitor. Authenticated users receive only their own documents.

`GET /api/v1/tools/documents/<uuid>/`

Returns one document owned by the authenticated user or anonymous visitor.

`GET /api/v1/tools/documents/<uuid>/pdf/?visitor_id=<id>`

Downloads a server-generated PDF for an authorized document.

`POST /api/v1/tools/events/`

Records tool usage/conversion events with optional UTM attribution and document linkage.

Supported event types: `tool_open`, `tool_start`, `tool_complete`, `document_created`, `pdf_downloaded`, `png_downloaded`, `copy`, `cta_click`, `lead_submitted`.

`GET /api/v1/tools/stats/<tool-slug>/`

Returns basic event counts and document totals for the tool. This endpoint is intended for internal analytics use and requires authentication/authorization; it must not be exposed as a public dashboard without appropriate access control.

## Projects

`GET /api/v1/projects/`

Returns published projects/products.

`GET /api/v1/projects/<slug>/`

Returns one published project/product.

Project types: `product`, `client`, `case-study`.

## Content

`GET /api/v1/content/`

Returns published site content.

`GET /api/v1/content/<key>/`

Returns one published content record.

## Contract rules

- Public read endpoints expose only published/active records.
- Public lead and tool event/document creation accepts only explicitly writable fields.
- Server-managed fields such as IDs, status, notes and timestamps are read-only.
- Anonymous document/history access is scoped by a client-generated visitor ID.
- Tool API endpoints use scoped DRF throttles; production deployments should use a shared cache backend for multi-worker rate limiting.
- Validation errors use standard Django REST Framework validation responses.
- Frontend code must consume the documented response shapes and must not rely on undocumented fields.
