# Incident Simulation & Troubleshooting

## 1. Database Unavailable
Simulate: Stop Postgres / wrong DB_URL in.env
Log: `database | ERROR | connection failed | req_id=abc123`
Fix: Check DB_URL, restart postgres, check logs with request_id
Command: `docker-compose restart db`

## 2. Redis Unavailable
Simulate: `docker-compose stop redis`
Log: `redis | ERROR | ConnectionError`
Endpoint: /api/health/redis/ -> 503
Fix: Restart redis, check cache fallback

## 3. Invalid API Request
Simulate: `curl -X POST /api/v1/rides/ -d '{}'`
Log: `API_ERROR | 400 | RIDE_NOT_FOUND | req_id=xyz`
Fix: Global handler returns consistent {success:false, message, error_code}

## 4. Celery Task Failure
Simulate: Raise exception in task
Log: `TASK_FAILED | retry=1 | error=...`
Fix: Check flower dashboard, check retry pattern, logs with request_id trace: Mobile -> Django -> Service -> DB -> Celery same request_id