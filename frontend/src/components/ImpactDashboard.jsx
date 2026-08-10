import './ImpactDashboard.css'

/**
 * The numbers that make the abstract graph mean something: how many
 * of these patients would have had zero path to a transplant through
 * their own donor, and how many actually got matched this round.
 */
export default function ImpactDashboard({ result }) {
  if (!result) {
    return (
      <div className="dashboard-empty">
        <p>Run a match to see the impact.</p>
      </div>
    )
  }

  const { total_pairs, matched_pairs, unmatched_pairs } = result.impact_summary
  const percentMatched = total_pairs > 0 ? Math.round((matched_pairs / total_pairs) * 100) : 0

  return (
    <div className="dashboard">
      <div className="dashboard-headline">
        <span className="headline-number">{percentMatched}%</span>
        <span className="headline-label">of this pool matched into a swap</span>
      </div>

      <div className="dashboard-comparison">
        <div className="comparison-row">
          <span className="comparison-label">Without this system</span>
          <span className="comparison-value zero">0 patients</span>
        </div>
        <div className="comparison-row">
          <span className="comparison-label">With {result.matcher === 'optimal' ? 'the optimal matcher' : 'the greedy matcher'}</span>
          <span className="comparison-value">{matched_pairs} patients</span>
        </div>
      </div>

      <div className="dashboard-stats">
        <Stat label="Total pairs" value={total_pairs} />
        <Stat label="Matched" value={matched_pairs} accent />
        <Stat label="Unmatched" value={unmatched_pairs} />
        <Stat label="Cycles used" value={result.matched_cycles.length} />
        <Stat label="Runtime" value={`${result.runtime_ms} ms`} />
        {result.solver_status && <Stat label="Solver status" value={result.solver_status} />}
      </div>
    </div>
  )
}

function Stat({ label, value, accent }) {
  return (
    <div className="stat">
      <span className={accent ? 'stat-value accent' : 'stat-value'}>{value}</span>
      <span className="stat-label">{label}</span>
    </div>
  )
}
