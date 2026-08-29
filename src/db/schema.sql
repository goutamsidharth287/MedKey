-- Med Key's Supabase schema. Run this in the Supabase SQL editor before using the app.
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text not null,
  display_name text not null,
  analysis_count integer not null default 0 check (analysis_count >= 0),
  analysis_date date,
  created_at timestamptz not null default now()
);

create table if not exists public.report_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  analysis text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.report_messages (
  id uuid primary key default gen_random_uuid(),
  report_id uuid not null references public.report_sessions(id) on delete cascade,
  role text not null check (role in ('user', 'assistant')),
  content text not null,
  created_at timestamptz not null default now()
);

-- A database trigger creates the matching profile even when Supabase requires
-- email confirmation and the new user has no browser session yet.
create or replace function public.create_profile_for_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, display_name)
  values (
    new.id,
    coalesce(new.email, ''),
    coalesce(new.raw_user_meta_data ->> 'display_name', 'Med Key user')
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.create_profile_for_new_user();

alter table public.profiles enable row level security;
alter table public.report_sessions enable row level security;
alter table public.report_messages enable row level security;

create policy "profile owners manage their profile" on public.profiles
  for all using (auth.uid() = id) with check (auth.uid() = id);
create policy "users manage their own reports" on public.report_sessions
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "users manage messages in their reports" on public.report_messages
  for all using (exists (select 1 from public.report_sessions s where s.id = report_id and s.user_id = auth.uid()))
  with check (exists (select 1 from public.report_sessions s where s.id = report_id and s.user_id = auth.uid()));
