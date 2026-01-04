/**
 * Note types matching backend Pydantic schemas
 * @see backend/app/schemas.py
 */

/**
 * Input for creating a new note
 * Matches: NoteCreate(BaseModel) in backend
 *
 * @example
 * const input: NoteCreateInput = {
 *   title: "My First Note",
 *   content: "This is the content"
 * };
 */
export interface NoteCreateInput {
  title: string;
  content: string;
}

/**
 * Note as returned from the API
 * Matches: NoteRead(BaseModel) in backend
 *
 * @example
 * const note: Note = {
 *   id: 1,
 *   title: "My First Note",
 *   content: "This is the content"
 * };
 */
export interface Note {
  id: number;
  title: string;
  content: string;
}

/**
 * API response envelope (Task 7 pattern)
 * Can be enabled later for consistent error handling
 */
export interface NoteResponse {
  data: Note;
  ok: true;
}

/**
 * Notes list response
 */
export type NotesListResponse = Note[];

/**
 * Enveloped list response (optional)
 */
export interface NotesListResponseEnvelope {
  data: NotesListResponse;
  total: number;
  ok: true;
}
