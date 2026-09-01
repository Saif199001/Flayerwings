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
- `lead_type`: `contact`, `social_audit`, `project`
- `source`
- `message`
- `social_profile_url`

For `social_audit`, `social_profile_url` is required.

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
- Public lead creation accepts only explicitly writable fields.
- Server-managed fields such as IDs, status, notes and timestamps are read-only.
- Validation errors use standard Django REST Framework validation responses.
- Frontend code must consume the documented response shapes and must not rely on undocumented fields.
