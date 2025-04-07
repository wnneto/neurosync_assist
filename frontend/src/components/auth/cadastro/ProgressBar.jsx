import React from 'react';

export default function ProgressBar({ step }) {
  return (
    <div className="progress-bar">
      {[1, 2, 3].map((num) => (
        <React.Fragment key={num}>
          <div className={`progress-step ${step >= num ? 'active' : ''}`}>{num}</div>
          {num < 3 && <div className={`progress-line ${step > num ? 'active' : ''}`} />}
        </React.Fragment>
      ))}
    </div>
  );
}
