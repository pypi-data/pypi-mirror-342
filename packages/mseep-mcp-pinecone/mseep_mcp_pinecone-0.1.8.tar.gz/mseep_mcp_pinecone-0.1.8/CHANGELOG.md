# Changelog

All notable changes to the MCP-Pinecone project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.8] - 2025-01-04
### Added
- Added `pinecone-store` prompt to store documents in Pinecone
- Added `pinecone-stats` tool to get stats about the Pinecone index
### Changed
- Refactoring across the codebase to make it more modular and easier to extend
- Removed `embed-document` tool
- Removed `chunk-document` tool

## [0.1.7] - 2025-01-01
### Added
- Updated prompt to `pinecone-query` because Zed can't use tools.

## [0.1.6] - 2024-12-31
### Added
- Added `chunk_enabled` argument to `process-document` tool to enable/disable chunking. Defaults to false.
- Added `list-documents` tool to list all documents in a namespace

## [0.1.5] - 2024-12-29
### Added
- Added `process-document` tool to combine chunking, embedding, and upserting documents into Pinecone
- Added `chunk-document` tool to explicitly chunk documents into chunks
- Added `embed-document` tool to explicitly embed documents into Pinecone
- Mention Pinecone api in README

## [0.1.4] - 2024-12-20
### Added
- Added `langchain` dependency for chunking
- Auto chunk documents by markdown headers

## [0.1.3] - 2024-12-20
### Added
- Namespace support for all vector operations (search, read, upsert)
- Explicit namespace parameter in tool schemas

### Changed
- Updated MCP package to latest version

## [0.1.0 - 0.1.2]
### Added
- Initial public release
- Basic Pinecone integration with MCP
- Semantic search capabilities
- Document reading and writing
- Metadata support