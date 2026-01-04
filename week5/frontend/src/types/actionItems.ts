/**
 * Action Item types matching backend Pydantic schemas
 * @see backend/app/schemas.py
 */

/**
 * Input for creating a new action item
 * Matches: ActionItemCreate(BaseModel) in backend
 *
 * @example
 * const input: ActionItemCreateInput = {
 *   description: "Complete the assignment"
 * };
 */
export interface ActionItemCreateInput {
  description: string;
}

/**
 * Action item as returned from the API
 * Matches: ActionItemRead(BaseModel) in backend
 *
 * @example
 * const item: ActionItem = {
 *   id: 1,
 *   description: "Complete the assignment",
 *   completed: false
 * };
 */
export interface ActionItem {
  id: number;
  description: string;
  completed: boolean;
}

/**
 * Bulk complete input (for Task 4)
 */
export interface BulkCompleteInput {
  ids: number[];
}

/**
 * Bulk complete response (for Task 4)
 */
export interface BulkCompleteResponse {
  updated: ActionItem[];
  failed: Array<{ id: number; error: string }>;
}
