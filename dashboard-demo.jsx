import React from "react";

/**
 * Archived reference component.
 *
 * This repository uses `dashboard-demo.html` as the primary dashboard demo.
 * The JSX dashboard is intentionally reduced to an archive notice so reviewers
 * do not mistake it for an active, wired frontend.
 */
export default function DashboardArchivedReference() {
  return (
    <main style={{ fontFamily: "Segoe UI, -apple-system, sans-serif", padding: 24 }}>
      <h1 style={{ marginBottom: 12 }}>Archived Dashboard Reference</h1>
      <p style={{ marginBottom: 8 }}>
        The active frontend demo for this project is <code>dashboard-demo.html</code>.
      </p>
      <p style={{ marginBottom: 8 }}>
        This JSX file is preserved only as an archive placeholder and is not part of
        the runnable demo flow in this repository.
      </p>
      <p>
        Backend grading and report generation are implemented in the Python files under
        <code> prototype/</code>.
      </p>
    </main>
  );
}
