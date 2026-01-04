/**
 * Notes List Component
 *
 * Displays notes with loading and error states
 */

import { useEffect } from 'react';
import { useNotes } from '../../contexts/NotesContext';
import { Card } from '../ui/Card';
import type { Note } from '../../types/notes';

export function NotesList() {
  const { notes, loading, error, loadNotes } = useNotes();

  useEffect(() => {
    loadNotes();
  }, []);

  if (loading) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading notes...</span>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-6">
        <div className="text-center py-8">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => loadNotes()}
            className="text-blue-600 hover:underline"
          >
            Retry
          </button>
        </div>
      </Card>
    );
  }

  if (notes.length === 0) {
    return (
      <Card className="p-6">
        <div className="text-center py-8 text-gray-500">
          <p className="text-lg mb-2">No notes yet</p>
          <p className="text-sm">Create your first note to get started!</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {notes.map((note: Note) => (
        <Card key={note.id} className="p-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{note.title}</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{note.content}</p>
        </Card>
      ))}
    </div>
  );
}
