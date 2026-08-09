import { useState } from 'react'
import GraphView from './components/GraphView.jsx'
import ImpactDashboard from './components/ImpactDashboard.jsx'
import ControlPanel from './components/ControlPanel.jsx'
import BenchmarkChart from './components/BenchmarkChart.jsx'
import { matchOptimal, matchGreedy } from './api/client.js'
import './App.css'

export default function App() {
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleRun({ count, seed, matcher }) {
    setIsLoading(true)
    setError(null)
    try {
      const run = matcher === 'optimal' ? matchOptimal : matchGreedy
      const data = await run({ count, seed })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>Renal Swap Exchange</h1>
          <p className="app-tagline">No donor is a dead end.</p>
        </div>
        <span className="no-ai-badge">Real graph algorithms &amp; integer programming — zero AI calls</span>
      </header>

      <main className="app-main">
        <section className="panel panel-graph">
          <GraphView
            nodes={result?.nodes ?? []}
            edges={result?.edges ?? []}
            matchedCycles={result?.matched_cycles ?? []}
          />
        </section>

        <aside className="app-sidebar">
          <section className="panel">
            <ControlPanel onRun={handleRun} isLoading={isLoading} />
            {error && <p className="app-error">{error}</p>}
          </section>

          <section className="panel">
            <ImpactDashboard result={result} />
          </section>
        </aside>
      </main>

      <section className="panel panel-benchmark">
        <BenchmarkChart />
      </section>
    </div>
  )
}
