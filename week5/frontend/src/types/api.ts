/**
 * Generic API types for error handling and responses
 */

/**
 * Standard error response from backend
 */
export interface ApiError {
  code: string;
  message: string;
  details?: unknown;
}

/**
 * Error response envelope
 */
export interface ApiErrorResponse {
  ok: false;
  error: ApiError;
}

/**
 * Union type for API responses
 * Usage: ApiResponse<Note> could be Note | ApiErrorResponse
 *
 * @example
 * function handleResponse(response: ApiResponse<Note>) {
 *   if (response.ok) {
 *     console.log(response.data.title); // TypeScript knows this exists
 *   } else {
 *     console.log(response.error.message); // TypeScript knows this exists
 *   }
 * }
 */
export type ApiResponse<T> =
  | { ok: true; data: T }
  | { ok: false; error: ApiError };

/**
 * HTTP methods we use
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

/**
 * Request options (subset of fetch options)
 */
export interface RequestOptions {
  method?: HttpMethod;
  headers?: Record<string, string>;
  body?: unknown;
  signal?: AbortSignal;
}

/**
 * Pagination parameters (for Task 2, Task 8)
 */
export interface PaginationParams {
  page?: number;
  page_size?: number;
}

/**
 * Paginated response
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}
