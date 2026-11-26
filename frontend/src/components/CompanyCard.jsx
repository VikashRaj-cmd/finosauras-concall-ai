export default function CompanyCard({ summary, onClick }) {
  return (
    <div
      onClick={onClick}
      className="bg-white border border-gray-200 rounded-xl p-5 cursor-pointer hover:shadow-md hover:border-blue-400 transition-all"
    >
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">{summary.company}</h2>
          <p className="text-sm text-gray-500 mt-0.5">
            {summary.nse_symbol} · {summary.quarter}
          </p>
        </div>
        <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">
          {summary.source || "BSE"}
        </span>
      </div>
      {summary.tldr?.length > 0 && (
        <p className="text-sm text-gray-600 mt-3 line-clamp-2">
          {summary.tldr[0]}
        </p>
      )}
      <div className="mt-3 flex gap-2 flex-wrap">
        {summary.key_metrics?.slice(0, 2).map((m, i) => (
          <span key={i} className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
            {m.metric}: {m.value}
          </span>
        ))}
      </div>
    </div>
  )
}
