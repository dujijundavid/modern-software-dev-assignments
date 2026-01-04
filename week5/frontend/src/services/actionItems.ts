/**
 * Action Items API service
 *
 * Provides typed methods for all Action Item-related API operations
 */

import { get, post, put } from './api';
import type {
  ActionItem,
  ActionItemCreateInput,
} from '../types/actionItems';

// Future: Bulk operations for Task 4
// import type {
//   BulkCompleteInput,
//   BulkCompleteResponse,
// } from '../types/actionItems';

/**
 * Fetch all action items
 * GET /action-items/
 *
 * @example
 * const items = await fetchActionItems();
 */
export async function fetchActionItems(signal?: AbortSignal): Promise<ActionItem[]> {
  return get<ActionItem[]>('/action-items/', signal);
}

/**
 * Create a new action item
 * POST /action-items/
 *
 * @example
 * const newItem = await createActionItem({
 *   description: 'Complete assignment'
 * });
 */
export async function createActionItem(
  input: ActionItemCreateInput,
  signal?: AbortSignal
): Promise<ActionItem> {
  return post<ActionItem>('/action-items/', input, signal);
}

/**
 * Mark an action item as completed
 * PUT /action-items/{id}/complete
 *
 * @example
 * const completed = await completeActionItem(1);
 */
export async function completeActionItem(
  id: number,
  signal?: AbortSignal
): Promise<ActionItem> {
  return put<ActionItem>(`/action-items/${id}/complete`, {}, signal);
}

// Future: Bulk operations for Task 4
// export async function bulkCompleteActionItems(
//   input: BulkCompleteInput
// ): Promise<BulkCompleteResponse>;
