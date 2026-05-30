-- ================================================
-- JAVIX BOT — Supabase jadvallar
-- Supabase SQL Editor'ga ko'chirib ishga tushiring
-- ================================================

-- 1. SUHBAT TARIXI
create table if not exists messages (
  id bigint generated always as identity primary key,
  user_id bigint not null,
  role text not null check (role in ('user', 'model')),
  content text not null,
  created_at timestamptz default now()
);

create index if not exists idx_messages_user_id on messages(user_id);
create index if not exists idx_messages_created_at on messages(created_at desc);

-- 2. XOTIRA (foydalanuvchi haqida)
create table if not exists memory (
  id bigint generated always as identity primary key,
  user_id bigint not null,
  key text not null,
  value text not null,
  updated_at timestamptz default now(),
  unique(user_id, key)
);

create index if not exists idx_memory_user_id on memory(user_id);

-- 3. ESLATMALAR
create table if not exists reminders (
  id bigint generated always as identity primary key,
  user_id bigint not null,
  text text not null,
  remind_at timestamptz not null,
  repeat text check (repeat in ('daily', 'weekly') or repeat is null),
  done boolean default false,
  created_at timestamptz default now()
);

create index if not exists idx_reminders_remind_at on reminders(remind_at);
create index if not exists idx_reminders_done on reminders(done);

-- ================================================
-- RLS (Row Level Security) o'chirish
-- Bot service_role key ishlatadi, RLS shart emas
-- ================================================
alter table messages disable row level security;
alter table memory disable row level security;
alter table reminders disable row level security;
