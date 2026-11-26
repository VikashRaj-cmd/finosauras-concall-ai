import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { API_BASE } from "../config"
import { useWebSocket } from "../hooks/useWebSocket"
import CompanyCard from "../components/CompanyCard"
import LiveBadge from "../components/LiveBadge"

export default function Dashboard() {
  const [summaries, setSummaries] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch(`${API_BASE}/api/summaries`)
      .then((r) => r.json())
      .then((data) => { setSummaries(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const connected = useWebSocket((newSummary) => {
    setSummaries((prev) => {
      const exists = prev.find((s) => s.nse_symbol === newSummary.nse_symbol && s.quarter === newSummary.quarter)
      if (exists) return prev
      return [newSummary, ...prev]
    })
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Finosauras Concall AI</h1>
            <p className="text-sm text-gray-500 mt-0.5">Real-time earnings call intelligence</p>
          </div>
          <LiveBadge connected={connected} />
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-700">
            Latest Transcripts
            <span className="ml-2 text-sm font-normal text-gray-400">({summaries.length} companies)</span>
          </h2>
        </div>

        {loading ? (
          <div className="text-center py-20 text-gray-400">Loading summaries...</div>
        ) : summaries.length === 0 ? (
          <div className="text-center py-20 text-gray-400">No summaries yet. Run the pipeline first.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {summaries.map((s, i) => (
              <CompanyCard
                key={i}
                summary={s}
                onClick={() => {
                  const sym = s.nse_symbol || s.company.split(' ')[0].toUpperCase()
                  navigate(`/summary/${sym}`)
                }}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
