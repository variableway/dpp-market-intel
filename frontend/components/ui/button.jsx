import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-full text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary px-4 py-2 text-primary-foreground hover:opacity-90",
        secondary: "bg-secondary px-4 py-2 text-secondary-foreground hover:bg-secondary/90",
        ghost: "px-3 py-2 text-foreground hover:bg-white/60"
      }
    },
    defaultVariants: {
      variant: "default"
    }
  }
);

export function Button({ className, variant, ...props }) {
  return <button className={cn(buttonVariants({ variant }), className)} {...props} />;
}
