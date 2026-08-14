
## Sprint 2 – Lesson 2: Configuration Management

### Problem

The application needs different settings for development, testing, and production without changing the source code.

### Decision

Use `pydantic-settings` as the single source of truth for application configuration.

### Why

- Type-safe configuration
- Automatic validation
- Centralized settings
- Easy to test
- Compatible with environment variables and cloud deployments

### Alternatives Considered

- `os.getenv()` throughout the project
  - Rejected because it scatters configuration logic and lacks validation.

### Lessons Learned

Configuration is infrastructure, not business logic. The application should read settings from a single validated object instead of directly from environment variables.

## Sprint 2 – Lesson 3: Database Foundation

### Problem
The application needs a safe, reusable way to communicate with PostgreSQL.

### Decision
Use SQLAlchemy Engine + Session pattern.

### Why
- Connection pooling
- Transaction management
- Database abstraction
- Seamless FastAPI integration

### Lessons Learned
The Engine manages connections, while the Session represents a unit of work. Every request receives its own Session, which is automatically closed after the response.

## Sprint 2 – Lesson 4: Database Versioning

### Problem
Python models and database tables can drift apart over time.

### Decision
Use Alembic to version the database schema.

### Why
- Track schema changes
- Reproducible deployments
- Rollback support
- Team collaboration

### Lessons Learned
Alembic treats the database schema like source code. Every structural change is captured in a migration file that can be applied consistently across environments.