/**
 * Utility function to merge Tailwind CSS classes
 *
 * WHY: Prevents class conflicts when combining multiple class sources
 *
 * @example
 * cn('px-4 py-2', 'bg-blue-500') // => 'px-4 py-2 bg-blue-500'
 * cn('px-4', isActive && 'bg-blue-500', 'py-2') // => 'px-4 bg-blue-500 py-2'
 *
 * Note: For production, you might want to install 'clsx' and 'tailwind-merge':
 * npm install clsx tailwind-merge
 *
 * Then replace with:
 * import { clsx } from 'clsx';
 * import { twMerge } from 'tailwind-merge';
 *
 * export function cn(...inputs: ClassValue[]) {
 *   return twMerge(clsx(inputs));
 * }
 */

/**
 * Simple version for now
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
