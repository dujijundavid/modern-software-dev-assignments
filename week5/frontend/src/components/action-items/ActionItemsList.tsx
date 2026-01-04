/**
 * Action Items List Component
 *
 * Displays action items with complete button
 */

import { useEffect } from 'react';
import { useActionItems } from '../../contexts/ActionItemsContext';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import type { ActionItem } from '../../types/actionItems';

export function ActionItemsList() {
  const { actionItems, loading, error, loadActionItems, completeActionItem } = useActionItems();

  useEffect(() => {
    loadActionItems();
  }, []);

  if (loading) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading action items...</span>
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
            onClick={() => loadActionItems()}
            className="text-blue-600 hover:underline"
          >
            Retry
          </button>
        </div>
      </Card>
    );
  }

  if (actionItems.length === 0) {
    return (
      <Card className="p-6">
        <div className="text-center py-8 text-gray-500">
          <p className="text-lg mb-2">No action items yet</p>
          <p className="text-sm">Create your first action item to get started!</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {actionItems.map((item: ActionItem) => (
        <Card key={item.id} className={`p-4 ${item.completed ? 'opacity-60' : ''}`}>
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3 flex-1">
              {/* Completion indicator */}
              <div className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                item.completed ? 'bg-green-500 border-green-500' : 'border-gray-300'
              }`}>
                {item.completed && (
                  <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>

              {/* Text with strikethrough if completed */}
              <span className={`${item.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {item.description}
              </span>
            </div>

            {/* Complete button (only if pending) */}
            {!item.completed && (
              <Button
                size="sm"
                variant="primary"
                onClick={() => completeActionItem(item.id)}
              >
                Complete
              </Button>
            )}
          </div>
        </Card>
      ))}
    </div>
  );
}
