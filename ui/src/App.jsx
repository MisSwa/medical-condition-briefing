import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000/brief'

function sourceToLink(source) {
  if (source.startsWith('pmid:')) {
    const id = source.replace('pmid:', '')
    return { href: `https://pubmed.ncbi.nlm.nih.gov/${id}/`, label: source }
  }
  if (source.startsWith('nct:')) {
    const id = source.replace('nct:', '')
    return { href: `https://clinicaltrials.gov/study/${id}`, label: source }
  }
  return { href: null, label: source }
}

export default function App() {
  const [condition, setCondition] = useState('')
  const [loading, setLoading] = useState(false)
  const [brief, setBrief] = useState(null)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setBrief(null)

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ condition: condition.trim() }),
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Request failed (${res.status})`)
      }

      setBrief(await res.json())
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Medical Condition Briefing</h1>
        <p>Enter a medical condition to generate a structured brief from live data sources.</p>
      </header>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={condition}
          onChange={(e) => setCondition(e.target.value)}
          placeholder="e.g. asthma, type 2 diabetes, breast cancer"
          disabled={loading}
          aria-label="Medical condition"
        />
        <button type="submit" disabled={loading || !condition.trim()}>
          {loading ? 'Generating…' : 'Generate Brief'}
        </button>
      </form>

      {loading && <div className="spinner" aria-label="Loading" role="status" />}

      {error && <div className="error" role="alert">{error}</div>}

      {brief && (
        <div className="brief">
          <h2>{brief.condition}</h2>

          <section>
            <h3>Standard of Care</h3>
            <ul>
              {brief.standard_of_care.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          </section>

          <section>
            <h3>Emerging Treatments</h3>
            <ul>
              {brief.emerging_treatments.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          </section>

          <section>
            <h3>Key Organizations</h3>
            <ul>
              {brief.key_organizations.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          </section>

          <section>
            <h3>Sources</h3>
            <ul className="sources">
              {brief.sources.map((source, i) => {
                const { href, label } = sourceToLink(source)
                return (
                  <li key={i}>
                    {href
                      ? <a href={href} target="_blank" rel="noopener noreferrer">{label}</a>
                      : label}
                  </li>
                )
              })}
            </ul>
          </section>
        </div>
      )}
    </div>
  )
}
