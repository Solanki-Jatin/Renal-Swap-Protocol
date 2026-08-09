/**
 * Every call to the backend lives in this one file. If the API's
 * address or shape ever changes, this is the only file that should
 * need to change, every component below imports from here rather
 * than calling fetch directly.
 */

const API_BASE_URL = 'http://localhost:8000'

async function postJSON(path, body) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    const detail = await response.text()
    throw new Error(`${path} failed (${response.status}): ${detail}`)
  }
  return response.json()
}

async function getJSON(path) {
  const response = await fetch(`${API_BASE_URL}${path}`)
  if (!response.ok) {
    const detail = await response.text()
    throw new Error(`${path} failed (${response.status}): ${detail}`)
  }
  return response.json()
}

/**
 * Generates a synthetic pool of incompatible patient-donor pairs.
 * Rarely needed directly, since matchOptimal / matchGreedy already
 * generate their own pool internally, kept here for completeness
 * against the documented API surface.
 */
export function generateDataset({ count = 30, hospitalIds = null, seed = null } = {}) {
  return postJSON('/dataset/generate', { count, hospital_ids: hospitalIds, seed })
}

/** Builds the compatibility graph for a freshly generated pool, without running a matcher. */
export function buildGraph({ count = 30, hospitalIds = null, seed = null } = {}) {
  return postJSON('/graph/build', { count, hospital_ids: hospitalIds, seed })
}

/** Generates a pool and solves it with the optimal ILP matcher. */
export function matchOptimal({ count = 30, hospitalIds = null, seed = null } = {}) {
  return postJSON('/match/optimal', { count, hospital_ids: hospitalIds, seed })
}

/** Generates a pool and solves it with the fast greedy baseline matcher. */
export function matchGreedy({ count = 30, hospitalIds = null, seed = null } = {}) {
  return postJSON('/match/greedy', { count, hospital_ids: hospitalIds, seed })
}

/** Runs the optimal vs greedy benchmark. Pass poolSizes as an array of numbers, e.g. [50, 100, 200]. */
export function getBenchmark(poolSizes = null) {
  const query = poolSizes ? `?pool_sizes=${poolSizes.join(',')}` : ''
  return getJSON(`/benchmark${query}`)
}
