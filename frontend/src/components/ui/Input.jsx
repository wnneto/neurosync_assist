// src/components/ui/Input.jsx
import React from 'react';

const Input = ({ className = '', ...props }) => {
  return (
    <input
      className={`border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 ${className}`}
      {...props}
    />
  );
};

export default Input;