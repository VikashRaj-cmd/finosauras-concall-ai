import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import SummaryDetail from "./pages/SummaryDetail"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/summary/:symbol" element={<SummaryDetail />} />
      </Routes>
    </BrowserRouter>
  )
}
