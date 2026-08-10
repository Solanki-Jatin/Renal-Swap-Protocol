import { useState } from 'react'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from 'recharts'
import { getBenchmark } from '../api/client'
import './BenchmarkChart.css'

/**
 * Runs the optimal-vs-greedy benchmark and charts it. This is what
 * turns "the optimal solver is better" from a claim into a picture,
 * matched patients per pool size, optimal next to greedy.
 */
export default function BenchmarkChart() {
  const [results, setResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  async function runBenchmark() {
    setIsLoading(true)
    setError(null)
    try {
      const data = await getBenchmark()
      setResults(data.results)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="benchmark-panel">
      <div className="benchmark-header">
        <div>
          <h3>Optimal vs greedy</h3>
          <p className="benchmark-subtitle">Same pools, two matchers, real numbers.</p>
        </div>
        <button className="benchmark-run" onClick={runBenchmark} disabled={isLoading}>
          {isLoading ? 'Running… (~20s)' : 'Run benchmark'}
        </button>
      </div>

      {error && <p className="benchmark-error">{error}</p>}

      {results && (
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={results} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
            <CartesianGrid stroke="#223052" strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="pool_size"
              tick={{ fill: '#8592ac', fontFamily: 'IBM Plex Mono', fontSize: 11 }}
              tickFormatter={(v) => `${v}`}
              label={{ value: 'Pool size', position: 'insideBottom', offset: -2, fill: '#8592ac', fontSize: 11 }}
            />
            <YAxis tick={{ fill: '#8592ac', fontFamily: 'IBM Plex Mono', fontSize: 11 }} />
            <Tooltip
              contentStyle={{ background: '#121a2c', border: '1px solid #223052', borderRadius: 8 }}
              labelStyle={{ color: '#e7ecf5', fontFamily: 'IBM Plex Mono' }}
              itemStyle={{ fontFamily: 'IBM Plex Mono', fontSize: 12 }}
            />
            <Legend wrapperStyle={{ fontFamily: 'IBM Plex Sans', fontSize: 12, color: '#8592ac' }} />
            <Bar dataKey="optimal_matched" name="Optimal matched" fill="#f2a93b" radius={[4, 4, 0, 0]} />
            <Bar dataKey="greedy_matched" name="Greedy matched" fill="#34d3c6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}

      {!results && !isLoading && !error && (
        <p className="benchmark-hint">Runs both matchers across several pool sizes, takes about 20 seconds.</p>
      )}
    </div>
  )
}
