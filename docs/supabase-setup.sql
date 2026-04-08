-- docs/supabase-setup.sql
-- Supabaseのダッシュボード > SQL Editor で実行する

CREATE TABLE reservations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    machine     TEXT NOT NULL CHECK (machine IN ('bench_press', 'squat_rack', 'deadlift')),
    date        DATE NOT NULL,
    hour        SMALLINT NOT NULL CHECK (hour >= 10 AND hour <= 21),
    username    TEXT NOT NULL CHECK (char_length(username) BETWEEN 1 AND 20),
    created_at  TIMESTAMPTZ DEFAULT now(),

    UNIQUE (machine, date, hour)
);

-- クエリ高速化のためのインデックス
CREATE INDEX idx_reservations_machine_date ON reservations (machine, date);
