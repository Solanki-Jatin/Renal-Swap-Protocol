import { useState } from 'react'
import './ControlPanel.css'

/**
 * The backend generates a fresh pool per request rather than keeping
 * one running pool on the server, so "adding a pair" here means
 * generating a new pool of the requested size, not appending one
 * hand-picked pair to a list. This panel is what actually drives a
 * match: pick a pool size and a matcher, run it, watch the graph.
 */
export default function ControlPanel({ onRun, isLoading }) {
  const [count, setCount] = useState(30)
  const [seed, setSeed] = useState('')
  const [matcher, setMatcher] = useState('optimal')

  function handleSubmit(event) {
    event.preventDefault()
    onRun({
      count: Number(count),
      seed: seed === '' ? null : Number(seed),
      matcher,
    })
  }

  return (
    <form className="control-panel" onSubmit={handleSubmit}>
      <div className="control-field">
        <label htmlFor="pool-size">Pool size</label>
        <input
          id="pool-size"
          type="number"
          min="2"
          max="500"
          value={count}
          onChange={(e) => setCount(e.target.value)}
        />
      </div>

      <div className="control-field">
        <label htmlFor="seed">Seed (optional)</label>
        <input
          id="seed"
          type="number"
          placeholder="random"
          value={seed}
          onChange={(e) => setSeed(e.target.value)}
        />
      </div>

      <div className="control-field">
        <span className="control-field-label">Matcher</span>
        <div className="matcher-toggle">
          <button
            type="button"
            className={matcher === 'optimal' ? 'toggle-option active' : 'toggle-option'}
            onClick={() => setMatcher('optimal')}
          >
            Optimal
          </button>
          <button
            type="button"
            className={matcher === 'greedy' ? 'toggle-option active' : 'toggle-option'}
            onClick={() => setMatcher('greedy')}
          >
            Greedy
          </button>
        </div>
      </div>

      <button type="submit" className="run-button" disabled={isLoading}>
        {isLoading ? 'Matching…' : 'Run matching'}
      </button>
    </form>
  )
}
