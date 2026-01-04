/**
 * Card Component
 *
 * Simple container component
 */

import { HTMLAttributes, forwardRef } from 'react';
import { cn } from '../../utils/cn';

export const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('bg-white rounded-lg border border-gray-200 shadow-sm', className)}
      {...props}
    />
  )
);

Card.displayName = 'Card';
