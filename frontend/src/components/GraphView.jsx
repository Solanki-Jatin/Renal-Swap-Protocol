import { useMemo } from 'react'
import './GraphView.css'

const VIEWBOX_SIZE = 640
const CENTER = VIEWBOX_SIZE / 2
const MAX_BACKGROUND_EDGES = 260

/**
 * Renders the compatibility pool as a ring: every pair sits on a
 * circle, since a matched cycle IS a circle, this layout makes the
 * shape of a swap visually literal rather than abstract. Unmatched
 * connections are drawn faint in the background, matched cycles are
 * drawn bright, thick, and animated, so the eye goes straight to them.
 */
export default function GraphView({ nodes, edges, matchedCycles }) {
  const layout = useMemo(() => computeLayout(nodes, edges, matchedCycles), [nodes, edges, matchedCycles])

  if (!nodes || nodes.length === 0) {
    return (
      <div className="graph-empty">
        <p>No pairs to show yet. Run a match to see the pool.</p>
      </div>
    )
  }

  return (
    <div className="graph-view">
      <svg viewBox={`0 0 ${VIEWBOX_SIZE} ${VIEWBOX_SIZE}`} className="graph-svg" role="img" aria-label="Compatibility graph">
        <defs>
          <filter id="matchGlow" x="-60%" y="-60%" width="220%" height="220%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <circle cx={CENTER} cy={CENTER} r={layout.radius} className="ring-guide" />

        {layout.backgroundEdges.map((edge, i) => (
          <line
            key={`bg-${i}`}
            x1={edge.x1}
            y1={edge.y1}
            x2={edge.x2}
            y2={edge.y2}
            className="edge-background"
          />
        ))}

        {layout.matchedEdges.map((edge, i) => (
          <line
            key={`match-${i}`}
            x1={edge.x1}
            y1={edge.y1}
            x2={edge.x2}
            y2={edge.y2}
            className="edge-matched"
            filter="url(#matchGlow)"
          />
        ))}

        {layout.points.map((point) => (
          <g key={point.id} className={point.matched ? 'node matched' : 'node'}>
            <circle cx={point.x} cy={point.y} r={layout.nodeRadius} className="node-circle" filter={point.matched ? 'url(#matchGlow)' : undefined} />
            {layout.nodeRadius >= 12 && (
              <text x={point.x} y={point.y} className="node-label" dy="0.32em">
                {point.label}
              </text>
            )}
            <title>{`${point.id}: patient ${point.patientType}, donor ${point.donorType}`}</title>
          </g>
        ))}
      </svg>

      <div className="graph-legend">
        <span className="legend-item">
          <span className="legend-swatch matched" /> Matched into a swap
        </span>
        <span className="legend-item">
          <span className="legend-swatch unmatched" /> Not matched this round
        </span>
      </div>
    </div>
  )
}

function computeLayout(nodes, edges, matchedCycles) {
  const radius = VIEWBOX_SIZE * 0.36
  const nodeCount = nodes.length
  const nodeRadius = clamp(18 - nodeCount / 15, 5, 16)

  const positionById = new Map()
  const points = nodes.map((node, index) => {
    const angle = (index / nodeCount) * Math.PI * 2 - Math.PI / 2
    const x = CENTER + radius * Math.cos(angle)
    const y = CENTER + radius * Math.sin(angle)
    positionById.set(node.id, { x, y })
    return {
      id: node.id,
      x,
      y,
      patientType: node.patient_blood_type,
      donorType: node.donor_blood_type,
      label: `${node.patient_blood_type}`,
      matched: false,
    }
  })

  const matchedPairIds = new Set()
  const matchedEdgeKeys = new Set()
  const matchedEdges = []

  for (const cycle of matchedCycles || []) {
    for (let i = 0; i < cycle.length; i++) {
      const fromId = cycle[i]
      const toId = cycle[(i + 1) % cycle.length]
      matchedPairIds.add(fromId)
      const from = positionById.get(fromId)
      const to = positionById.get(toId)
      if (!from || !to) continue
      matchedEdgeKeys.add(`${fromId}->${toId}`)
      matchedEdges.push({ x1: from.x, y1: from.y, x2: to.x, y2: to.y })
    }
  }

  for (const point of points) {
    if (matchedPairIds.has(point.id)) point.matched = true
  }

  let backgroundCandidates = (edges || []).filter((edge) => !matchedEdgeKeys.has(`${edge.from}->${edge.to}`))
  const step = Math.max(1, Math.ceil(backgroundCandidates.length / MAX_BACKGROUND_EDGES))
  const backgroundEdges = []
  for (let i = 0; i < backgroundCandidates.length; i += step) {
    const edge = backgroundCandidates[i]
    const from = positionById.get(edge.from)
    const to = positionById.get(edge.to)
    if (!from || !to) continue
    backgroundEdges.push({ x1: from.x, y1: from.y, x2: to.x, y2: to.y })
  }

  return { points, matchedEdges, backgroundEdges, radius, nodeRadius }
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value))
}
