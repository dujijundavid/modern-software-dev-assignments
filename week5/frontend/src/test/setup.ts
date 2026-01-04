/**
 * Vitest Setup File
 *
 * Configures test environment with:
 * - React Testing Library
 * - JSDOM matchers
 * - Global test utilities
 */

import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

/**
 * Extend Vitest's expect with React Testing Library matchers
 */
expect.extend(matchers);

/**
 * Cleanup after each test
 * - Unmounts React trees
 * - Resets DOM
 */
afterEach(() => {
  cleanup();
});

/**
 * Mock IntersectionObserver
 * (used by many component libraries)
 */
globalThis.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
})) as any;

/**
 * Mock window.matchMedia
 * (used for responsive design tests)
 */
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});
