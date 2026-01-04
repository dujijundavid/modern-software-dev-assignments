/**
 * Action Items Context - Manages action items state and operations
 *
 * SIMILAR PATTERN to NotesContext, but includes:
 * - Optimistic completion (Task 3)
 * - Rollback on error
 */

import { createContext, useContext, useCallback, useState, ReactNode } from 'react';
import { fetchActionItems, createActionItem, completeActionItem } from '../services/actionItems';
import type { ActionItem, ActionItemCreateInput } from '../types/actionItems';

/**
 * Context state shape
 */
interface ActionItemsState {
  actionItems: ActionItem[];
  loading: boolean;
  error: string | null;
}

/**
 * Context actions shape
 */
interface ActionItemsActions {
  loadActionItems: () => Promise<void>;
  createActionItem: (input: ActionItemCreateInput) => Promise<void>;
  completeActionItem: (id: number) => Promise<void>;
  refresh: () => Promise<void>;
}

/**
 * Combined context value
 */
type ActionItemsContextValue = ActionItemsState & ActionItemsActions;

/**
 * Create the context
 */
const ActionItemsContext = createContext<ActionItemsContextValue | undefined>(undefined);

/**
 * Custom hook to use action items context
 *
 * @example
 * function MyComponent() {
 *   const { actionItems, loading, completeActionItem } = useActionItems();
 *   ...
 * }
 */
export function useActionItems(): ActionItemsContextValue {
  const context = useContext(ActionItemsContext);
  if (!context) {
    throw new Error('useActionItems must be used within an ActionItemsProvider');
  }
  return context;
}

/**
 * Provider component props
 */
interface ActionItemsProviderProps {
  children: ReactNode;
}

/**
 * Action Items Provider Component
 *
 * WHAT IT DOES:
 * - Manages action items state (list, loading, errors)
 * - Provides CRUD operations
 * - Optimistic completion with rollback
 *
 * @example
 * <ActionItemsProvider>
 *   <App />
 * </ActionItemsProvider>
 */
export function ActionItemsProvider({ children }: ActionItemsProviderProps) {
  const [state, setState] = useState<ActionItemsState>({
    actionItems: [],
    loading: true,
    error: null,
  });

  /**
   * Load all action items
   */
  const loadActionItems = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const items = await fetchActionItems();
      setState((prev) => ({ ...prev, actionItems: items, loading: false }));
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to load action items';
      setState((prev) => ({ ...prev, error: message, loading: false }));
    }
  }, []);

  /**
   * Create a new action item
   */
  const createActionItemHandler = useCallback(async (input: ActionItemCreateInput) => {
    // Optimistic update
    const tempItem: ActionItem = {
      id: Date.now(),
      description: input.description,
      completed: false,
    };

    setState((prev) => ({
      ...prev,
      actionItems: [...prev.actionItems, tempItem],
    }));

    try {
      const createdItem = await createActionItem(input);

      // Replace temporary item with real one
      setState((prev) => ({
        ...prev,
        actionItems: prev.actionItems.map((item) =>
          item.id === tempItem.id ? createdItem : item
        ),
      }));
    } catch (error) {
      // Rollback
      setState((prev) => ({
        ...prev,
        actionItems: prev.actionItems.filter((item) => item.id !== tempItem.id),
        error: error instanceof Error ? error.message : 'Failed to create action item',
      }));
      throw error;
    }
  }, []);

  /**
   * Complete an action item
   *
   * OPTIMISTIC UPDATE:
   * 1. Mark as completed in UI immediately
   * 2. Call API
   * 3. Rollback on error
   */
  const completeActionItemHandler = useCallback(async (id: number) => {
    // Store original state for rollback
    const originalItem = state.actionItems.find((item) => item.id === id);
    if (!originalItem) return;

    // Optimistic update
    setState((prev) => ({
      ...prev,
      actionItems: prev.actionItems.map((item) =>
        item.id === id ? { ...item, completed: true } : item
      ),
    }));

    try {
      await completeActionItem(id);
      // Success: keep the optimistic update
    } catch (error) {
      // Rollback
      setState((prev) => ({
        ...prev,
        actionItems: prev.actionItems.map((item) =>
          item.id === id ? originalItem : item
        ),
        error: error instanceof Error ? error.message : 'Failed to complete action item',
      }));
      throw error;
    }
  }, [state.actionItems]);

  /**
   * Refresh action items
   */
  const refresh = useCallback(async () => {
    await loadActionItems();
  }, [loadActionItems]);

  const value: ActionItemsContextValue = {
    ...state,
    loadActionItems,
    createActionItem: createActionItemHandler,
    completeActionItem: completeActionItemHandler,
    refresh,
  };

  return <ActionItemsContext.Provider value={value}>{children}</ActionItemsContext.Provider>;
}
