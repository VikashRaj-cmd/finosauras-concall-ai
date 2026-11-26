import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { API_BASE } from "../config"

function Section({ title, children }) {
  return (
    <div className="mb-8">
      <h2 className="text-base font-semibold text-gray-800 border-b border-gray-200 pb-2 mb-3">{title}</h2>
      {children}
    </div>
  )
}

function BulletList({ items }) {
  if (!items?.length) return <p className="text-sm text-gray-400">None reported.</p>
  return (
    <ul className="space-y-1.5">
      {items.map((item, i) => (
        <li key={i} className="flex gap-2 text-sm text-gray-700">
          <span className="text-blue-400 mt-0.5">•</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}

export default function SummaryDetail() {
  const { symbol } = useParams()
  const navigate = useNavigate()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/api/summaries/${symbol}`)
      .then((r) => r.json())
      .then((data) => { setSummary(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [symbol])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>
  if (!summary) return <div className="text-center py-20 text-gray-400">Summary not found.</div>

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <button onClick={() => navigate("/")} className="text-sm text-blue-600 hover:underline mb-2">
            ← Back to Dashboard
          </button>
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{summary.company}</h1>
              <p className="text-sm text-gray-500 mt-0.5">
                {summary.nse_symbol} · {summary.quarter} · {summary.source}
              </p>
            </div>
            <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
              Processed
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        <Section title="TL;DR">
          <BulletList items={summary.tldr} />
        </Section>

        <Section title="Management Commentary">
          <BulletList items={summary.management_commentary} />
        </Section>

        <Section title="Guidance & Outlook">
          <BulletList items={summary.guidance} />
        </Section>

        <Section title="Key Metrics">
          {summary.key_metrics?.length ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-gray-100 text-gray-600 text-left">
                    <th className="px-3 py-2 font-medium">Metric</th>
                    <th className="px-3 py-2 font-medium">Value</th>
                    <th className="px-3 py-2 font-medium">Context</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.key_metrics.map((m, i) => (
                    <tr key={i} className="border-t border-gray-100">
                      <td className="px-3 py-2 font-medium text-gray-800">{m.metric}</td>
                      <td className="px-3 py-2 text-blue-700 font-semibold">{m.value}</td>
                      <td className="px-3 py-2 text-gray-600">{m.context}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : <p className="text-sm text-gray-400">No metrics reported.</p>}
        </Section>

        <Section title="Segment Performance">
          {summary.segment_performance?.length ? (
            <div className="space-y-3">
              {summary.segment_performance.map((s, i) => (
                <div key={i} className="bg-white border border-gray-200 rounded-lg p-4">
                  <p className="font-medium text-gray-800 text-sm">{s.segment}</p>
                  <p className="text-sm text-gray-600 mt-1">{s.notes}</p>
                </div>
              ))}
            </div>
          ) : <p className="text-sm text-gray-400">No segment data reported.</p>}
        </Section>

        <Section title="Notable Q&A">
          {summary.notable_qa?.length ? (
            <div className="space-y-4">
              {summary.notable_qa.map((qa, i) => (
                <div key={i} className="bg-white border border-gray-200 rounded-lg p-4">
                  <p className="text-sm font-medium text-gray-500 mb-1">
                    Q — {qa.asked_by}
                  </p>
                  <p className="text-sm text-gray-800 mb-2">{qa.question}</p>
                  <p className="text-sm text-gray-500 font-medium mb-1">A — Management</p>
                  <p className="text-sm text-gray-700">{qa.answer}</p>
                </div>
              ))}
            </div>
          ) : <p className="text-sm text-gray-400">No Q&A reported.</p>}
        </Section>

        <Section title="Risks & Concerns">
          <BulletList items={summary.risks} />
        </Section>
      </main>
    </div>
  )
}
