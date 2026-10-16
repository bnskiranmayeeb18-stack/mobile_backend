# Mobile Reliability Research

## Problem
Mobile clients face network drops, app kills, duplicate requests.

## Solutions
1. Idempotency-Key: Header Idempotency-Key, server stores 24h
2. Sync Endpoint: POST /api/v1/rides/sync/ with client_events
3. Version Field: optimistic concurrency, If-Match
4. updated_at for delta sync: GET ?since=ISO8601
