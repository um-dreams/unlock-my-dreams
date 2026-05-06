import { redirect } from "next/navigation"
import { getServerSession } from "next-auth/next"
import { BusinessPlanGenerator } from "@/components/BusinessPlanGenerator"

export default async function DashboardPage() {
  const session = await getServerSession()
  
  if (!session) {
    // For MVP testing, if no session, we'll bypass redirect so we can test the generator
    // redirect("/api/auth/signin")
  }

  // Use a hardcoded mock user UUID for now if session is missing
  const userId = "00000000-0000-0000-0000-000000000000"

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <header className="px-6 py-4 bg-white border-b border-gray-200">
        <h1 className="text-xl font-bold">Unlock My Dreams</h1>
      </header>
      <main className="flex-1 p-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold mb-4">Welcome back, {session?.user?.name || "Entrepreneur"}!</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200 md:col-span-2">
              <h3 className="font-semibold mb-2">My Business Plan</h3>
              <p className="text-sm text-gray-500 mb-4">Create your business plan using our AI consultant.</p>
              <BusinessPlanGenerator userId={userId} />
            </div>
            <div className="space-y-6">
              <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-semibold mb-2">Checklist</h3>
                <p className="text-sm text-gray-500">Generate a business plan first to see your tasks.</p>
              </div>
              <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-semibold mb-2">Website</h3>
                <p className="text-sm text-gray-500">Draft your business plan to unlock the website builder.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
