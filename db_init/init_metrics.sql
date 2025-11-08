
GRANT pg_monitor TO postgres;

GRANT SELECT ON pg_stat_activity TO postgres;
GRANT SELECT ON pg_stat_database TO postgres;

CREATE OR REPLACE FUNCTION pg_total_tables() RETURNS bigint AS $$
  SELECT count(*) FROM pg_tables WHERE schemaname = 'public';
$$ LANGUAGE sql;

-- Примечание: В PostgreSQL 10+ роль pg_monitor включена, но явное предоставление прав
-- на pg_stat_activity и pg_stat_database часто решает проблему.