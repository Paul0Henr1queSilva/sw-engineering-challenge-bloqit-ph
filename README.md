# Dropoff Bloq

A Django + Django REST Framework project for managing **Bloqs**, **Lockers**, and **Rents** (rental flows).  
This README explains how to set up, run, test, authenticate (JWT), manage database migrations, and understand the main concepts of the system.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Environment Variables](#environment-variables)
6. [Database Migrations](#database-migrations)
7. [Running the Server](#running-the-server)
8. [Authentication (JWT) & Access Tokens](#authentication-jwt--access-tokens)
9. [API Standards](#api-standards)
12. [Testing](#testing)
---

## Overview

Dropoff Bloq manages the lifecycle of **smart lockers** and **parcel rentals**, including:

- Creating and managing **Bloqs** (physical locker units)
- Managing **Lockers** inside each Bloq
- Handling **Rents**, which represent the use of a locker by a user

The API is versioned (`/api/v1/`) and uses UUID fields (`bloqId`, `lockerId`, `rentId`) for all lookups instead of numeric database IDs.

---

## Architecture

### Apps and Models

**Bloq**
- Unique field: `bloqId` (UUID)
- Fields: `title`, `address`, timestamps
- Relationship: One-to-many with `Locker`

**Locker**
- Unique field: `lockerId` (UUID)
- FK to `Bloq`
- Fields: `status`, `isOccupied`
- Relationship: One-to-many with `Rent`

**Rent**
- Unique field: `rentId` (UUID)
- Optional FK to `Locker`
- Fields: `weight`, `size`, `status`
- Automatic transition rules (see [Business Logic](#business-logic))

**Enums**
- `RentStatus`: `CREATED`, `WAITING_DROPOFF`, `WAITING_PICKUP`, `DELIVERED`
- `RentSize`: `XS`, `S`, `M`, `L`, `XL`
- `LockerStatus`: `OPEN`, `CLOSED`

Each enum is stored using its **name** (e.g., `"DELIVERED"`, `"M"`, `"OPEN"`).

---

## Requirements

- Python 3.11+ (tested on 3.13)
- SQLite (default) or PostgreSQL 14+
- pip / venv
- (optional) `make`, `curl`

---

## Installation

```bash
# 1) Clone the repository
git clone https://github.com/Paul0Henr1queSilva/sw-engineering-challenge-bloqit-ph.git
cd dropoff_bloq

# 2) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -U pip
pip install -r requirements.txt
```

---

## Environment Variables

### Create a .env file (or set environment variables manually):

```bash
DJANGO_DEBUG=true
DJANGO_SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_DB_ENGINE=sqlite
DJANGO_DB_NAME=db.sqlite3
```


## Database Migrations

### First-time setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### When you change models

```bash
python manage.py makemigrations
python manage.py migrate
```

### Example workflow

```bash
# Add new model fields
python manage.py makemigrations bloq_api

# Review and apply
python manage.py migrate

## Running the Server
python manage.py runserver 127.0.0.1:8000
```

## Authentication (JWT) & Access Tokens

We use JWT (JSON Web Tokens) for authentication, via djangorestframework-simplejwt.
Each user generates their own access and refresh tokens.

### 1) Create a user

```bash
python manage.py createsuperuser
```

### 2) Obtain tokens (login)

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"p@ssw0rd"}'
```

```bash
{
  "access":  "<ACCESS_TOKEN>",
  "refresh": "<REFRESH_TOKEN>"
}
```

Response

```bash
{
  "access":  "<ACCESS_TOKEN>",
  "refresh": "<REFRESH_TOKEN>"
}
```

### 3) Call any API with the access token

```bash
curl http://127.0.0.1:8000/api/v1/lockers \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 4) Refresh token

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<REFRESH_TOKEN>"}'
```

### 5) Verify a token

```bash
curl -X POST http://127.0.0.1:8000/api/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token":"<ACCESS_OR_REFRESH_TOKEN>"}'
```

## API Standards

 - Prefix: /api/v1/
 - UUID Lookups: bloqId, lockerId, rentId
 - Format: JSON
 - Pagination: PageNumberPagination ({"count": ..., "results": [...]})
 - Auth: JWT Bearer tokens
 - Error Codes: 400, 401, 403, 404, 422, etc.


## Testing

### Run Tests

```bash
pytest -v
```
