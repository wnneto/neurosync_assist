import React from "react";

export function Button({
  children,
  onClick,
  variant = "default",
  className = "",
  disabled = false,
  type = "button",
}) {
  const base = "px-4 py-2 rounded text-white font-semibold transition";
  const variants = {
    default: "bg-blue-600 hover:bg-blue-700",
    outline: "border border-gray-300 text-gray-700 bg-white hover:bg-gray-100",
    destructive: "bg-red-600 hover:bg-red-700",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
