'use client'

import { useState } from 'react'

export function BusinessPlanGenerator({ userId }: { userId: string }) {
  const [idea, setIdea] = useState('')
  const [plan, setPlan] = useState<any>(null)
  const [checklist, setChecklist] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/plans/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, idea })
      })
      const data = await res.json()
      setPlan(data.plan_content)
      setChecklist(data.checklist || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (plan) {
    return (
      <div className="mt-6 p-4 border rounded bg-gray-50">
        <h3 className="text-xl font-bold mb-2">{plan.title}</h3>
        <p className="font-semibold mt-4">Executive Summary</p>
        <p className="text-sm text-gray-700">{plan.executive_summary}</p>
        
        <p className="font-semibold mt-4">Target Market</p>
        <p className="text-sm text-gray-700">{plan.target_market}</p>
        
        <p className="font-semibold mt-4">Revenue Model</p>
        <p className="text-sm text-gray-700">{plan.revenue_model}</p>
        
        <p className="font-semibold mt-4">Competitors</p>
        <ul className="list-disc pl-5 text-sm text-gray-700">
          {plan.competitors?.map((c: string, i: number) => <li key={i}>{c}</li>)}
        </ul>

        {checklist.length > 0 && (
          <div className="mt-8 border-t pt-4">
            <h4 className="text-lg font-bold mb-3">Your Launch Checklist</h4>
            <div className="space-y-3">
              {checklist.map((item, idx) => (
                <div key={idx} className="flex items-start">
                  <input type="checkbox" className="mt-1 mr-3" />
                  <div>
                    <p className="font-semibold">{item.title}</p>
                    <p className="text-sm text-gray-600">{item.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="mt-6">
      <textarea 
        className="w-full p-3 border rounded border-gray-300 text-sm min-h-[100px]"
        placeholder="Describe your business idea... e.g., A subscription box for exotic teas."
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
      />
      <button 
        onClick={handleGenerate}
        disabled={loading || !idea.trim()}
        className="mt-3 px-4 py-2 bg-black text-white rounded text-sm disabled:opacity-50"
      >
        {loading ? 'Generating Plan...' : 'Generate Plan with AI'}
      </button>
    </div>
  )
}
