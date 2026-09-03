# Flayer Wings Platform

Shared SaaS infrastructure for Flayer Wings products.

Current foundation:

- Workspaces as the tenant boundary
- Workspace memberships and roles
- Product subscriptions with provider-neutral billing state
- Audit logs
- Workspace creation/list/detail APIs

Product domains should use this layer for tenancy instead of implementing separate user-to-tenant ownership models.
