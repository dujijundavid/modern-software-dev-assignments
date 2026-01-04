/**
 * Create Action Item Form Component
 *
 * Form to create new action items
 */

import { useState, FormEvent } from 'react';
import { useActionItems } from '../../contexts/ActionItemsContext';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

export function CreateActionItemForm() {
  const { createActionItem } = useActionItems();
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Basic validation
    if (!description.trim()) {
      setError('Description is required');
      return;
    }

    if (description.length < 3) {
      setError('Description must be at least 3 characters');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await createActionItem({ description: description.trim() });
      setDescription('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create action item');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Description"
        value={description}
        onChange={(e) => {
          setDescription(e.target.value);
          setError(null);
        }}
        placeholder="Enter action item description"
        disabled={isSubmitting}
      />

      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}

      <Button type="submit" variant="primary" loading={isSubmitting}>
        Add Action Item
      </Button>
    </form>
  );
}
