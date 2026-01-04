/**
 * Notes API service
 *
 * Provides typed methods for all Notes-related API operations
 */

import { get, post } from './api';
import type { Note, NoteCreateInput, NotesListResponse } from '../types/notes';

/**
 * Fetch all notes
 * GET /notes/
 *
 * @example
 * const notes = await fetchNotes();
 */
export async function fetchNotes(signal?: AbortSignal): Promise<NotesListResponse> {
  return get<NotesListResponse>('/notes/', signal);
}

/**
 * Fetch a single note
 * GET /notes/{id}
 *
 * @example
 * const note = await fetchNote(1);
 */
export async function fetchNote(id: number, signal?: AbortSignal): Promise<Note> {
  return get<Note>(`/notes/${id}`, signal);
}

/**
 * Search notes (optional query param)
 * GET /notes/search?q=query
 *
 * @example
 * const results = await searchNotes('python');
 * const all = await searchNotes(); // No query
 */
export async function searchNotes(
  query?: string,
  signal?: AbortSignal
): Promise<NotesListResponse> {
  const url = query ? `/notes/search/?q=${encodeURIComponent(query)}` : '/notes/search/';
  return get<NotesListResponse>(url, signal);
}

/**
 * Create a new note
 * POST /notes/
 *
 * @example
 * const newNote = await createNote({
 *   title: 'My Note',
 *   content: 'Content here'
 * });
 */
export async function createNote(
  input: NoteCreateInput,
  signal?: AbortSignal
): Promise<Note> {
  return post<Note>('/notes/', input, signal);
}

// Future: Update and delete for full CRUD (Task 3)
// export async function updateNote(id: number, input: NoteUpdateInput): Promise<Note>;
// export async function deleteNote(id: number): Promise<void>;
