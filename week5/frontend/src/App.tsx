/**
 * App Component
 *
 * Root component that composes the entire application
 *
 * ARCHITECTURE:
 * - Providers at top level (context injection)
 * - Layout components (Main)
 * - Feature sections (Notes, Action Items)
 */

import { NotesProvider } from './contexts/NotesContext';
import { ActionItemsProvider } from './contexts/ActionItemsContext';
import { NotesList, CreateNoteForm } from './components/notes';
import { ActionItemsList, CreateActionItemForm } from './components/action-items';

/**
 * App Content Component
 *
 * Separated to enable providers wrapper
 */
function AppContent() {
  return (
    <div className="min-h-screen bg-background">
      <main className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Page header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Modern Software Dev Starter
          </h1>
          <p className="text-lg text-gray-600">
            Week 5: Agentic Development with Warp
          </p>
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800">
              ✅ 阶段 2 完成！类型安全 + API 层 + 状态管理
            </p>
            <p className="text-xs text-green-600 mt-2">
              TypeScript 类型定义完整，API 客户端就绪，React Context 状态管理运行中
            </p>
          </div>
        </div>

        {/* Notes Section */}
        <section className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            Notes
          </h2>
          <div className="space-y-6">
            <CreateNoteForm />
            <NotesList />
          </div>
        </section>

        {/* Action Items Section */}
        <section className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            Action Items
          </h2>
          <div className="space-y-6">
            <CreateActionItemForm />
            <ActionItemsList />
          </div>
        </section>
      </main>
    </div>
  );
}

/**
 * App Component
 *
 * Wraps content with context providers
 */
function App() {
  return (
    <NotesProvider>
      <ActionItemsProvider>
        <AppContent />
      </ActionItemsProvider>
    </NotesProvider>
  );
}

export default App;
