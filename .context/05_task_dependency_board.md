# Unified Task Matrix

## Epics & Subtasks

### Epic 1: Environment & Project Initialization [COMPLETED]
- [x] **TASK-001**: Configure Python 3.12 environment in `.venv` and install `requirements.txt`.
- [x] **TASK-002**: Symlink Go 1.22 binary and tidy Go modules in `app/src/`.
- [x] **TASK-003**: Compile frontend assets (TypeScript and Tailwind CSS via `npm run build`).
- [x] **TASK-004**: Verify `.env` configuration file keys and paths.

### Epic 2: Autonomous Context Architecture [COMPLETED]
- [x] **TASK-005**: Initialize `.context/` living memory matrix using `init_context.sh`.
- [x] **TASK-006**: Populate project manifest, architecture contracts, tech stack specs, repository map, and initial ADRs.

### Epic 3: Graphify Knowledge Graph [COMPLETED]
- [x] **TASK-007**: Run graphify file detection and AST extraction across Python, Go, TypeScript, and SQL code.
- [x] **TASK-008**: Build graph, cluster modules, detect god nodes & bridges, and label communities.
- [x] **TASK-009**: Export interactive HTML visualizer (`graphify-out/graph.html`) and generate `GRAPH_REPORT.md`.

### Epic 4: Local Database & Testing Verification [COMPLETED]
- [x] **TASK-010**: Install user-space PostgreSQL 18.6 and initialize local cluster on port 5432.
- [x] **TASK-011**: Resolve schema circular foreign key ordering in `app/db/schema.sql` and apply schema.
- [x] **TASK-012**: Seed local database (`seed_local_db.py`) with admin, student, and alumni test users and channels.
- [x] **TASK-013**: Resolve blueprint routing, template errors, and pool closure issues (`mydb.close()`).
- [x] **TASK-014**: Execute automated test suite (`pytest tests/`) and end-to-end integration tests with 100% pass rate.
