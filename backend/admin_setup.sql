-- ═══════════════════════════════════════════════════════════════
-- Admin Setup SQL
-- Run this in Supabase → SQL Editor BEFORE running create_admins.py
-- ═══════════════════════════════════════════════════════════════

-- 1. Create admins table
CREATE TABLE IF NOT EXISTS admins (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('nmc', 'police')),
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- 2. Add status column to grievances (if not already there)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name='grievances' AND column_name='status'
  ) THEN
    ALTER TABLE grievances ADD COLUMN status TEXT NOT NULL DEFAULT 'submitted';
  END IF;
END $$;

-- 3. Add status column to crime_reports (if not already there)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name='crime_reports' AND column_name='status'
  ) THEN
    ALTER TABLE crime_reports ADD COLUMN status TEXT NOT NULL DEFAULT 'received';
  END IF;
END $$;

-- 4. Enable Row Level Security
ALTER TABLE admins ENABLE ROW LEVEL SECURITY;

-- 5. RLS: Only service_role (backend) can read admins table
--    This prevents any frontend from ever reading admin credentials
CREATE POLICY "Service role only" ON admins
  FOR ALL
  USING (auth.role() = 'service_role');

-- 6. Verify tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;