/**
 * Create Note Form Component
 *
 * Form to create new notes with validation
 */

import { useState, FormEvent } from 'react';
import { useNotes } from '../../contexts/NotesContext';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

export function CreateNoteForm() {
  const { createNote } = useNotes();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Basic validation
    if (!title.trim() || !content.trim()) {
      setError('Both title and content are required');
      return;
    }

    if (title.length < 3) {
      setError('Title must be at least 3 characters');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await createNote({ title: title.trim(), content: content.trim() });
      setTitle('');
      setContent('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create note');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter note title"
        disabled={isSubmitting}
      />

      <div className="flex flex-col gap-1.5">
        <label className="text-sm font-medium text-gray-700">
          Content
        </label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Enter note content"
          disabled={isSubmitting}
          rows={4}
          className="px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
        />
      </div>

      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}

      <Button type="submit" variant="primary" loading={isSubmitting}>
        Add Note
      </Button>
    </form>
  );
}
