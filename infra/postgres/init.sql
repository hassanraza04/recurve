-- Recurve app-metadata schema (Postgres).
-- This is the control plane: who the tenants are, which Stripe connections they
-- own (credentials encrypted at rest), and which users belong to which tenant.
-- The warehouse (DuckDB/BigQuery) holds the analytics; this holds the wiring.

create schema if not exists recurve;
set search_path to recurve, public;

-- tenants ---------------------------------------------------------------------
create table if not exists tenants (
    id           uuid primary key default gen_random_uuid(),
    slug         text not null unique,
    name         text not null,
    plan_tier    text not null default 'free'
                 check (plan_tier in ('free', 'pro', 'team')),
    status       text not null default 'active'
                 check (status in ('active', 'suspended')),
    is_demo      boolean not null default false,
    created_at   timestamptz not null default now()
);

-- users (identity comes from Clerk; we store the mapping + light profile) ------
create table if not exists users (
    id             uuid primary key default gen_random_uuid(),
    clerk_user_id  text not null unique,
    email          text not null,
    created_at     timestamptz not null default now()
);

-- membership: a user belongs to one or more tenants, with a role --------------
create table if not exists memberships (
    user_id     uuid not null references users (id) on delete cascade,
    tenant_id   uuid not null references tenants (id) on delete cascade,
    role        text not null default 'member'
                check (role in ('owner', 'admin', 'member')),
    created_at  timestamptz not null default now(),
    primary key (user_id, tenant_id)
);

-- connections: a tenant's link to a billing provider. The provider key is a
-- RESTRICTED Stripe key, Fernet-encrypted before it ever touches this table.
-- We keep only the ciphertext + a last4 for display; never the plaintext.
create table if not exists connections (
    id              uuid primary key default gen_random_uuid(),
    tenant_id       uuid not null references tenants (id) on delete cascade,
    provider        text not null default 'stripe'
                    check (provider in ('stripe')),
    mode            text not null default 'test'
                    check (mode in ('test', 'live')),
    encrypted_key   bytea not null,
    key_last4       text not null,
    status          text not null default 'pending'
                    check (status in ('pending', 'active', 'error', 'revoked')),
    last_synced_at  timestamptz,
    created_at      timestamptz not null default now(),
    -- one active connection per tenant+provider keeps ingest unambiguous
    unique (tenant_id, provider)
);

-- ingest_runs: a thin audit log of pipeline runs, one row per tenant per run --
create table if not exists ingest_runs (
    id            uuid primary key default gen_random_uuid(),
    tenant_id     uuid not null references tenants (id) on delete cascade,
    status        text not null default 'running'
                  check (status in ('running', 'succeeded', 'failed')),
    rows_loaded   bigint,
    started_at    timestamptz not null default now(),
    finished_at   timestamptz,
    error         text
);

create index if not exists idx_memberships_tenant on memberships (tenant_id);
create index if not exists idx_connections_tenant on connections (tenant_id);
create index if not exists idx_ingest_runs_tenant on ingest_runs (tenant_id, started_at desc);
