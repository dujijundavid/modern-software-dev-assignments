/**
 * Base API client with error handling and type safety
 *
 * WHY THIS DESIGN:
 * - Type-safe: All requests and responses are typed
 * - Error handling: Structured error responses
 * - AbortSignal support: Cancel requests on component unmount
 * - Reusable: Used by all service modules
 */

import type {
  ApiError,
  RequestOptions,
} from '../types/api';

/**
 * Base URL for API (can be overridden via env var)
 * Empty in development (uses Vite proxy)
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

/**
 * Custom error class for API errors
 *
 * @example
 * try {
 *   await apiRequest('/notes/', { method: 'POST', body: {...} });
 * } catch (error) {
 *   if (error instanceof ApiRequestError) {
 *     console.error(error.code, error.message);
 *   }
 * }
 */
export class ApiRequestError extends Error {
  public readonly statusCode: number;
  public readonly code: string;
  public readonly details?: unknown;

  constructor(message: string, statusCode: number, code: string, details?: unknown) {
    super(message);
    this.name = 'ApiRequestError';
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
  }
}

/**
 * Parse JSON response safely
 *
 * Validates content-type and catches parse errors
 */
async function parseJSON<T>(response: Response): Promise<T> {
  const contentType = response.headers.get('content-type');

  if (!contentType?.includes('application/json')) {
    throw new ApiRequestError(
      `Expected JSON response, got ${contentType}`,
      response.status,
      'INVALID_RESPONSE_TYPE'
    );
  }

  try {
    return await response.json();
  } catch (error) {
    throw new ApiRequestError(
      `Failed to parse JSON: ${error instanceof Error ? error.message : 'Unknown error'}`,
      response.status,
      'JSON_PARSE_ERROR'
    );
  }
}

/**
 * Make an API request with full type safety
 *
 * @param endpoint - API endpoint (e.g., '/notes/')
 * @param options - Request options
 * @returns Promise<T> - Typed response data
 *
 * @example
 * const notes = await apiRequest<Note[]>('/notes/');
 * const note = await apiRequest<Note>('/notes/1');
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const {
    method = 'GET',
    headers = {},
    body,
    signal,
  } = options;

  const url = `${API_BASE_URL}${endpoint}`;

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...headers,
    },
    signal,
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      // Try to parse error response
      let errorData: ApiError;
      try {
        const parsed = await parseJSON<{ ok: false; error: ApiError }>(response);
        errorData = parsed.error;
      } catch {
        // Fallback to status text
        errorData = {
          code: response.status.toString(),
          message: response.statusText || 'An error occurred',
        };
      }

      throw new ApiRequestError(
        errorData.message,
        response.status,
        errorData.code,
        errorData.details
      );
    }

    return await parseJSON<T>(response);
  } catch (error) {
    // Re-throw ApiRequestError as-is
    if (error instanceof ApiRequestError) {
      throw error;
    }

    // Network errors or other issues
    if (error instanceof Error) {
      throw new ApiRequestError(
        error.message,
        0,
        'NETWORK_ERROR'
      );
    }

    throw new ApiRequestError(
      'An unknown error occurred',
      0,
      'UNKNOWN_ERROR'
    );
  }
}

/**
 * GET request helper
 *
 * @example
 * const notes = await get<Note[]>('/notes/');
 */
export async function get<T>(endpoint: string, signal?: AbortSignal): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'GET', signal });
}

/**
 * POST request helper
 *
 * @example
 * const note = await post<Note>('/notes/', { title: 'Test', content: '...' });
 */
export async function post<T>(
  endpoint: string,
  body: unknown,
  signal?: AbortSignal
): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'POST', body, signal });
}

/**
 * PUT request helper
 *
 * @example
 * const note = await put<Note>('/notes/1', { title: 'Updated' });
 */
export async function put<T>(
  endpoint: string,
  body: unknown,
  signal?: AbortSignal
): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'PUT', body, signal });
}

/**
 * DELETE request helper
 *
 * @example
 * await del('/notes/1');
 */
export async function del<T>(endpoint: string, signal?: AbortSignal): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'DELETE', signal });
}
