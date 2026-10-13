@"
# Database Design - Saved Services

## Models

### Service
- id: UUIDField PK, default=uuid4
- name: CharField(200) indexed
- description: TextField
- is_available: BooleanField indexed
- price: DecimalField
- created_at: DateTime auto_now_add

### SavedService
- id: UUIDField PK
- customer: FK -> AUTH_USER_MODEL, CASCADE, related_name=saved_services, db_index=True
- service: FK -> Service, CASCADE, related_name=saved_by, db_index=True
- created_at: DateTime auto_now_add, db_index=True

## Constraints
- UniqueConstraint: fields=[customer, service], name=unique_customer_service
  Reason: One user cannot save same service twice

## Indexes
- Index: fields=[customer, -created_at], name=idx_saved_cust_created
  Reason: Fast list query for user ordered by recent
- is_available index: filter available services
- name index: search

## Relationships
User 1 -- * SavedService
Service 1 -- * SavedService (saved_by)
User * -- * Service via SavedService (M2M through)

## ER Diagram
[User] ||--o{ [SavedService] }o--|| [Service]

## Query Examples
get_saved_services_for_customer(user) -> filter(customer=user).select_related('service')
save_service_for_customer -> get_or_create
remove_saved_service -> filter(id, customer).delete()

## Migration
python manage.py makemigrations saved_services
python manage.py migrate
"@ | Set-Content -Path docs/DATABASE_DESIGN.md -Encoding UTF8