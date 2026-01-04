/**
 * Notes Context - Manages notes state and operations
 *
 * WHY CONTEXT:
 * - Avoids prop drilling through component tree
 * - Centralized state management for notes
 * - Easy to test (mock context in tests)
 * - No external dependencies (unlike Redux)
 *
 * ARCHITECTURE:
 * - State: notes list, loading, error, search query
 * - Actions: load, create, search, clear search, refresh
 * - Optimistic updates: Instant UI feedback with rollback on error
 */

import { createContext, useContext, useCallback, useState, ReactNode } from 'react';
import { fetchNotes, createNote, searchNotes } from '../services/notes';
import type { Note, NoteCreateInput } from '../types/notes';

/**
 * Context state shape
 */
interface NotesState {
  notes: Note[];
  loading: boolean;
  error: string | null;
  searchQuery: string;
}

/**
 * Context actions shape
 */
interface NotesActions {
  loadNotes: () => Promise<void>;
  createNote: (input: NoteCreateInput) => Promise<void>;
  searchNotes: (query: string) => Promise<void>;
  clearSearch: () => void;
  refresh: () => Promise<void>;
}

/**
 * Combined context value
 */
type NotesContextValue = NotesState & NotesActions;

/**
 * Create the context with undefined default (enforces using provider)
 */
const NotesContext = createContext<NotesContextValue | undefined>(undefined);

/**
 * Custom hook to use notes context
 * Throws if used outside provider (catches bugs early)
 *
 * @example
 * function MyComponent() {
 *   const { notes, loading, createNote } = useNotes();
 *   ...
 * }
 */
export function useNotes(): NotesContextValue {
  const context = useContext(NotesContext);
  if (!context) {
    throw new Error('useNotes must be used within a NotesProvider');
  }
  return context;
}

/**
 * Provider component props
 */
interface NotesProviderProps {
  children: ReactNode;
}

/**
 * Notes Provider Component
 *
 * WHAT IT DOES:
 * - Manages notes state (list, loading, errors)
 * - Provides CRUD operations
 * - Handles search functionality
 * - Optimizes re-renders with useCallback
 *
 * @example
 * <NotesProvider>
 *   <App />
 * </NotesProvider>
 */
export function NotesProvider({ children }: NotesProviderProps) {
  const [state, setState] = useState<NotesState>({
    notes: [],
    loading: true,
    error: null,
    searchQuery: '',
  });

  /**
   * Load all notes
   *
   * OPTIMIZATION: useCallback prevents unnecessary re-renders
   * of child components that receive this function
   */
  const loadNotes = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const notes = await fetchNotes();
      setState((prev) => ({ ...prev, notes, loading: false }));
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to load notes';
      setState((prev) => ({ ...prev, error: message, loading: false }));
    }
  }, []);

  /**
   * Create a new note
   *
   * OPTIMISTIC UPDATE PATTERN (Task 3):
   * 1. Add note to local state immediately (UI updates instantly)
   * 2. Call API
   * 3. Rollback on error
   *
   * WHY: Better UX - user sees immediate feedback
   */
  const createNoteHandler = useCallback(async (input: NoteCreateInput) => {
    // Optimistic update: assume success
    const tempNote: Note = {
      id: Date.now(), // Temporary ID
      title: input.title,
      content: input.content,
    };

    setState((prev) => ({
      ...prev,
      notes: [...prev.notes, tempNote],
    }));

    try {
      const createdNote = await createNote(input);

      // Replace temporary note with real one
      setState((prev) => ({
        ...prev,
        notes: prev.notes.map((n) => (n.id === tempNote.id ? createdNote : n)),
      }));
    } catch (error) {
      // Rollback: remove temporary note
      setState((prev) => ({
        ...prev,
        notes: prev.notes.filter((n) => n.id !== tempNote.id),
        error: error instanceof Error ? error.message : 'Failed to create note',
      }));
      throw error; // Re-throw so caller can handle
    }
  }, []);

  /**
   * Search notes
   */
  const searchNotesHandler = useCallback(async (query: string) => {
    setState((prev) => ({ ...prev, loading: true, searchQuery: query, error: null }));

    try {
      const notes = await searchNotes(query);
      setState((prev) => ({ ...prev, notes, loading: false }));
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Search failed';
      setState((prev) => ({ ...prev, error: message, loading: false }));
    }
  }, []);

  /**
   * Clear search and reload all notes
   */
  const clearSearch = useCallback(() => {
    setState((prev) => ({ ...prev, searchQuery: '' }));
    loadNotes();
  }, [loadNotes]);

  /**
   * Refresh notes (alias for loadNotes)
   */
  const refresh = useCallback(async () => {
    await loadNotes();
  }, [loadNotes]);

  const value: NotesContextValue = {
    ...state,
    loadNotes,
    createNote: createNoteHandler,
    searchNotes: searchNotesHandler,
    clearSearch,
    refresh,
  };

  return <NotesContext.Provider value={value}>{children}</NotesContext.Provider>;
}
