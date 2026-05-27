# ETL Pipeline & Data Integration System

A modular ETL and data integration system that simulates data movement from OLTP to OLAP environments with metadata-driven observability and a FastAPI-based execution interface.

## Overview

The project models a simplified data platform architecture consisting of:

- Synthetic OLTP data generation
- OLTP source database
- ETL ingestion and transformation pipeline
- OLAP/raw target database
- Metadata layer for pipeline tracking and observability
- REST API for pipeline execution and monitoring

## Features

- Modular ETL pipeline (OLTP → OLAP)
- Metadata-driven pipeline tracking (status, timestamps, errors)
- Structured execution logging
- REST API to trigger and inspect pipeline runs
- PostgreSQL-based simulation environment

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/runs` | Start pipeline execution |
| GET | `/runs` | List all pipeline runs |
| GET | `/runs/{run_id}` | Retrieve details for a specific run |

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQL

## Goals of the Project

This project focuses on:
- ETL and data pipeline architecture
- System integration patterns
- Metadata-driven observability
- API-based orchestration
- Separation of OLTP, OLAP, and operational metadata concerns
